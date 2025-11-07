"""
UI/UX Analyst Agent
Expert agent for analyzing visual design, user experience, and accessibility.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.instructions.uiux_instructions import UIUX_ANALYSIS_INSTRUCTIONS


# UI/UX Analyst Agent with Vision Capabilities
uiux_analyst = Agent(
    name="UI/UX Analyst",
    model=OpenAIChat(id="gpt-4o"),  # Vision-capable model
    instructions=UIUX_ANALYSIS_INSTRUCTIONS,
    markdown=True,
    description=(
        "Expert UI/UX analyst specializing in visual design, user experience, "
        "accessibility, and modern web design practices. Analyzes screenshots "
        "and accessibility data to provide comprehensive UI/UX insights."
    ),
)
