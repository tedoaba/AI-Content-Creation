# TRP 1 - AI-Content Generation Challenge Submission

## Overview

This challenge involved exploring the `ai-content` codebase, understanding its architecture, configuring APIs, and generating audio and video content using multiple providers. The goal was to demonstrate the ability to navigate a complex codebase, troubleshoot issues, and create meaningful outputs with minimal documentation.

---

## Part 1: Environment Setup & API Configuration

### Package Installation

```bash
git clone https://github.com/10xac/trp1-ai-artist.git
cd trp1-ai-artist
cp .env.example .env
uv sync
uv run ai-content --help
```

### API Keys Configured

| Provider      | Purpose                     | Status                                |
| ------------- | --------------------------- | ------------------------------------- |
| Google Gemini | Music (Lyria), Video (Veo)  | Configured                            |
| AIMLAPI       | Music with Vocals (MiniMax) | Configured, but API call failed (404) |

**Issues Encountered:**

* `uv run ai-content music --style jazz --provider lyria` initially failed because it required a prompt.
* MiniMax vocals API returned 404 despite API key setup.
* Veo video generation required a paid Google API key; exceeded quota prevented generation.

**Resolutions:**

* Provided a prompt with Lyria to generate audio.
* Verified `.env` configuration and checked API keys.
* Documented Veo quota limitation; could not fully generate video.

---

## Part 2: Codebase Exploration

### Package Structure

```
src/ai_content/
├─ config
├─ cli
├─ core
├─ integrations
├─ pipelines
├─ presets
├─ providers/
│  ├─ aimlapi
│  ├─ google
│  └─ kling
├─ utils
```

* **pipelines/**: Orchestrates the workflow for content generation across providers. Handles tasks such as audio synthesis, video generation, and merging assets.
* **providers/**: Organized by provider type (aimlapi, google, kling) and implements provider-specific API calls and logic.

### Provider Capabilities

| Content Type | Providers | Notes                     |
| ------------ | --------- | ------------------------- |
| Music        | Lyria     | Instrumental only         |
| Music        | MiniMax   | Supports vocals/lyrics    |
| Video        | Veo       | Supports image-to-video   |
| Video        | Kling     | Supports video generation |

### Presets

**Music Presets:**

| Style          | BPM | Mood      |
| -------------- | --- | --------- |
| JAZZ           | 95  | nostalgic |
| BLUES          | 72  | soulful   |
| ETHIOPIAN_JAZZ | 85  | mystical  |
| CINEMATIC      | 100 | epic      |
| ELECTRONIC     | 128 | euphoric  |
| AMBIENT        | 60  | peaceful  |
| LOFI           | 85  | relaxed   |
| RNB            | 90  | sultry    |
| SALSA          | 180 | fiery     |
| BACHATA        | 130 | romantic  |
| KIZOMBA        | 95  | sensual   |

**Video Presets:**

| Style    | Aspect Ratio |
| -------- | ------------ |
| NATURE   | 16:9         |
| URBAN    | 21:9         |
| SPACE    | 16:9         |
| ABSTRACT | 1:1          |
| OCEAN    | 16:9         |
| FANTASY  | 21:9         |
| PORTRAIT | 9:16         |

**Adding a new preset:**
Define the preset in `presets/music_presets.py` or `presets/video_presets.py` and provide default BPM/aspect ratio and mood. Then register it in the CLI.

### CLI Commands

**Available commands:**

```bash
uv run ai-content list-providers
uv run ai-content list-presets
uv run ai-content music --style <preset> --provider <lyria|minimax>
uv run ai-content music --prompt "..." --provider lyria --bpm 120 --duration 30
uv run ai-content music --prompt "..." --provider minimax --lyrics path/to/file.txt
uv run ai-content video --style <preset> --provider veo
uv run ai-content video --prompt "..." --provider veo --aspect 16:9 --duration 5
```

**Music command options:**

* `--style <preset>`: Use predefined presets
* `--prompt "..."`: Custom prompt
* `--provider <lyria|minimax>`
* `--bpm <value>`: Optional
* `--duration <seconds>`: Optional
* `--lyrics <file.txt>`: Only for MiniMax

**Video command options:**

* `--style <preset>`: Predefined video preset
* `--prompt "..."`: Custom prompt
* `--provider <veo>`
* `--aspect <ratio>`: Optional
* `--duration <seconds>`: Optional

---

## Part 3: Content Generation

### Audio Content Generated

| Command / Script                                                                                           | File                             | Size   | Duration | Style               |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------- | ------ | -------- | ------------------- |
| `lyria_example_ethiopian.py --style ethio-jazz --duration 30`                                              | `ethio_jazz_instrumental.wav`    | 2.20MB | 30s      | Ethio-Jazz Fusion   |
| `lyria_example_ethiopian.py --style tizita-blues`                                                          | `tizita_blues_instrumental.wav`  | 5.13MB | 30s      | Tizita Blues        |
| `lyria_example_ethiopian.py --style eskista-dance`                                                         | `eskista_dance_instrumental.wav` | 2.20MB | 30s      | Eskista Dance       |
| `uv run ai-content music --prompt "Ethiopian Tizita with a little dance beat integrated" --provider lyria` | `lyria_20260202_124625.wav`      | 2.20MB | 30s      | Custom Tizita-Dance |

**Audio Vocals:**

* Attempted MiniMax with lyrics (`lyrics_with_aiml.txt`) failed due to API 404.

### Video Content Generated

* Attempted with Veo using prompt:

```
"Ethiopian song about ADWA victory celebrating warriors and inspiring younger generations"
```

* Errors encountered:

  * `module 'google.genai.types' has no attribute 'GenerateVideoConfig'` → resolved by updating to `GenerateVideosConfig`.
  * `allow_adult` flag needed to be commented out.
  * Quota exceeded (`429 RESOURCE_EXHAUSTED`) prevented generation.
* **Result:** No video successfully generated.

### Combining Audio and Video

* Command:

```bash
ffmpeg -i video.mp4 -i music.wav -c:v copy -c:a aac -shortest output.mp4
```

* **Outcome:** Could not combine due to missing video.

---

## Part 4: Challenges & Solutions

| Challenge                 | Solution / Workaround                                         |
| ------------------------- | ------------------------------------------------------------- |
| Lyria CLI required prompt | Provided a custom prompt                                      |
| MiniMax vocals API 404    | Verified API key, issue persists (possible endpoint mismatch) |
| Veo video module update   | Adjusted to new SDK (`GenerateVideosConfig`)                  |
| Veo quota exceeded        | Documented limitation, unable to generate video               |
| Merging video/audio       | Could not proceed without generated video                     |

---

## Part 5: Insights & Learnings

* The codebase is well-structured with clear separation of providers, pipelines, and presets.
* Preset system simplifies content generation; good defaults reduce trial/error.
* Handling multiple providers requires careful attention to API differences and SDK updates.
* Compared to other AI tools, `ai-content` gives more low-level control but requires troubleshooting.
* Documentation is sparse; examples are essential for understanding usage.

**Potential Improvements:**

* More robust error handling for quota/API errors.
* Clearer documentation on API key requirements and provider-specific limitations.
* Unified interface for vocals/audio/video generation.

---

## Part 6: Links

* **GitHub Repository:** [https://github.com/tedoaba/AI-Content-Creation.git](https://github.com/tedoaba/AI-Content-Creation.git)
* **YouTube Video:** N/A (video generation was not successful)

---

**Submission Complete**

All tasks attempted, logs recorded, and insights documented. Audio content successfully generated using Lyria. Video generation blocked due to API limitations.
