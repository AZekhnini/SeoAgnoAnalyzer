"""
Configuration file for API keys and settings.
"""

import os


class Config:
    """Application configuration"""

    # ===========================================
    # API KEYS (Required)
    # ===========================================

    # OpenAI API Key - Required for AI analysis
    # Get your key: https://platform.openai.com/api-keys
    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
        ""  # Add your key here or set as environment variable
    )

    # PageSpeed API Key - Optional (increases rate limits)
    # Get your key: https://developers.google.com/speed/docs/insights/v5/get-started
    PAGESPEED_API_KEY = os.getenv(
        "PAGESPEED_API_KEY",
        ""  # Add your key here or set as environment variable (optional)
    )

    # ===========================================
    # HELPER METHODS
    # ===========================================

    @classmethod
    def get_openai_key(cls):
        """Get OpenAI API key with validation"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not configured. "
                "Set it in config.py or as environment variable."
            )
        return cls.OPENAI_API_KEY

    @classmethod
    def get_pagespeed_key(cls):
        """Get PageSpeed API key (optional)"""
        return cls.PAGESPEED_API_KEY

    @classmethod
    def validate_required_keys(cls):
        """Check if required API keys are configured"""
        return bool(cls.OPENAI_API_KEY)

    @classmethod
    def print_status(cls):
        """Print configuration status"""
        print("\nAPI Configuration Status:")
        print(f"{'[OK]' if cls.OPENAI_API_KEY else '[ERROR]'} OpenAI API Key: {'Configured' if cls.OPENAI_API_KEY else 'Not configured'}")
        print(f"{'[OK]' if cls.PAGESPEED_API_KEY else '[SKIP]'} PageSpeed API Key: {'Configured' if cls.PAGESPEED_API_KEY else 'Not configured (optional)'}")


if __name__ == "__main__":
    Config.print_status()
