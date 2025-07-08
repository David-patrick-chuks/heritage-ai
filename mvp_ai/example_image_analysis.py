#!/usr/bin/env python3
"""
Example: AI Image Analysis for Cultural Design Elements
Demonstrates how HeritageAI analyzes actual images to extract design elements
"""

import os
import json
from ai_culture_generator import ai_culture_generator

def analyze_cultural_image(culture: str, image_path: str):
    """Analyze a cultural design image and extract design elements"""
    
    print(f"🎨 HeritageAI Image Analysis Example")
    print(f"Culture: {culture}")
    print(f"Image: {image_path}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        print("💡 Please provide a valid image path")
        return
    
    try:
        # Generate comprehensive metadata from image analysis
        print("🤖 Analyzing image with AI...")
        metadata = ai_culture_generator.generate_culture_metadata(culture, image_path)
        
        # Display results
        print(f"\n✅ Analysis Results:")
        print(f"📝 Culture: {metadata.get('culture')}")
        print(f"📷 Source Image: {metadata.get('source_image')}")
        
        # Fonts
        fonts = metadata.get('fonts', [])
        print(f"\n🎨 Recommended Fonts ({len(fonts)}):")
        for i, font in enumerate(fonts, 1):
            print(f"   {i}. {font}")
        
        # Elements
        elements = metadata.get('elements', [])
        print(f"\n🎯 Design Elements ({len(elements)}):")
        for element in elements:
            print(f"   • {element.get('name')} ({element.get('type')})")
            print(f"     {element.get('description')}")
        
        # Colors
        colors = metadata.get('colors', [])
        print(f"\n🌈 Color Palette ({len(colors)}):")
        for i, color in enumerate(colors, 1):
            print(f"   {i}. {color}")
        
        # Patterns
        patterns = metadata.get('patterns', [])
        print(f"\n📐 Patterns ({len(patterns)}):")
        for pattern in patterns:
            print(f"   • {pattern.get('name')} ({pattern.get('style')})")
            print(f"     {pattern.get('description')[:100]}...")
        
        # Brief
        brief = metadata.get('brief', {})
        print(f"\n📋 Design Brief:")
        print(f"   Cultural Context: {brief.get('cultural_context', 'N/A')[:100]}...")
        print(f"   Design Principles: {brief.get('design_principles', 'N/A')[:100]}...")
        
        # Save results
        output_file = f"{culture}_image_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis saved to: {output_file}")
        
        return metadata
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

def main():
    """Main example function"""
    
    # Example usage
    print("🎨 HeritageAI - Image Analysis Example")
    print("=" * 50)
    
    # You can replace these with your own image paths
    examples = [
        {
            "culture": "yoruba",
            "image": "assets/yoruba_pattern_1.png"
        },
        {
            "culture": "celtic", 
            "image": "assets/celtic_pattern_1.png"
        }
    ]
    
    for example in examples:
        if os.path.exists(example["image"]):
            print(f"\n📷 Analyzing {example['culture']} image...")
            analyze_cultural_image(example["culture"], example["image"])
        else:
            print(f"\n⚠️ Image not found: {example['image']}")
            print("💡 Generate images first using:")
            print(f"   python main.py generate --culture {example['culture']} --count 1")
    
    print(f"\n🎉 Example completed!")
    print("💡 The AI analyzes actual images to extract authentic design elements")
    print("   instead of using predefined data mappings.")

if __name__ == "__main__":
    main() 