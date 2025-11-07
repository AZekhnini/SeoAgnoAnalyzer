"""
Technical Performance Analysis Agent
Configures the performance analyst agent with specialized instructions.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.instructions.performance_instructions import PERFORMANCE_ANALYST_INSTRUCTIONS


def create_performance_analyst(model_id: str = "gpt-4o-mini") -> Agent:
    """
    Create and configure the Technical Performance Analysis Agent.

    Args:
        model_id: The OpenAI model ID to use (default: gpt-4o-mini)

    Returns:
        Configured Agent instance
    """

    performance_analyst = Agent(
        name="Technical Performance Analyst",
        model=OpenAIChat(id=model_id),
        instructions=PERFORMANCE_ANALYST_INSTRUCTIONS,
        markdown=True,
        description="Expert in web performance optimization, Core Web Vitals, and technical SEO",
    )

    return performance_analyst


# Create default instance
performance_analyst = create_performance_analyst()
