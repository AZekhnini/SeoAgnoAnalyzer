"""
SEO Analysis Agent
Defines the agent responsible for analyzing SEO features.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.instructions.seo_instructions import SEO_ANALYST_INSTRUCTIONS


def create_seo_analyst(model_id: str = "gpt-4o-mini") -> Agent:
    """
    Create and configure the SEO Analysis Agent.

    Args:
        model_id: The OpenAI model ID to use (default: gpt-4o-mini)

    Returns:
        Configured Agent instance for SEO analysis
    """
    seo_analyst = Agent(
        name = "SEO Analyst",
        model = OpenAIChat(id=model_id),
        instructions = SEO_ANALYST_INSTRUCTIONS,
        markdown = True,
    )

    return seo_analyst


# Create default instance
seo_analyst = create_seo_analyst()
