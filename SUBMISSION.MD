# TRP 1 - AI-Content Generation Challenge

Overview
This challenge measures your ability to explore, understand, and operate an existing AI content generation codebase. In the 2026 Forward Deployed Engineer (FDE) role, you will rarely build systems from scratch—instead, you will inherit complex codebases, decipher their architecture, and deploy them to solve real-world problems.

The question we are answering: Can you explore an unfamiliar codebase, understand its capabilities, configure it correctly, and generate meaningful outputs despite incomplete documentation?

## Part 1: Environment Setup & API Configuration (30 min)

You are given access to the ai-content package—a multi-provider AI content generation framework.

Your tasks:

Clone and Install the Package

# Clone
git clone https://github.com/10xac/trp1-ai-artist.git
cd trp1-ai-artist

# Setup
cp .env.example .env

# Edit .env with their API keys
uv sync

# Run
uv run ai-content --help
uv run ai-content music --style jazz --provider lyria

Obtain API Keys (Choose at least ONE provider)

Provider
Purpose
How to Get
Google Gemini
Music (Lyria), Video (Veo), Image (Imagen)
Google AI Studio → Get API Key
AIMLAPI
Music with Vocals (MiniMax)
AIMLAPI.com → Sign up → API Keys


Configure Your Environment

Create a .env file in the project root:

# Google Gemini API (for Lyria music, Veo video, Imagen images)
GEMINI_API_KEY=your_google_api_key_here

# AIMLAPI (for MiniMax music with vocals)
AIMLAPI_KEY=your_aimlapi_key_here

Verify Installation

uv run ai-content --help
uv run ai-content list-providers
uv run ai-content list-presets

Note: You do NOT need KlingAI credentials. Gemini and/or AIMLAPI are sufficient.

## Part 2: Codebase Exploration (30 min)

Before generating content, you must understand the system you're working with.

Explore and document:

Package Structure

What are the main modules in src/ai_content/?
How are providers organized?
What is the purpose of the pipelines/ directory?

Provider Capabilities

What music providers are available? What are their differences?
What video providers are available? Which supports image-to-video?
Which provider supports vocals/lyrics?

Preset System

List all available music presets with their BPM and mood
List all available video presets with their aspect ratios
How would you add a new preset?

CLI Commands

What commands are available?
What options does the music command accept?
What options does the video command accept?
Part 3: Content Generation (30 min)
Now, put your understanding to work by generating actual content.

Required Generations:

Generate Audio Content of your Choice (lyria generates only Instrumental)

# Using a cli and preset
uv run ai-content music --style jazz --provider lyria --duration 30

# Or with existing script
uv run python examples/lyria_example_ethiopian.py --style ethio-jazz --duration 30
uv run python examples/lyria_example_ethiopian.py --style tizita-blues
uv run python examples/lyria_example_ethiopian.py --style eskista-dance

# Or with custom prompt
uv run ai-content music --prompt "Your creative prompt here" --provider lyria

Generate Audio Vocals (if you have AIMLAPI key)

Create a lyrics file (.txt)
Use MiniMax provider with lyrics:

uv run ai-content music --prompt "Your style prompt" --provider minimax --lyrics path/to/lyrics.txt

Generate Video

uv run ai-content video --style nature --provider veo --duration 5

Combine into a Music Video (Bonus)

Use FFmpeg to merge your audio and video:

ffmpeg -i video.mp4 -i music.wav -c:v copy -c:a aac -shortest output.mp4

Artifacts:

At least 1 generated audio files (different styles/providers)
At least 1 generated video file
(Bonus) 1 combined video

Part 4: YouTube Upload & Submission (30 min)
Upload Requirements:

Upload your best generated content to YouTube (unlisted is fine)
Title format: [TRP1] Your Name - Content Description
Description should include:
Prompt used for generation
Provider and preset used
Any creative decisions made

Submission Package:

Create a submission report (SUBMISSION.md) containing:

Environment Setup Documentation

Which APIs did you configure?
Any issues encountered during setup?
How did you resolve them?

Codebase Understanding

Architecture diagram or description
Key insights about the provider system
How the pipeline orchestration works

Generation Log

Commands executed
Prompts used and why
Results achieved (screenshots, file sizes, durations)

Challenges & Solutions

What didn't work on first try?
How did you troubleshoot?
What workarounds did you discover?

Insights & Learnings

What surprised you about the codebase?
What would you improve?
How does this compare to other AI tools you've used?

Links

YouTube video link(s)
GitHub repo with your exploration artifacts


Grading Rubric Overview
Category
Points
Focus
Environment Setup & Configuration
25
Successful API setup, working installation
Codebase Exploration & Documentation
25
Depth of understanding, quality of exploration artifacts
Content Generation
15
Successfully generated audio/video, creative use of presets
Troubleshooting & Persistence
20
Documented challenges, workarounds found
Curiosity & Extra Effort
15
Exploration beyond requirements, insights gained
Total
100





Tips for Success
Read the Source Code - The best documentation is often in the code itself. Look at src/ai_content/providers/ to understand how each provider works.

Check the Examples - The examples/ directory contains working code for common use cases.

Use the Presets - Start with presets before crafting custom prompts. They're optimized for good results.

Document Everything - Your troubleshooting journey is as valuable as your final output. We want to see how you think.

Ask Unblocking Questions - If you're stuck for more than 15 minutes, describe your problem clearly and ask for help.


Available Commands Reference
# List available options
uv run ai-content list-providers
uv run ai-content list-presets

# Music generation
uv run ai-content music --style <preset> --provider <lyria|minimax>
uv run ai-content music --prompt "..." --provider lyria --bpm 120 --duration 30
uv run ai-content music --prompt "..." --provider minimax --lyrics path/to/file.txt

# Video generation
uv run ai-content video --style <preset> --provider veo
uv run ai-content video --prompt "..." --provider veo --aspect 16:9 --duration 5

Submission Checklist
SUBMISSION.md - Complete report
YouTube link(s) in submission
GitHub repo link in submission



Good luck! Remember: We're measuring your exploration, comprehension, and persistence—not just the final output.

