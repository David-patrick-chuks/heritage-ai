#!/usr/bin/env python3
"""
test_ai_culture.py - Test script for AI Culture Generator
Demonstrates how AI can generate culture-specific design elements from image analysis.
"""
import json
import os
import logging
from typing import Optional, Dict, Any
from ai_culture_generator import ai_culture_generator

logger = logging.getLogger(__name__)


def test_culture_generation(culture_name: str, image_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Test AI generation for a specific culture.
    Args:
        culture_name (str): The culture to test.
        image_path (Optional[str]): Path to the image file.
    Returns:
        Optional[Dict[str, Any]]: Generated metadata or None if failed.
    """
    logger.info(f"\n🤖 Testing AI Culture Generator for: {culture_name}")
    if image_path:
        logger.info(f"📷 Using image: {image_path}")
    else:
        logger.warning("⚠️ No image provided - will use fallback data")
    logger.info("=" * 60)
    try:
        logger.info("📊 Generating comprehensive culture metadata...")
        if image_path and os.path.exists(image_path):
            metadata = ai_culture_generator.generate_culture_metadata(culture_name, image_path)
        else:
            logger.error("❌ No valid image provided - cannot test image analysis")
            return None
        logger.info(f"\n✅ Generated metadata for {culture_name}:")
        logger.info(f"   📝 Culture: {metadata.get('culture', 'N/A')}")
        logger.info(f"   🎨 Fonts ({len(metadata.get('fonts', []))}): {', '.join(metadata.get('fonts', [])[:3])}")
        logger.info(f"   🎯 Elements ({len(metadata.get('elements', []))}):")
        for element in metadata.get('elements', [])[:2]:
            logger.info(f"      - {element.get('name', 'N/A')} ({element.get('type', 'N/A')}): {element.get('description', 'N/A')}")
        logger.info(f"   🌈 Colors ({len(metadata.get('colors', []))}): {', '.join(metadata.get('colors', [])[:3])}")
        logger.info(f"   📐 Patterns ({len(metadata.get('patterns', []))}):")
        for pattern in metadata.get('patterns', [])[:2]:
            logger.info(f"      - {pattern.get('name', 'N/A')} ({pattern.get('style', 'N/A')}): {pattern.get('description', 'N/A')[:50]}...")
        brief = metadata.get('brief', {})
        logger.info(f"   📋 Design Brief:")
        logger.info(f"      - Cultural Context: {brief.get('cultural_context', 'N/A')[:80]}...")
        logger.info(f"      - Design Principles: {brief.get('design_principles', 'N/A')[:80]}...")
        filename = f"{culture_name}_ai_metadata.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        logger.info(f"\n💾 Metadata saved to: {filename}")
        return metadata
    except Exception as e:
        logger.error(f"❌ Error generating metadata for {culture_name}: {e}")
        return None

def test_individual_components(culture_name: str, image_path: Optional[str] = None) -> None:
    """
    Test individual AI generation components.
    Args:
        culture_name (str): The culture to test.
        image_path (Optional[str]): Path to the image file.
    """
    logger.info(f"\n🔧 Testing individual components for: {culture_name}")
    logger.info("-" * 40)
    if not image_path or not os.path.exists(image_path):
        logger.error("❌ No valid image provided - cannot test image analysis components")
        return
    try:
        fonts = ai_culture_generator.generate_culture_fonts(culture_name, image_path)
        logger.info(f"✅ Fonts: {', '.join(fonts)}")
    except Exception as e:
        logger.error(f"❌ Fonts error: {e}")
    try:
        elements = ai_culture_generator.generate_culture_elements(culture_name, image_path)
        logger.info(f"✅ Elements: {len(elements)} generated")
        for element in elements[:2]:
            logger.info(f"   - {element.get('name')} ({element.get('type')})")
    except Exception as e:
        logger.error(f"❌ Elements error: {e}")
    try:
        colors = ai_culture_generator.generate_culture_colors(culture_name, image_path)
        logger.info(f"✅ Colors: {', '.join(colors[:3])}")
    except Exception as e:
        logger.error(f"❌ Colors error: {e}")
    try:
        patterns = ai_culture_generator.generate_culture_patterns(culture_name, image_path)
        logger.info(f"✅ Patterns: {len(patterns)} generated")
        for pattern in patterns[:2]:
            logger.info(f"   - {pattern.get('name')} ({pattern.get('style')})")
    except Exception as e:
        logger.error(f"❌ Patterns error: {e}")

def main() -> None:
    """
    Main test function for AI Culture Generator.
    """
    logger.info("🎨 HeritageAI - AI Culture Generator Test (Image Analysis)")
    logger.info("=" * 60)
    test_image = "assets/yoruba_pattern_imagen4.png"  # Example image path
    if not os.path.exists(test_image):
        logger.error(f"❌ Test image not found: {test_image}")
        logger.info("💡 Please generate some images first using:")
        logger.info("   python main.py generate --culture yoruba --count 1")
        logger.info("   Then update the test_image path in this script")
        return
    culture = "yoruba"
    metadata = test_culture_generation(culture, test_image)
    test_individual_components(culture, test_image)
    logger.info("\n" + "="*60)
    logger.info("\n🎉 AI Culture Generator test completed!")
    logger.info("💡 The system now uses AI image analysis to generate authentic culture-specific design elements")
    logger.info("   based on actual visual content instead of predefined data mappings.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    main() 