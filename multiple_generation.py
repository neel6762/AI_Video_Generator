"""Pass a list of user prompts to the agent and generate multiple videos."""

from agent import invoke_agent

user_prompts = [
    "A documentary about the history of the iPhone",
    "A documentary about the beauty of nature",
    "Different cuisines of the world",
    "Different festivals celebrated in India - along with the history and traditions associated with them.",
]

for user_prompt in user_prompts:
    print(f"\nGenerating video for prompt: {user_prompt}\n")
    agent = invoke_agent(user_prompt)
    agent.invoke({"input": user_prompt})
    print("==" * 60)