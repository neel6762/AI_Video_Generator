# AI Video Generation System

An AI-powered video generation system that creates videos from text prompts using local text and image-to-text models and other tools. This project demonstrates the integration of multiple AI technologies to automate video creation, including script generation, image generation, audio synthesis, and video assembly.

## Features

- **AI-Powered Script Generation**: Creates structured video scripts from user prompts using local LLM models
- **Project Management**: Organizes generated content into structured project directories
- **Image Generation**: Generates relevant visuals for each section of the video using Stable Diffusion
- **Text-to-Speech**: Converts script narration into high-quality audio using gTTS
- **Video Assembly**: Automatically combines generated images and audio into a cohesive video
- **Local Processing**: Runs entirely on your local machine using Ollama for LLM and local models for image generation


## Prerequisites

Use the requirements.txt file to install the dependencies.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install and set up Ollama:
- Follow the instructions at [Ollama's official website](https://ollama.ai) to install Ollama
- Pull the required model:
```bash
ollama pull qwen3:14b
```

3. Install and set up Stable Diffusion:
- Reference from [Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

## Usage

1. Start the video generation process:
```bash
python agent.py
```

2. Enter your prompt when prompted. For example:
```
Enter your prompt to generate a video: The history of artificial intelligence
```

The system will:
1. Generate a structured video script
2. Create relevant images for each section
3. Generate audio narration
4. Assemble everything into a final video

The output will be saved in the `projects` directory, organized by project name.

## Project Structure

- `agent.py`: Main entry point and agent initialization
- `utils.py`: Core functionality for video generation
- `config.py`: Configuration settings
- `multiple_generation.py`: Generate multiple videos from a list of prompts
- `test_tools.py`: Test the tools in isolation
- `projects/`: Directory containing generated content
  - Each project has its own subdirectory with:
    - Generated script (JSON)
    - Image files
    - Audio files
    - Final video

## Configuration

The system can be configured through `config.py`. Key settings include:
- LLM model parameters
- Image generation settings
- System prompts