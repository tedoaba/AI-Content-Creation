import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from ai_content.core.registry import ProviderRegistry
from ai_content.core.result import GenerationResult
from ai_content.core.exceptions import (
    ProviderError,
    AuthenticationError,
    TimeoutError,
)
from ai_content.config import get_settings

logger = logging.getLogger(__name__)

@ProviderRegistry.register_video("veo")
class GoogleVeoProvider:
    """
    Google Veo video provider using the latest google-genai SDK.

    Supports:
      - Text-to-video
      - Image-to-video (first frame)
    """

    name = "veo"
    supports_image_to_video = True
    max_duration_seconds = 8

    def __init__(self):
        self.settings = get_settings().google
        self._client = None

    def _get_client(self):
        """Lazy-load the Google GenAI client."""
        if self._client is None:
            try:
                from google import genai
                api_key = self.settings.api_key
                if not api_key:
                    raise AuthenticationError("veo")
                self._client = genai.Client(api_key=api_key)
            except ImportError:
                raise ProviderError(
                    "veo",
                    "google-genai package not installed. Run: pip install google-genai",
                )
        return self._client

    async def generate(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "16:9",
        duration_seconds: int = 5,
        first_frame_url: str | None = None,
        output_path: str | None = None,
        use_fast_model: bool = False,
        person_generation: str = "allow_adult",
    ) -> GenerationResult:

        client = self._get_client()
        from google.genai import types

        model = (
            self.settings.video_fast_model
            if use_fast_model
            else self.settings.video_model
        )

        logger.info(f"🎬 Veo: Generating video ({aspect_ratio})")
        logger.debug(f"   Prompt: {prompt[:50]}...")
        logger.debug(f"   Model: {model}")

        try:
            # Build the source & config
            source_kwargs = {}
            if first_frame_url:
                image_bytes = await self._fetch_image(first_frame_url)
                source_kwargs["image"] = types.Image(image_bytes=image_bytes)
                # Prompt can be optional in image-to-video
                source_kwargs["prompt"] = prompt
            else:
                source_kwargs["prompt"] = prompt

            config = types.GenerateVideosConfig(
                        aspect_ratio=aspect_ratio,
                        # person_generation=person_generation,
                        number_of_videos=1,
                    )



            # Kick off generation
            operation = client.models.generate_videos(
                model=model,
                **source_kwargs,
                config=config,
            )

            # Poll until done
            logger.info("   Waiting for generation...")
            while not operation.done:
                await asyncio.sleep(5)
                operation = await client.operations.get(operation)

            if not operation.response or not operation.response.generated_videos:
                return GenerationResult(
                    success=False,
                    provider=self.name,
                    content_type="video",
                    error="No video generated",
                )

            video = operation.response.generated_videos[0].video
            video_bytes = video.video_bytes

            # Save file
            if output_path:
                file_path = Path(output_path)
            else:
                out_dir = get_settings().output_dir
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                file_path = out_dir / f"veo_{timestamp}.mp4"

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(video_bytes)

            logger.info(f"✅ Veo: Saved to {file_path}")

            return GenerationResult(
                success=True,
                provider=self.name,
                content_type="video",
                file_path=file_path,
                data=video_bytes,
                metadata={
                    "aspect_ratio": aspect_ratio,
                    "model": model,
                    "prompt": prompt,
                },
            )

        except Exception as e:
            logger.error(f"Veo generation failed: {e}")
            return GenerationResult(
                success=False,
                provider=self.name,
                content_type="video",
                error=str(e),
            )

    async def _fetch_image(self, url: str) -> bytes:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
