"""
Multi-Agent Workflow Example

This example demonstrates how to create a multi-agent workflow where
specialized agents collaborate to complete complex tasks.

Prerequisites:
    pip install agent-framework --pre azure-identity

Environment Variables:
    AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
"""

import asyncio
import os
import logging
from dataclasses import dataclass
from typing import Optional

from agent_framework import Agent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

credential = DefaultAzureCredential()


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class WorkflowContext:
    """Shared context between agents."""
    original_request: str
    plan: Optional[str] = None
    research: Optional[str] = None
    draft: Optional[str] = None
    final_output: Optional[str] = None


# =============================================================================
# Specialized Agents
# =============================================================================

def create_planner_agent():
    """Create a planning agent that breaks down tasks."""
    return AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="Planner",
        instructions="""You are a strategic planning agent.

Your role:
1. Analyze the user's request
2. Break it down into clear, actionable steps
3. Identify what information needs to be gathered
4. Create a structured plan

Output format:
- GOAL: One sentence summary
- STEPS: Numbered list of actions
- REQUIREMENTS: What information is needed
- SUCCESS CRITERIA: How to know when done
"""
    )


def create_researcher_agent():
    """Create a research agent that gathers information."""
    return AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="Researcher",
        instructions="""You are a thorough research agent.

Your role:
1. Gather relevant information for the task
2. Find best practices and examples
3. Identify potential challenges
4. Compile findings in a structured format

Output format:
- KEY FINDINGS: Bullet points of important information
- BEST PRACTICES: Recommended approaches
- CONSIDERATIONS: Things to keep in mind
- SOURCES: Where information came from (if applicable)
"""
    )


def create_writer_agent():
    """Create a writing agent that produces content."""
    return AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="Writer",
        instructions="""You are a skilled content creation agent.

Your role:
1. Take the plan and research as input
2. Create well-structured, clear content
3. Ensure accuracy and completeness
4. Format appropriately for the audience

Guidelines:
- Be concise but thorough
- Use clear headings and structure
- Include code examples when relevant
- Maintain professional tone
"""
    )


def create_reviewer_agent():
    """Create a review agent that validates output."""
    return AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="Reviewer",
        instructions="""You are a quality assurance agent.

Your role:
1. Review the draft content
2. Check for accuracy and completeness
3. Suggest improvements
4. Provide final polished version

Output format:
- ASSESSMENT: Overall quality evaluation
- IMPROVEMENTS MADE: What was enhanced
- FINAL VERSION: The polished content
"""
    )


# =============================================================================
# Workflow Orchestration
# =============================================================================

async def run_workflow(request: str) -> str:
    """
    Run the multi-agent workflow.
    
    Args:
        request: The user's request
        
    Returns:
        The final output from the workflow
    """
    context = WorkflowContext(original_request=request)
    
    # Phase 1: Planning
    logger.info("Phase 1: Planning")
    planner = create_planner_agent()
    context.plan = await planner.run(
        f"Create a plan for: {request}"
    )
    print(f"\n📋 PLAN:\n{context.plan}\n")
    
    # Phase 2: Research
    logger.info("Phase 2: Research")
    researcher = create_researcher_agent()
    context.research = await researcher.run(
        f"""Based on this plan:
{context.plan}

Research the following request:
{request}"""
    )
    print(f"\n🔍 RESEARCH:\n{context.research}\n")
    
    # Phase 3: Writing
    logger.info("Phase 3: Writing")
    writer = create_writer_agent()
    context.draft = await writer.run(
        f"""Using this plan:
{context.plan}

And this research:
{context.research}

Create content for:
{request}"""
    )
    print(f"\n✏️ DRAFT:\n{context.draft}\n")
    
    # Phase 4: Review
    logger.info("Phase 4: Review")
    reviewer = create_reviewer_agent()
    context.final_output = await reviewer.run(
        f"""Review and improve this draft:
{context.draft}

Original request was:
{request}"""
    )
    print(f"\n✅ FINAL:\n{context.final_output}\n")
    
    return context.final_output


async def demo():
    """Demonstrate the multi-agent workflow."""
    request = """
    Create a guide for deploying an Azure AI agent to production.
    Include security best practices and monitoring recommendations.
    """
    
    print("=" * 60)
    print("MULTI-AGENT WORKFLOW DEMO")
    print("=" * 60)
    print(f"\nRequest: {request.strip()}\n")
    
    result = await run_workflow(request)
    
    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETE")
    print("=" * 60)


async def interactive():
    """Interactive mode for the workflow."""
    print("\n" + "=" * 60)
    print("MULTI-AGENT WORKFLOW")
    print("Enter a complex task and watch the agents collaborate")
    print("Type 'quit' to exit")
    print("=" * 60 + "\n")
    
    while True:
        try:
            request = input("Your request: ").strip()
            
            if request.lower() in ["quit", "exit", "q"]:
                break
            
            if not request:
                continue
            
            await run_workflow(request)
            
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo())
    else:
        asyncio.run(interactive())
