#!/usr/bin/env python3
"""
Test script for HeritageAI image generation with new settings:
- Default 4 images per generation
- Consistent aspect ratios
- Improved prompts
"""

import os
import sys
from imagegen_gemini import generate_pattern_image
from gemini_client import gemini_client

def test_single_generation():
    """Test generating 4 images for a single culture"""
    print("🎨 Testing single culture generation (4 images)...")
    
    culture = "Igbo"
    try:
        result = generate_pattern_image(
            culture=culture,
            sample_count=4,
            aspect_ratio="1:1"
        )
        
        if result:
            print(f"✅ Successfully generated {len(result)} images for {culture}")
            for i, image_path in enumerate(result, 1):
                print(f"   {i}. {os.path.basename(image_path)}")
                if os.path.exists(image_path):
                    file_size = os.path.getsize(image_path)
                    print(f"      Size: {file_size:,} bytes")
                else:
                    print(f"      ⚠️ File not found")
        else:
            print("❌ Generation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_different_aspect_ratios():
    """Test different aspect ratios"""
    print("\n📐 Testing different aspect ratios...")
    
    aspect_ratios = ["1:1", "4:3", "16:9"]
    culture = "edo"
    
    for ratio in aspect_ratios:
        print(f"  Testing {ratio} aspect ratio...")
        try:
            result = generate_pattern_image(
                culture=culture,
                sample_count=1,  # Just 1 for testing
                aspect_ratio=ratio
            )
            
            if result:
                image_path = result[0] if isinstance(result, list) else result
                print(f"    ✅ Generated: {os.path.basename(image_path)}")
            else:
                print(f"    ❌ Failed")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")

def test_multiple_runs():
    """Test running generation 3 times to get 12 total images"""
    print("\n🔄 Testing multiple runs (3 runs × 4 images = 12 total)...")
    
    culture = "maori"
    total_images = 0
    
    for run in range(1, 4):
        print(f"  Run {run}/3...")
        try:
            result = generate_pattern_image(
                culture=culture,
                sample_count=4,
                aspect_ratio="1:1"
            )
            
            if result:
                run_count = len(result)
                total_images += run_count
                print(f"    ✅ Generated {run_count} images (Total: {total_images})")
            else:
                print(f"    ❌ Run {run} failed")
                
        except Exception as e:
            print(f"    ❌ Error in run {run}: {e}")
    
    print(f"\n📊 Summary: Generated {total_images} total images across 3 runs")

def test_improved_prompts():
    """Test the improved prompts for better consistency"""
    print("\n✨ Testing improved prompts...")
    
    cultures = ["yoruba", "edo", "maori"]
    
    for culture in cultures:
        print(f"  Testing {culture} with improved prompt...")
        try:
            result = generate_pattern_image(
                culture=culture,
                sample_count=1,  # Just 1 for testing
                aspect_ratio="1:1"
            )
            
            if result:
                image_path = result[0] if isinstance(result, list) else result
                print(f"    ✅ Generated: {os.path.basename(image_path)}")
            else:
                print(f"    ❌ Failed")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 HeritageAI Image Generation Test Suite")
    print("=" * 50)
    
    # Check if assets directory exists
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"📁 Created assets directory: {assets_dir}")
    
    # Run tests
    test_single_generation()
    test_different_aspect_ratios()
    test_multiple_runs()
    test_improved_prompts()
    
    print("\n🎉 Test suite completed!")
    print("💡 You can now run:")
    print("   python main.py generate --culture yoruba")
    print("   (This will generate 4 images by default)")

if __name__ == "__main__":
    main() 