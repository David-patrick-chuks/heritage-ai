#!/usr/bin/env python3
"""
test_retry.py - Test script for Gemini client retry logic and multiple API keys.
"""
from gemini_client import gemini_client
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)

def test_api_key_loading() -> None:
    """
    Test that API keys are loaded correctly.
    """
    logger.info("🔑 Testing API key loading...")
    logger.info(f"Number of API keys loaded: {len(gemini_client.api_keys)}")
    for i, key in enumerate(gemini_client.api_keys):
        # Show first 10 characters of each key for verification
        masked_key = key[:10] + "..." if len(key) > 10 else key
        logger.info(f"  Key {i+1}: {masked_key}")
    logger.info("")

def test_text_generation() -> None:
    """
    Test text generation with retry logic.
    """
    logger.info("📝 Testing text generation...")
    try:
        result = gemini_client.generate_text("Say 'Hello from HeritageAI' in one sentence.")
        logger.info(f"✅ Text generation successful: {result}")
    except Exception as e:
        logger.error(f"❌ Text generation failed: {e}")
    logger.info("")

def test_image_generation() -> None:
    """
    Test image generation with retry logic.
    """
    logger.info("🖼️ Testing image generation...")
    try:
        result = gemini_client.generate_image(
            prompt="A simple geometric pattern with 3 colors",
            sample_count=1,
            filename="test_pattern.png"
        )
        logger.info(f"✅ Image generation successful: {result}")
    except Exception as e:
        logger.error(f"❌ Image generation failed: {e}")
    logger.info("")

def test_error_handling() -> None:
    """
    Test error handling with invalid API key.
    """
    logger.info("🧪 Testing error handling...")
    
    # Temporarily set an invalid key
    original_keys = gemini_client.api_keys.copy()
    gemini_client.api_keys = ["invalid_key_for_testing"]
    gemini_client.current_key_index = 0
    
    try:
        result = gemini_client.generate_text("This should fail")
        logger.warning(f"Unexpected success: {result}")
    except Exception as e:
        logger.info(f"✅ Error handling working: {type(e).__name__}: {e}")
    
    # Restore original keys
    gemini_client.api_keys = original_keys
    gemini_client.current_key_index = 0
    logger.info("")

def main() -> None:
    """
    Run all tests for Gemini client retry logic and error handling.
    """
    logger.info("🚀 HeritageAI Gemini Client Test Suite")
    logger.info("=" * 50)
    
    test_api_key_loading()
    test_text_generation()
    test_image_generation()
    test_error_handling()
    
    logger.info("✅ Test suite completed!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    main() 