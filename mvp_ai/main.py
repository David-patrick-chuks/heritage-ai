"""
main.py - HeritageAI CLI and orchestration module

Provides command-line tools for generating, analyzing, and exporting culturally-inspired design assets using AI models.
"""
import os
import argparse
import json
import logging
import datetime
from typing import Any, Dict, Optional
from clip_model import generate_pattern_and_palette, score_image_with_prompt
from gemini_notes import generate_cultural_note
from imagegen_gemini import generate_pattern_image
from color_palette import extract_palette
from export_formats import export_kit_formats
from ai_culture_generator import ai_culture_generator

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Default cultures for examples, but any culture can be used
DEFAULT_CULTURES = ['yoruba', 'edo', 'maori']
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

def cli_generate(args: argparse.Namespace) -> None:
    """Generate pattern images and color palettes for a culture."""
    culture: str = args.culture
    sample_count: int = args.count
    aspect_ratio: str = args.aspect_ratio
    logger.info(f"Generating {sample_count} pattern image(s) for {culture.title()} with aspect ratio {aspect_ratio}...")
    image_result = generate_pattern_image(culture, sample_count=sample_count, aspect_ratio=aspect_ratio)
    if image_result:
        image_paths = [image_result] if isinstance(image_result, str) else image_result
        for idx, image_path in enumerate(image_paths, 1):
            logger.info(f"Pattern image {idx} generated and saved to: {image_path}")
            palette, palette_json = extract_palette(image_path)
            logger.info(f"Extracted color palette: {palette}")
            logger.info(f"Palette JSON saved to: {palette_json}")
    else:
        logger.error("Pattern image generation failed.")

def cli_palette(args: argparse.Namespace) -> None:
    """Extract color palettes for all PNG images in the assets directory."""
    logger.info("Extracting palettes for all PNG images in assets/...")
    for fname in os.listdir(ASSETS_DIR):
        if fname.endswith('.png'):
            img_path = os.path.join(ASSETS_DIR, fname)
            palette, palette_json = extract_palette(img_path)
            logger.info(f"{fname}: {palette} (saved to {palette_json})")

def cli_brief(args: argparse.Namespace) -> None:
    """Generate cultural notes for all PNG images in the assets directory."""
    logger.info("Generating cultural notes for all PNG images in assets/...")
    for fname in os.listdir(ASSETS_DIR):
        if fname.endswith('.png'):
            culture = fname.split('_')[0]
            note = generate_cultural_note(culture)
            note_path = os.path.join(ASSETS_DIR, f"{culture}_note.txt")
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(note)
            logger.info(f"{fname}: note saved to {note_path}")

def cli_bundle(args: argparse.Namespace) -> None:
    """Bundle image, palette, and note for each PNG in the assets directory."""
    logger.info("Bundling image, palette, and note for each PNG in assets/...")
    for fname in os.listdir(ASSETS_DIR):
        if fname.endswith('.png'):
            base = os.path.splitext(fname)[0]
            culture = base.split('_')[0]
            img_path = os.path.join(ASSETS_DIR, fname)
            palette_path = os.path.join(ASSETS_DIR, f"{base}_palette.json")
            note_path = os.path.join(ASSETS_DIR, f"{culture}_note.txt")
            bundle: Dict[str, Any] = {"image": fname}
            if os.path.exists(palette_path):
                with open(palette_path) as f:
                    bundle["palette"] = json.load(f)["palette"]
            if os.path.exists(note_path):
                with open(note_path, encoding='utf-8') as f:
                    bundle["note"] = f.read().strip()
            bundle_path = os.path.join(ASSETS_DIR, f"{base}_bundle.json")
            with open(bundle_path, 'w', encoding='utf-8') as f:
                json.dump(bundle, f, indent=2)
            logger.info(f"Bundle saved to {bundle_path}")

def cli_clip_score(args: argparse.Namespace) -> None:
    """Score all PNG images in the assets directory against a prompt using CLIP."""
    prompt: str = args.prompt
    logger.info(f"Scoring all PNG images in assets/ against prompt: '{prompt}'")
    for fname in os.listdir(ASSETS_DIR):
        if fname.endswith('.png'):
            img_path = os.path.join(ASSETS_DIR, fname)
            try:
                score = score_image_with_prompt(img_path, prompt)
                logger.info(f"{fname}: score = {score}")
            except Exception as e:
                logger.error(f"{fname}: error scoring image: {e}")

def cli_generate_kit(args: argparse.Namespace) -> None:
    """Generate a complete design kit for a culture using AI image analysis."""
    culture: str = args.culture
    logger.info(f"🎨 Generating AI-powered design kit for {culture} culture...")
    kit_dir = os.path.join(ASSETS_DIR, f"{culture}_kit")
    os.makedirs(kit_dir, exist_ok=True)
    patterns = []
    palettes = []
    from gemini_client import gemini_client
    try:
        culture_details = gemini_client.generate_culture_details(culture)
        clip_prompt = f"{culture.title()} {culture_details}"
    except Exception as e:
        logger.warning(f"Could not generate culture details for CLIP: {e}")
        clip_prompt = f"{culture.title()} textile pattern, authentic cultural motifs"
    pattern_metadata = []
    for i in range(3):
        logger.info(f"  Generating pattern {i+1}/3...")
        try:
            unique_filename = f"{culture}_pattern_{i+1}.png"
            image_result = generate_pattern_image(culture, filename=unique_filename, sample_count=4, aspect_ratio="1:1")
            if image_result:
                image_paths = image_result if isinstance(image_result, list) else [image_result]
                for idx, pattern_path in enumerate(image_paths):
                    patterns.append(pattern_path)
                    if not os.path.exists(pattern_path):
                        logger.warning(f"File does not exist: {pattern_path}")
                    try:
                        palette_colors, palette_path = extract_palette(pattern_path)
                        palettes.append({
                            "colors": palette_colors,
                            "source_image": os.path.basename(pattern_path),
                            "note": f"Color palette extracted from {culture} pattern {idx+1}"
                        })
                    except Exception as e:
                        logger.error(f"Error extracting palette: {e}")
                    try:
                        clip_score = score_image_with_prompt(pattern_path, clip_prompt)
                        logger.info(f"CLIP score: {clip_score:.3f} for {os.path.basename(pattern_path)}")
                    except Exception as e:
                        logger.error(f"Error scoring with CLIP: {e}")
                        clip_score = None
                    pattern_metadata.append({
                        "image": os.path.basename(pattern_path),
                        "clip_score": clip_score,
                        "clip_prompt": clip_prompt
                    })
        except Exception as e:
            logger.error(f"Error generating pattern: {e}")
    ai_metadata: Optional[Dict[str, Any]] = None
    if patterns and os.path.exists(patterns[0]):
        logger.info(f"  🤖 Analyzing generated patterns with AI...")
        try:
            ai_metadata = ai_culture_generator.generate_culture_metadata(culture, patterns[0])
            logger.info(f"  ✅ AI analysis completed")
        except Exception as e:
            logger.warning(f"  ⚠️ AI analysis failed: {e}")
    briefs = []
    if ai_metadata and 'brief' in ai_metadata:
        briefs.append(ai_metadata['brief'])
        logger.info(f"  📋 Using AI-generated design brief")
    else:
        try:
            brief = generate_cultural_note(culture)
            briefs.append(brief)
            logger.info(f"  📋 Using fallback cultural note")
        except Exception as e:
            logger.error(f"Error generating brief: {e}")
    kit_metadata: Dict[str, Any] = {
        "culture": culture,
        "generated_at": str(datetime.datetime.now()),
        "generated_by": "AI Image Analysis + Pattern Generation",
        "version": "2.0",
        "assets": {
            "patterns": [os.path.basename(p) for p in patterns],
            "palettes": palettes,
            "briefs": briefs,
            "pattern_metadata": pattern_metadata
        },
        "ai_analysis": {
            "fonts": ai_metadata.get('fonts', []) if ai_metadata else [],
            "elements": ai_metadata.get('elements', []) if ai_metadata else [],
            "ai_colors": ai_metadata.get('colors', []) if ai_metadata else [],
            "ai_patterns": ai_metadata.get('patterns', []) if ai_metadata else [],
            "design_brief": ai_metadata.get('brief', {}) if ai_metadata else {}
        },
        "export_formats": ["SVG", "PNG", "CSS", "JSON", "Figma", "Canva"],
        "compatible_platforms": ["Figma", "Canva", "Webflow", "Adobe Creative Suite"]
    }
    metadata_path = os.path.join(kit_dir, "kit_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(kit_metadata, f, indent=2)
    if ai_metadata:
        ai_metadata_path = os.path.join(kit_dir, f"{culture}_ai_analysis.json")
        with open(ai_metadata_path, 'w') as f:
            json.dump(ai_metadata, f, indent=2)
        logger.info(f"  💾 AI analysis saved to: {ai_metadata_path}")
    for pattern_path in patterns:
        if os.path.exists(pattern_path):
            new_path = os.path.join(kit_dir, os.path.basename(pattern_path))
            os.rename(pattern_path, new_path)
    logger.info("  Exporting in multiple formats...")
    exports = export_kit_formats(kit_dir, kit_metadata)
    logger.info(f"✅ AI-powered design kit generated in: {kit_dir}")
    logger.info(f"📁 Contains: {len(patterns)} patterns, {len(palettes)} palettes, {len(briefs)} briefs")
    if ai_metadata:
        logger.info(f"🤖 AI Analysis: {len(ai_metadata.get('fonts', []))} fonts, {len(ai_metadata.get('elements', []))} elements, {len(ai_metadata.get('colors', []))} colors")
    logger.info(f"📄 Metadata: {metadata_path}")
    logger.info(f"🎨 Export formats:")
    for format_name, path in exports.items():
        logger.info(f"   - {format_name.upper()}: {os.path.basename(path)}")

def cli_generate_culture_metadata(args: argparse.Namespace) -> None:
    """Generate AI-powered culture metadata from image analysis."""
    culture: str = args.culture
    image_path: str = args.image
    output_path: str = args.output or f"{culture}_metadata.json"
    if not image_path:
        logger.error("Image path is required for AI analysis. Usage: python main.py generate-culture-metadata --culture yoruba --image path/to/image.png")
        return
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        return
    logger.info(f"🤖 Generating AI-powered metadata for {culture} culture from image: {image_path}")
    try:
        metadata = ai_culture_generator.generate_culture_metadata(culture, image_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Culture metadata generated and saved to: {output_path}")
        logger.info(f"📊 Generated data includes:")
        logger.info(f"   - {len(metadata.get('fonts', []))} fonts")
        logger.info(f"   - {len(metadata.get('elements', []))} design elements")
        logger.info(f"   - {len(metadata.get('colors', []))} colors")
        logger.info(f"   - {len(metadata.get('patterns', []))} patterns")
        logger.info(f"   - Design brief with {len(metadata.get('brief', {}))} sections")
        logger.info(f"🎨 Sample fonts: {', '.join(metadata.get('fonts', [])[:3])}")
        logger.info(f"🎯 Sample elements: {', '.join([e['name'] for e in metadata.get('elements', [])[:2]])}")
        logger.info(f"🌈 Sample colors: {', '.join(metadata.get('colors', [])[:3])}")
    except Exception as e:
        logger.error(f"Error generating culture metadata: {e}")

def main() -> None:
    """Main entry point for the HeritageAI CLI."""
    parser = argparse.ArgumentParser(description="HeritageAI CLI")
    subparsers = parser.add_subparsers(dest='command')

    # generate
    gen_parser = subparsers.add_parser('generate', help='Generate pattern images and palettes')
    gen_parser.add_argument('--culture', required=True, help='Culture for pattern generation (e.g., yoruba, edo, maori, celtic, aztec, etc.)')
    gen_parser.add_argument('--count', type=int, default=4, help='Number of images to generate (default: 4)')
    gen_parser.add_argument('--aspect-ratio', default='1:1', choices=['1:1', '3:4', '4:3', '9:16', '16:9'], help='Aspect ratio for generated images (default: 1:1)')
    gen_parser.set_defaults(func=cli_generate)

    # palette
    pal_parser = subparsers.add_parser('palette', help='Extract palettes for all images in assets/')
    pal_parser.set_defaults(func=cli_palette)

    # brief
    brief_parser = subparsers.add_parser('brief', help='Generate cultural notes for all images in assets/')
    brief_parser.set_defaults(func=cli_brief)

    # bundle
    bundle_parser = subparsers.add_parser('bundle', help='Bundle image, palette, and note for each asset')
    bundle_parser.set_defaults(func=cli_bundle)

    # clip-score
    clip_parser = subparsers.add_parser('clip-score', help='Score all images in assets/ against a text prompt using CLIP')
    clip_parser.add_argument('--prompt', required=True, help='Text prompt to score images against')
    clip_parser.set_defaults(func=cli_clip_score)

    # generate-kit
    kit_parser = subparsers.add_parser('generate-kit', help='Generate complete design kit for a culture')
    kit_parser.add_argument('--culture', required=True, help='Culture to generate kit for (e.g., yoruba, edo, maori, celtic, aztec, etc.)')
    kit_parser.set_defaults(func=cli_generate_kit)

    # generate-culture-metadata
    metadata_parser = subparsers.add_parser('generate-culture-metadata', help='Generate AI-powered culture metadata from image analysis')
    metadata_parser.add_argument('--culture', required=True, help='Culture to generate metadata for')
    metadata_parser.add_argument('--image', required=True, help='Path to image file for AI analysis')
    metadata_parser.add_argument('--output', default=None, help='Output file path (default: culture_metadata.json)')
    metadata_parser.set_defaults(func=cli_generate_culture_metadata)
    kit_parser.set_defaults(func=cli_generate_kit)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 