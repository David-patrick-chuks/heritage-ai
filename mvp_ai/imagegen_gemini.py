"""
imagegen_gemini.py - Pattern image generation using Gemini with robust prompt engineering and AI-driven culture details.
"""
import os
import logging
from typing import Optional, List, Union
from gemini_client import gemini_client

# Configure logging
logger = logging.getLogger(__name__)

# Directory to save generated images
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_pattern_image(
    culture: str,
    filename: Optional[str] = None,
    sample_count: int = 4,
    aspect_ratio: str = "1:1"
) -> Optional[Union[str, List[str]]]:
    """
    Generate pattern image(s) using the robust Gemini client with retry logic and a universal, highly detailed prompt.

    Args:
        culture (str): The culture to generate the pattern for.
        filename (Optional[str]): Optional filename for the generated image(s).
        sample_count (int): Number of images to generate (default: 4).
        aspect_ratio (str): Aspect ratio for generated images (default: "1:1").

    Returns:
        Optional[Union[str, List[str]]]: Path(s) to the generated image(s), or None if generation fails.
    """
    culture_key = culture.lower()
    # Always use dynamic AI-generated details, with cache
    if not hasattr(generate_pattern_image, '_dynamic_culture_details_cache'):
        generate_pattern_image._dynamic_culture_details_cache = {}
    cache = generate_pattern_image._dynamic_culture_details_cache
    if culture_key in cache:
        details = cache[culture_key]
    else:
        details = gemini_client.generate_culture_details(culture)
        cache[culture_key] = details
    # Further tuned, explicit, high-detail prompt template
    prompt = (
        f"Generate a seamless {culture.title()} textile pattern. "
        f"Include the most iconic motifs, symbols, and artistic elements associated with {culture.title()} culture. {details} "
        "Use a color palette that is traditional for this culture. "
        "Arrange motifs in a style typical of this culture's textiles (e.g., rows, bands, grids, or all-over). "
        "Reference traditional techniques (e.g., weaving, resist-dyeing, embroidery) if relevant. "
        "The design must fill the entire square canvas, with no borders, white space, or empty areas at the edges. "
        "Do not include any text, watermarks, signatures, or logos. "
        "The pattern should be highly detailed, vibrant, and culturally authentic, with consistent spacing and no blank or plain areas. "
        "Avoid modern or anachronistic elements; reference real artifacts or museum pieces where possible. "
        "The style should be professional, visually balanced, museum-quality, and suitable for use in high-end design applications. "
        "Create the pattern as if by a professional textile designer."
    )
    if not filename:
        filename = f"{culture.title()}_pattern_imagen4.png"
    try:
        result = gemini_client.generate_image(
            prompt=prompt,
            sample_count=sample_count,
            filename=filename,
            aspect_ratio=aspect_ratio
        )
        return result
    except Exception as e:
        logger.error(f"[Imagen 4 API error: {e}]")
        return None 