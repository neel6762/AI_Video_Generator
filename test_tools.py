import utils

def test_tools():
    """Test all the tools in the utils.py file."""
    
    # Test generate_video_script
    print("Testing generate_video_script...")
    project_dir, script_path = utils.generate_video_script("Commercial for a pizza shop - Uncle John's Pizza")
    print(f"Script generated at: {script_path}")
    
    # Test generate_visuals
    print("\nTesting generate_visuals...")
    project_dir, image_dir = utils.generate_visuals(project_dir, script_path)
    print(f"Images generated in: {image_dir}")
    
    # Test generate_audio_from_script
    print("\nTesting generate_audio_from_script...")
    project_dir, audio_dir = utils.generate_audio_from_script(project_dir, script_path)
    print(f"Audio files generated in: {audio_dir}")
    
    # # Test assemble_video
    print("\nTesting assemble_video...")
    utils.assemble_video(project_dir, image_dir, audio_dir)
    print(f"Video assembled in: {project_dir}")
    
if __name__ == "__main__":
    test_tools()
