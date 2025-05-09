from typing import List
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from langchain_community.tools import DuckDuckGoSearchResults
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from pydantic import BaseModel, Field
import json
import os
import datetime
import torch
from diffusers import DiffusionPipeline

from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from config import CONFIG


class ScriptSection(BaseModel):
    section_number: int = Field(..., description="The number of the section in the video")
    section_title: str = Field(..., description="The title of the section")
    narration: str = Field(..., description="The narration of the section")
    prompt_for_image: List[str] = Field(..., description="The prompt for the image")


class VideoScript(BaseModel):
    project_name: str = Field(..., description="The name of the project")
    title: str = Field(..., description="The title of the video")
    description: str = Field(..., description="The description of the video")
    script_sections: List[ScriptSection] = Field(..., description="The sections of the video")

@tool
def generate_video_script(user_prompt: str) -> str:
    """Generates a video script from a given prompt.
    
    :param user_prompt: The prompt to generate the video script from.
    :return: The video script in json format.
    """
    
    output_dir = "llm_responses"
    os.makedirs(output_dir, exist_ok=True)
    
    model_config = CONFIG["llm_model_config"]
    prompt_config = CONFIG["llm_prompt_config"]
    
    model = ChatOllama(
        model = model_config["model_name"],
        temperature = model_config["temperature"],
        num_ctx = model_config["num_ctx"],
        keep_alive = 0
    )
            
    USER_PROMPT = f"""Generate a video script for the following prompt:
    {user_prompt}

    # Example
    User Prompt: 
    "History of football"
    
    Output:
    {prompt_config["example_prompt"]}
    """
    
    messages = [
        SystemMessage(content=[{"type": "text", "text": prompt_config["system_prompt"]}]),
        HumanMessage(content=[{"type": "text", "text": USER_PROMPT}]),
    ]
    
    structured_output = model.with_structured_output(VideoScript)
    response = structured_output.invoke(messages)
    json_response = response.model_dump()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"llm_response_{response.project_name}_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        json.dump(json_response, f)
    
    return json_response

@tool   
def generate_images(llm_response: dict):
    """Generate images from the llm response. Uses prompt suggestions from the llm response to generate images 
    and saves them to the project directory.
    
    :param llm_response: The llm response in json format
    :return: str (path to the project directory)
    """

    model_id = CONFIG["image_generation_config"]["model_name"]
    num_inference_steps = CONFIG["image_generation_config"]["num_inference_steps"]
    guidance_scale = CONFIG["image_generation_config"]["guidance_scale"]

    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    pipe = DiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )

    pipe = pipe.to(device)
    project_dir = os.path.join("images", llm_response["project_name"])
    
    os.makedirs(project_dir, exist_ok=True)

    for section in llm_response["script_sections"]:
        section_number = section["section_number"]
        section_description = section["narration"]
        print(f"-------------------\n{section_description}\n-------------------\n")

        for index, prompt in enumerate(section["prompt_for_image"]):
            print(f"Generating image for {prompt}")
            print(f"Prompt: {prompt}")
            image = pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]
            image.save(os.path.join(project_dir, f"section_{section_number}_image_{index + 1}.png"))
            print(f"Image saved as {os.path.join(project_dir, f'section_{section_number}_image_{index + 1}.png')}")
    
    return project_dir


@tool
def assemble_video(image_paths: List[str], audio_paths: List[str], output_path: str):
    """
    Assembles a video by pairing images with corresponding audio clips and outputs the final video.
    len(audio_paths) must be the same as the len(image_paths). The image at image_paths[n] will be
    displayed for the entire duration of the audio at audio_paths[n], and the video will be created
    by concatenating the video segments from indices 0 to len(audio_paths).

    :param image_paths: List of file paths to the images to be used in the video.
    :param audio_paths: List of file paths to the audio files that will be synced with the images.
    :param output_path: Path where the final video file will be saved. use .mp4 in the filename
    :return: None
    """

    image_clips = []

    for image_path, audio_path in zip(image_paths, audio_paths):

        # Load the audio clip
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Create an image clip with the duration of the audio clip
        image_clip = ImageClip(image_path).set_duration(duration)

        # Set the audio of the image clip
        image_clip = image_clip.set_audio(audio_clip)
        image_clips.append(image_clip)

    # Concatenate the image clips
    video_clip = concatenate_videoclips(image_clips, method="compose")

    # Write the video file
    video_clip.write_videofile(output_path, fps=24)


class DuckDuckGoSearchTool:
    def __init__(self):
        # Initialize search tool and session
        self.session = HTMLSession()
        self.search = DuckDuckGoSearchResults()

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from the results of the LangChain duck duck go search tool."""
        url_pattern = r'https?://[^\s,]+'
        urls = re.findall(url_pattern, text)
        return urls

    def scrape_and_clean(self, url: str) -> str:
        """Scrape and clean text content from a given URL. Doesn't always work well with javascript websites."""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ')
            return text
        except Exception as e:
            print(f"Failed to scrape URL {url}: {e}")
            return None

    def return_search_results(self, query: str, num_results: int=5) -> List[str]:
        """Perform a search query and return scraped content."""
        print(f'Performing Search on Query: {query} ...')

        # Perform a search query
        results = self.search.invoke(query, num_results=num_results)

        # Extract URLs from the search results
        urls = self.extract_urls(results)

        # Scrape and clean content for each URL
        scraped_content = []
        for url in urls:
            content = self.scrape_and_clean(url)
            if content:
                scraped_content.append(content)
            break

        print(f'...Done Performing Search on Query: {query}')
        return scraped_content

