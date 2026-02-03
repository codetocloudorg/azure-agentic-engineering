"""
Agent with Custom Tools Example

This example demonstrates how to create an agent with custom tools that can
perform actions like searching documents and creating summaries.

Prerequisites:
    pip install agent-framework --pre azure-identity azure-search-documents

Environment Variables:
    AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
    AZURE_SEARCH_ENDPOINT: Your Azure AI Search endpoint
    AZURE_SEARCH_INDEX: Your search index name
"""

import asyncio
import os
import logging
from typing import Optional
from datetime import datetime

from agent_framework import Agent
from agent_framework.tools import function_tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize credential
credential = DefaultAzureCredential()


# =============================================================================
# Custom Tools
# =============================================================================

@function_tool
def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        Current date and time in ISO format
    """
    return datetime.now().isoformat()


@function_tool
def search_documents(
    query: str,
    top: int = 5
) -> list[dict]:
    """
    Search the document index for relevant information.
    
    Args:
        query: The search query
        top: Maximum number of results to return
        
    Returns:
        List of matching documents with title and content
    """
    endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
    index_name = os.environ.get("AZURE_SEARCH_INDEX")
    
    if not endpoint or not index_name:
        return [{"error": "Search not configured"}]
    
    try:
        client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=credential
        )
        
        results = client.search(
            search_text=query,
            top=top,
            select=["title", "content", "url"]
        )
        
        return [
            {
                "title": doc.get("title", "Untitled"),
                "content": doc.get("content", "")[:500],
                "url": doc.get("url", "")
            }
            for doc in results
        ]
    except Exception as e:
        logger.error(f"Search error: {e}")
        return [{"error": str(e)}]


@function_tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression (e.g., "2 + 2 * 3")
        
    Returns:
        The result of the calculation
    """
    # Only allow safe operations
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Invalid characters in expression"
    
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@function_tool
def create_summary(
    text: str,
    max_sentences: int = 3
) -> str:
    """
    Create a brief summary of the provided text.
    
    Args:
        text: The text to summarize
        max_sentences: Maximum number of sentences in summary
        
    Returns:
        A brief summary of the text
    """
    # Simple extractive summary (first N sentences)
    sentences = text.replace("!", ".").replace("?", ".").split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    summary_sentences = sentences[:max_sentences]
    return ". ".join(summary_sentences) + "."


# =============================================================================
# Agent Configuration
# =============================================================================

async def create_tool_agent():
    """Create an agent with custom tools."""
    
    instructions = """You are a helpful research assistant with access to tools.

Available tools:
1. get_current_time: Get the current date and time
2. search_documents: Search the knowledge base for information
3. calculate: Perform mathematical calculations
4. create_summary: Summarize text content

Guidelines:
- Use search_documents when users ask about specific topics
- Use calculate for any math operations
- Always cite sources when using search results
- Be concise and accurate
"""
    
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="ResearchAssistant",
        instructions=instructions,
        tools=[
            get_current_time,
            search_documents,
            calculate,
            create_summary,
        ]
    )
    
    return agent


async def demo():
    """Demonstrate the agent with tools."""
    agent = await create_tool_agent()
    
    # Demo queries
    queries = [
        "What time is it?",
        "What is 15% of 250?",
        "Search for information about Azure AI services",
    ]
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print("=" * 50)
        
        response = await agent.run(query)
        print(f"Response: {response}")


async def interactive():
    """Interactive mode with tool-enabled agent."""
    agent = await create_tool_agent()
    
    print("\n" + "=" * 50)
    print("Research Assistant (with Tools)")
    print("Available: time, search, calculate, summarize")
    print("Type 'quit' to exit")
    print("=" * 50 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                break
            
            if not user_input:
                continue
            
            response = await agent.run(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo())
    else:
        asyncio.run(interactive())
