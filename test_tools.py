import utils
import os

def test_tools(user_prompt: str):
    """Test all the tools in the utils.py file."""
    
    # Test generate_video_script
    print("Testing generate_video_script...")
    script_path = utils.generate_video_script(user_prompt)
    print(f"Script generated at: {script_path}")
    
    project_dir = os.path.dirname(script_path)
    
    # Test generate_visuals
    print("\nTesting generate_visuals...")
    image_dir = utils.generate_visuals(script_path)
    print(f"Images generated in: {image_dir}")
    
    # Test generate_audio_from_script
    print("\nTesting generate_audio_from_script...")
    audio_dir = utils.generate_audio_from_script(script_path)
    print(f"Audio files generated in: {audio_dir}")
    
    # # Test assemble_video
    print("\nTesting assemble_video...")
    utils.assemble_video(project_dir)
    print(f"Video assembled in: {project_dir}")
    
if __name__ == "__main__":
    user_prompt = input("Enter the topic of the video: ")
    test_tools(user_prompt)
