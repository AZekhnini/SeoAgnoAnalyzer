"""
Input Classifier Agent
Intelligent agent that detects input type (URL, HTML, or Screenshot) and routes to appropriate workflow.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.instructions.classifier_instructions import CLASSIFIER_INSTRUCTIONS


# Input Classifier Agent
input_classifier = Agent(
    name="Input Classifier",
    model=OpenAIChat(id="gpt-4o-mini"),  # Fast, efficient for classification
    instructions=CLASSIFIER_INSTRUCTIONS,
    markdown=False,  # We want JSON output, not markdown
    description=(
        "Intelligent classifier that analyzes user input and determines whether "
        "it's a URL, raw HTML, screenshot path/data, or unknown format. Routes "
        "input to the appropriate analysis workflow."
    ),
)
