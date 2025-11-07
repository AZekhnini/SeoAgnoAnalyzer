"""
Summary Analyst Agent
Expert agent for synthesizing SEO, Performance, and UI/UX analyses into actionable insights.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.instructions.summary_instructions import SUMMARY_ANALYST_INSTRUCTIONS


# Summary Analyst Agent
summary_analyst = Agent(
    name="Website Analyst",
    model=OpenAIChat(id="gpt-4o-mini"),  # Text-based analysis is sufficient
    instructions=SUMMARY_ANALYST_INSTRUCTIONS,
    markdown=True,
    description=(
        "Expert website analyst specializing in synthesizing comprehensive analysis "
        "reports. Combines SEO, Performance, and UI/UX findings into actionable "
        "recommendations and executive summaries."
    ),
)
