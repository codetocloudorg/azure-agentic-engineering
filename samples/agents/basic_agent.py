"""
Basic Agent Example using Microsoft Agent Framework

This example demonstrates how to create a simple agent that can respond to user queries
using Azure OpenAI.

Prerequisites:
    pip install agent-framework --pre azure-identity

Environment Variables:
    AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
    AZURE_OPENAI_DEPLOYMENT: Your model deployment name (e.g., gpt-4o)
"""

import asyncio
import os
import logging
from typing import Optional

from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def create_agent(
    name: str = "AssistantBot",
    instructions: Optional[str] = None
):
    """
    Create an agent using Azure OpenAI.
    
    Args:
        name: The name of the agent
        instructions: Custom instructions for the agent
        
    Returns:
        Configured agent instance
    """
    default_instructions = """You are a helpful AI assistant specialized in Azure services.
    
    Guidelines:
    1. Provide accurate, up-to-date information about Azure
    2. Include code examples when appropriate
    3. Recommend best practices for security and cost optimization
    4. If unsure, acknowledge uncertainty rather than guessing
    """
    
    # Use managed identity for authentication
    credential = DefaultAzureCredential()
    
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        credential=credential,
    ).as_agent(
        name=name,
        instructions=instructions or default_instructions,
    )
    
    logger.info(f"Created agent: {name}")
    return agent


async def chat_loop(agent):
    """
    Interactive chat loop with the agent.
    
    Args:
        agent: The agent to chat with
    """
    print("\n" + "=" * 50)
    print("Azure AI Assistant")
    print("Type 'quit' to exit")
    print("=" * 50 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            logger.info(f"Processing query: {user_input[:50]}...")
            
            response = await agent.run(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"An error occurred: {e}")


async def main():
    """Main entry point."""
    # Validate environment
    required_vars = ["AZURE_OPENAI_ENDPOINT"]
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        logger.error(f"Missing environment variables: {missing}")
        print(f"Please set the following environment variables: {missing}")
        print("\nExample:")
        print("  export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com")
        return
    
    # Create and run agent
    agent = await create_agent()
    await chat_loop(agent)


if __name__ == "__main__":
    asyncio.run(main())
