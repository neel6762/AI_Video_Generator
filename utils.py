from typing import List
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from langchain_community.tools import DuckDuckGoSearchResults
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import requests
from pydantic import BaseModel
import json


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

        print(f'...Done Performing Search on Query: {query}')
        return scraped_content


