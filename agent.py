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
    tools = [utils.generate_video_script, utils.generate_visuals]

    agentModel = OllamaLLM(
        model=CONFIG["agent_config"]["model_name"],
        temperature = CONFIG["agent_config"]["temperature"]
    )

    messages = [
        SystemMessage(content=[{"type": "text", "text": CONFIG["agent_prompt_config"]["system_prompt"]}]),
        HumanMessage(content=[{"type": "text", "text": user_prompt}]),
    ]

    agent = initialize_agent(
        tools=tools,
        llm=agentModel,
        prompt=messages,
        verbose=True
    )
    
    return agent


if __name__ == "__main__":

    user_prompt = "Advertising campaign for a pizza shop"
    agent = invoke_agent(user_prompt)
    