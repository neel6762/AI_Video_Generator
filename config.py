SYSTEM_PROMPT_AGENT = """
You are an expert video creator tasked with generating a high-quality video based on a provided text prompt. Your goal is to produce a cohesive, engaging, and visually appealing video by leveraging your creativity and the tools available to you.

# Instructions
- Use the example prompt provided to you to generate the final video that incldues script generation, visuals generation, audio generation, and video assembly.
- It is important that you use all the tools provided to you to generate the final video.
"""

SYSTEM_PROMPT_SCRIPT_WRITER = """You are an expert scriptwriter, you are tasked in generating video scripts from a given text prompt.
    # Instructions
    - Generate a video script that is 5 minutes long.
    - The script should be engaging and interesting.

    # Output Format
    - Keep total narration suitable for 5 minutes (~700-750 words).
    - Use clear and engaging language suitable for a general audience.
    - Include 6-8 sections (chronological or thematic).
    - Provide 3–4 visual suggestions per section to guide video creation.
    - The script should be in the form of a story, with a beginning, middle, and end.

    # Output Struture
    The output should be a JSON object with the following structure:

    {
        "project_name": "string",
        "title": "string",
        "description": "string",
        "script_sections": [
          {
            "section_number": "number",
            "section_title": "string",
            "narration": "string",
            "prompt_for_image": ["string", "string"]
          },
          {
            "section_number": "number",
            "section_title": "string",
            "narration": "string",
            "prompt_for_image": ["string", "string"]
          },
          ......
        ]
    }
    """

EXAMPLE_PROMPT_SCRIPT_WRITER = """
{
    "project_name": "football_history",
    "title": "The History of Football: From Ancient Times to the Modern Game",
    "description": "Explore the rich history of football, from its ancient ceremonial origins to its rise as the most celebrated global sport. This journey uncovers how a simple ball game became a powerful symbol of unity, competition, and cultural identity.",
    "duration_minutes": 8,
    "script_sections": [
        {
            "section_number": 1,
            "section_title": "Origins in Ancient Civilizations",
            "narration": "The origins of football date back over two thousand years, deeply rooted in ancient civilizations. In China, a military training game called Cuju was popular, where soldiers kicked a leather ball through a small circular goal to improve agility. Ancient Greece and Rome had their own versions—Episkyros and Harpastum—played during grand public festivals, blending athletic skill with entertainment. Across the Atlantic, the Maya and Aztecs played ritualistic ball games using heavy rubber balls in stone courts, often accompanied by music and spiritual ceremonies. These games held deep cultural and religious meaning, sometimes deciding the fate of leaders and communities. Though differing in style, all these early ball games shared a universal theme—celebrating physical skill, unity, and cultural identity.",
            "prompt_for_image": [
                "Ancient Chinese soldier playing Cuju, bronze armor, kicking leather ball through small wooden ring, grassy field, foggy morning, cinematic wide shot, realistic textures",
                "Roman citizens in white togas playing Harpastum in crowded stone plaza, marble columns behind, midday sunlight, cobblestone streets, vibrant historical cityscape",
                "Mesoamerican ball court, tall carved stone walls, two players in feathered headdresses with large rubber ball, ceremonial scene, dramatic sunset, wide angle view",
                "Ancient Greek athletes in short white tunics playing Episkyros near marble amphitheater, golden sunlight, spectators on stone seats, dynamic athletic poses, clear blue sky",
                "Museum exhibit close-up of historical balls: aged leather Cuju ball, small Roman Harpastum ball, dark rubber Mesoamerican ball on velvet cloth under spotlight, high detail"
            ]
        },
        {
            "section_number": 2,
            "section_title": "Medieval Folk Football: Chaos and Community",
            "narration": "During medieval times, football evolved into chaotic village-wide events across Europe. Known as folk football, these rough matches featured hundreds of participants chasing a leather ball through narrow streets and open fields. With few rules, games were wild and often violent, lasting for hours or even days. Despite their unruly nature, they were vital social events that reinforced community bonds and local pride. Authorities often attempted to ban these games for their disruptive nature, but the passion for football couldn’t be contained. These traditions paved the way for the organized sport we recognize today.",
            "prompt_for_image": [
                "Medieval villagers chasing a leather ball through narrow cobbled streets, chaotic scene, torn tunics, stone houses in background, overcast sky, historical realism",
                "Large group of peasants playing football on muddy village field, worn leather ball, dynamic action, people falling and laughing, rustic wooden fences in background",
                "Medieval town square crowded with excited villagers watching a chaotic football match, vibrant flags hanging, stone buildings, dusk lighting, cinematic composition",
                "Local authority figures in cloaks trying to disperse an unruly football crowd, raised wooden sticks, frustrated expressions, village backdrop, cloudy sky",
                "Abandoned muddy leather football near old stone wall, torn fabric, historical village scenery, dramatic lighting, close-up perspective"
            ]
        },
        {
            "section_number": 3,
            "section_title": "The Rise of Modern Rules",
            "narration": "By the 19th century, the chaos of folk football called for order. British public schools like Eton and Harrow began formalizing their own football rules, leading to the first standardized version of the game. In 1863, the Football Association (FA) was established in London, officially separating football from rugby and defining clear rules centered around kicking, not carrying, the ball. This pivotal moment transformed football from a local pastime into an organized sport. Football clubs formed, leagues were established, and the modern game began its journey toward global popularity.",
            "prompt_for_image": [
                "Victorian gentlemen in formal suits discussing football rules in candlelit room, parchment papers on large oak table, historical setting, high detail",
                "Early football match with players in long-sleeve shirts and high socks playing on grassy field, vintage leather ball, cloudy skies, wide shot",
                "Illustration of 1863 Football Association rulebook, aged parchment with elegant handwriting, close-up shot, old quill pen on table",
                "Historic black-and-white team photograph, early football club players lined up in vintage uniforms, wooden football at their feet",
                "Early standardized football pitch layout on aged paper, hand-drawn field markings and measurements, close-up with vintage pen beside it"
            ]
        },
        {
            "section_number": 4,
            "section_title": "Football Goes Global",
            "narration": "As the British Empire expanded, football followed, becoming a beloved pastime across continents. British sailors, merchants, and soldiers introduced the game worldwide. South America embraced it passionately, giving rise to new playing styles that emphasized flair and creativity. In Africa and Asia, football became a unifying force amid cultural and political struggles. By the early 20th century, national football associations formed across the globe, and international competitions emerged, turning football into a universal language that transcended borders and united diverse cultures.",
            "prompt_for_image": [
                "British sailors playing football on a colonial-era dock, wooden ships in background, late afternoon light, high realism",
                "Early South American street football scene, barefoot children playing with a ragged ball, colorful houses, vibrant sunny day",
                "African football team huddled on dusty field, wearing simple uniforms, clear blue sky, happy faces, community spirit",
                "Illustration of national flags encircling a classic leather football on grass field, bright sunlight, symbolic composition",
                "Animated world map with glowing lines showing the global spread of football, connected cities, dark blue background, modern design"
            ]
        },
        {
            "section_number": 5,
            "section_title": "The Birth of the FIFA World Cup",
            "narration": "In 1930, the first FIFA World Cup was held in Uruguay, marking the dawn of football’s greatest tournament. Thirteen teams participated, and the host nation claimed victory in a thrilling final against Argentina. This historic event captured the hearts of millions, setting the stage for football’s rise as the world’s most beloved sport. Over the decades, the World Cup would produce unforgettable moments of triumph, heartbreak, and legendary performances that defined generations.",
            "prompt_for_image": [
                "Black and white image of 1930 FIFA World Cup final, packed stadium, players celebrating on field, grainy historical style",
                "Vintage poster of the first FIFA World Cup in Uruguay, bold retro typography, vibrant colors, stylized football imagery",
                "Uruguayan fans celebrating World Cup victory in crowded streets, waving flags, confetti falling, early 20th-century fashion",
                "Historic FIFA World Cup trophy placed on velvet cloth, soft spotlight, intricate metallic detailing, close-up shot",
                "Wide aerial view of Estadio Centenario stadium in 1930, filled with excited crowds, bright sunny day, historical realism"
            ]
        },
        {
            "section_number": 6,
            "section_title": "The Golden Age of Football Legends",
            "narration": "The mid-20th century ushered in football’s golden age, producing legendary figures like Pelé, Maradona, and Johan Cruyff. These players mesmerized the world with their skill, passion, and unforgettable moments on the field. From Pelé’s dazzling goals to Maradona’s famous 'Hand of God,' football became more than a sport—it became a spectacle of artistry and drama, broadcast to millions worldwide. These legends set the stage for football's enduring global appeal.",
            "prompt_for_image": [
                "Iconic image of Pelé celebrating a World Cup victory, arms raised, stadium lights glowing behind him, high detail",
                "Maradona performing the 'Hand of God' goal, mid-air handball action, intense expressions, historical accuracy",
                "Johan Cruyff executing the famous 'Cruyff Turn,' focused expression, dynamic movement captured, clear stadium background",
                "Crowded football stadium with roaring fans, waving colorful flags, golden evening light, high-energy atmosphere",
                "Vintage television showing classic black and white football broadcast, cozy living room background, nostalgic mood"
            ]
        },
        {
            "section_number": 7,
            "section_title": "Modern Football: A Billion-Dollar Industry",
            "narration": "Today, football is a billion-dollar global industry, influencing entertainment, fashion, and technology. Superstars like Messi, Ronaldo, and Mbappé dominate headlines, while massive stadiums host record-breaking crowds. Technology such as VAR and AI-driven analytics have transformed how the game is played. Despite its commercial success, football remains a simple, beautiful game that continues to unite people across cultures and generations.",
            "prompt_for_image": [
                "Lionel Messi lifting the World Cup trophy under confetti rain, golden lighting, massive stadium crowd behind him",
                "Cristiano Ronaldo performing his signature celebration, arms wide open, smiling, stadium lights shining",
                "Modern VAR room with multiple large screens reviewing a controversial goal decision, futuristic setup",
                "Gigantic modern football stadium illuminated at night, wide aerial view, filled with cheering crowds",
                "Children from diverse backgrounds playing football on a small community pitch, joyful expressions, warm afternoon light"
            ]
        },
        {
            "section_number": 8,
            "section_title": "The Future of Football",
            "narration": "Looking ahead, football continues to evolve with a focus on inclusivity, technology, and sustainability. Women’s football is reaching new heights, while AI-driven coaching and virtual reality training are reshaping how players develop skills. Football remains a powerful platform for addressing global issues like equality and environmental responsibility, ensuring its legacy as the world’s most beloved sport endures.",
            "prompt_for_image": [
                "Women's World Cup final, packed stadium, female players celebrating with trophy, colorful fireworks in background",
                "AI-driven football coaching interface, futuristic holographic display showing player stats and strategies",
                "Children from various cultures playing football together on an urban rooftop pitch, city skyline at sunset",
                "Futuristic smart stadium using sustainable energy, solar panels on roof, modern architecture, daytime scene",
                "Virtual reality football training session, young athlete wearing VR headset practicing kicks, high-tech environment"
            ]
        }
    ],
    "summary": "From ancient ceremonial games to record-breaking global spectacles, football’s history is a testament to humanity’s love for competition, community, and expression. It’s a game that transcends borders and cultures, uniting people in the joy of the beautiful game."
}
"""

CONFIG = {
    "agent_config": {
        "model_name": "qwen3:14b",
        "temperature": 0.7,
        "num_ctx": 5000
    },
    "agent_prompt_config": {
        "system_prompt": SYSTEM_PROMPT_AGENT,
    },
    "llm_model_config": {
        "model_name": "qwen3:14b",
        "temperature": 0.7,
        "num_ctx": 5000
    },
    "llm_prompt_config": {
        "system_prompt": SYSTEM_PROMPT_SCRIPT_WRITER, 
        "example_prompt": EXAMPLE_PROMPT_SCRIPT_WRITER
    },
    "image_generation_config": {
        "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
        "num_inference_steps": 20,
        "guidance_scale": 10
    }
}
