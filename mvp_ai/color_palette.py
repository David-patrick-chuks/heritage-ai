"""
color_palette.py - Extract color palettes from images using ColorThief for HeritageAI.
"""
import os
import json
import logging
from typing import List, Tuple, Optional
from colorthief import ColorThief

logger = logging.getLogger(__name__)

def extract_palette(
    image_path: str,
    palette_size: int = 5,
    output_name: Optional[str] = None
) -> Tuple[List[str], str]:
    """
    Extract a color palette from an image and save it as a JSON file.

    Args:
        image_path (str): Path to the image file.
        palette_size (int): Number of colors to extract (default: 5).
        output_name (Optional[str]): Optional output filename for the palette JSON.

    Returns:
        Tuple[List[str], str]: List of hex color strings and the path to the saved JSON file.
    """
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")
    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=palette_size)
    # Convert RGB tuples to hex
    hex_palette = ["#%02x%02x%02x" % color for color in palette]
    # Save to JSON
    assets_dir = os.path.dirname(image_path)
    if not output_name:
        base = os.path.splitext(os.path.basename(image_path))[0]
        output_name = f"{base}_palette.json"
    output_path = os.path.join(assets_dir, output_name)
    with open(output_path, 'w') as f:
        json.dump({"palette": hex_palette}, f, indent=2)
    logger.info(f"Extracted palette for {image_path}: {hex_palette} (saved to {output_path})")
    return hex_palette, output_path 