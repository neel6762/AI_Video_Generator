from langchain_core.tools import tool
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage, HumanMessage
import utils
from config import CONFIG


def invoke_agent(user_prompt: str):
    """Initialize the agent with the tools and the model

    :return: agent
    """
    tools = [utils.generate_video_script, utils.generate_visuals, utils.generate_audio_from_script, utils.assemble_video]

    agentModel = OllamaLLM(
        model=CONFIG["agent_config"]["model_name"],
        temperature = CONFIG["agent_config"]["temperature"]
    )

    user_prompt = """
    # User Prompt 
    {user_prompt}

    # Example
    - The user wants to create a video about {user_prompt}
    - Let me check all the tools available to me and execute them one by one to generate the video
    - I see there is a tool called **generate_video_script** that can generate a video script from the user prompt
    <tool_call>
    - Next, I need to call the tool **generate_visuals** that can generate visuals from the video script
    </tool_call>
    - After that, I need to call the tool **generate_audio_from_script** that can generate audio from the video script
    </tool_call>
    - Finally, I need to call the tool **assemble_video** that can assemble the video from the visuals, audio, and script
    </tool_call>
    """

    messages = [
        SystemMessage(content=[{"type": "text", "text": CONFIG["agent_prompt_config"]["system_prompt"]}]),
        HumanMessage(content=[{"type": "text", "text": user_prompt}]),
    ]

    agent = initialize_agent(
        tools=tools,
        llm=agentModel,
        prompt=messages,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent


if __name__ == "__main__":

    user_prompt = input("Enter your prompt to generate a video: ").strip()
    agent = invoke_agent(user_prompt)
    agent.invoke({"input": user_prompt})
    