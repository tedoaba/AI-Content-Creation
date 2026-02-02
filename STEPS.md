

## Part 3: Content Generation

Now, put your understanding to work by generating actual content.

Required Generations:

### Generate Audio Content of your Choice (lyria generates only Instrumental)

#### Using a cli and preset

```bash
uv run ai-content music --style jazz --provider lyria --duration 30
```

- didn't work at first it was asking me for a prompt

#### Or with existing script

```bash
uv run python examples/lyria_example_ethiopian.py --style ethio-jazz --duration 30
```

- I was able to generate the audio content `ethio_jazz_instrumental.wav`, size 2.20MB, duration 30 seconds with Ethio-Jazz Fusion style.


#### Or with custom prompt

```bash
uv run python examples/lyria_example_ethiopian.py --style tizita-blues
```

- I was able to generate the audio content `tizita_blues_instrumental.wav`, size 5.13MB, duration 30 seconds with Tizita Blues style.

```bash
uv run python examples/lyria_example_ethiopian.py --style eskista-dance
```

- I was able to generate the audio content `eskista_dance_instrumental.wav`, size 2.20MB, duration 30 seconds with Eskista Dance Music style.

#### Or with custom prompt

```bash
uv run ai-content music --prompt "Ethiopian Tizita with a litle dance beat integrated" --provider lyria
```

- I was able to generate the audio content `lyria_20260202_124625.wav`, size 2.20MB, duration 30 seconds.


#### Generate Audio Vocals (if you have AIMLAPI key)

Create a lyrics file (.txt)
Use MiniMax provider with lyrics:

```bash
uv run ai-content music --prompt "Ethiopian song about ADWA victory celebrating warriors and inspiring younger generations" --provider minimax --lyrics lyrics_with_aiml.txt
```

- I have generated the poem using ChatGPT about adwa and put it in the `.txt` file but the API key doesn't work (I have created one and added to .env file but couldn't reach it (404 error))

Generate Video

```bash
uv run ai-content video --style nature --provider veo --duration 5
```

- I got error for missing prompts

```bash
uv run ai-content video \
  --prompt "Ethiopian song about ADWA victory celebrating warriors and inspiring younger generations" \
  --provider veo \
  --aspect 16:9
```

- then I got `Error: module 'google.genai.types' has no attribute 'GenerateVideoConfig'`

The Google Veo provider was updated to use the latest google-genai SDK, replacing generate_video/GenerateVideoConfig with generate_videos/GenerateVideosConfig, simplifying handling of text-to-video and image-to-video through dynamic source_kwargs, unifying configuration for aspect ratio, person generation, and number of videos, and streamlining response access to video.video_bytes; polling was updated from aio methods to synchronous-style operations, class documentation was refreshed, and redundant code and comments were removed, while maintaining all previous features.

- after that I got `allow_adult` error and comment that that out to generate the video

- then I got quota error for veo because it requires a paid project api key to generate video

I attempted to generate a video with the Veo provider using the prompt:

"Ethiopian song about ADWA victory celebrating warriors and inspiring younger generations"

with a 16:9 aspect ratio. During generation, I received the following error:

`429 RESOURCE_EXHAUSTED: You exceeded your current quota, please check your plan and billing details.`


This indicates that my Google GenAI quota was exceeded, preventing the video from being created. I was advised to check my plan, billing details, and review the Gemini API rate limits
 for further guidance.


Combine into a Music Video (Bonus)

Use FFmpeg to merge your audio and video:

```bash
ffmpeg -i video.mp4 -i music.wav -c:v copy -c:a aac -shortest output.mp4
```

- couldn't get a generated video to mix with an audio
- 