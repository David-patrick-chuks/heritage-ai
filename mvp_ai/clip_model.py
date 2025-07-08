"""
clip_model.py - CLIP-based pattern scoring and (dummy) pattern/palette generation for HeritageAI.
"""
import os
import json
import torch
import open_clip
import logging
from typing import Tuple, Dict
from PIL import Image

logger = logging.getLogger(__name__)

def generate_pattern_and_palette(culture: str) -> Tuple[str, str]:
    """
    Dummy function to generate a pattern SVG and a palette JSON for a given culture.
    Args:
        culture (str): The culture for which to generate assets.
    Returns:
        Tuple[str, str]: Paths to the generated pattern SVG and palette JSON files.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    # TODO: Replace with real CLIP-based pattern generation
    pattern_path = os.path.join(assets_dir, f"{culture}_pattern.svg")
    palette_path = os.path.join(assets_dir, f"{culture}_palette.json")
    with open(pattern_path, 'w') as f:
        f.write(f'<svg><!-- Dummy pattern for {culture} --></svg>')
    palette: Dict[str, str] = {
        'primary': '#123456',
        'secondary': '#abcdef',
        'accent': '#fedcba',
        'note': f'Dummy palette for {culture}'
    }
    with open(palette_path, 'w') as f:
        json.dump(palette, f, indent=2)
    return pattern_path, palette_path

# Cache model and preprocess globally
_clip_model = None
_clip_preprocess = None
_clip_device = "cuda" if torch.cuda.is_available() else "cpu"

def _load_clip() -> None:
    """
    Load the CLIP model and preprocessing transforms if not already loaded.
    """
    global _clip_model, _clip_preprocess
    if _clip_model is None or _clip_preprocess is None:
        _clip_model, _, _clip_preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32-quickgelu", pretrained="openai", device=_clip_device
        )
        _clip_model.eval()
        logger.info(f"Loaded CLIP model on device: {_clip_device}")

# Real CLIP scoring implementation

def score_image_with_prompt(image_path: str, prompt: str) -> float:
    """
    Score an image against a text prompt using CLIP.
    Args:
        image_path (str): Path to the image file.
        prompt (str): Text prompt to score against.
    Returns:
        float: CLIP similarity score between image and prompt.
    """
    _load_clip()
    try:
        image = Image.open(image_path).convert("RGB")
        image_input = _clip_preprocess(image).unsqueeze(0).to(_clip_device)
        text_input = open_clip.tokenize([prompt]).to(_clip_device)
        with torch.no_grad():
            image_features = _clip_model.encode_image(image_input)
            text_features = _clip_model.encode_text(text_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            similarity = (image_features @ text_features.T).item()
        return float(similarity)
    except Exception as e:
        logger.error(f"Error scoring image with CLIP: {e}")
        return 0.0 