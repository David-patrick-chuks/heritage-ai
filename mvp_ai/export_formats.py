"""
export_formats.py - Export design kits and assets in multiple formats for HeritageAI.
"""
import os
import json
import base64
import logging
from typing import Any, Dict, List, Optional, Union
from PIL import Image
import io
from ai_culture_generator import ai_culture_generator

logger = logging.getLogger(__name__)

def get_culture_specific_fonts(culture: str, image_path: Optional[str] = None) -> List[str]:
    """
    Get culture-specific fonts using AI generation or fallback to defaults.
    Args:
        culture (str): The culture for which to get fonts.
        image_path (Optional[str]): Optional image path for AI analysis.
    Returns:
        List[str]: List of font names.
    """
    try:
        if image_path and os.path.exists(image_path):
            return ai_culture_generator.generate_culture_fonts(culture, image_path)
        else:
            return ['Nunito', 'Open Sans', 'Roboto', 'Lato']
    except Exception as e:
        logger.error(f"Error generating fonts for {culture}: {e}")
        return ['Nunito', 'Open Sans', 'Roboto', 'Lato']

def get_culture_specific_elements(culture: str, image_path: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Generate culture-specific design elements using AI or fallback to defaults.
    Args:
        culture (str): The culture for which to get elements.
        image_path (Optional[str]): Optional image path for AI analysis.
    Returns:
        List[Dict[str, str]]: List of design elements.
    """
    try:
        if image_path and os.path.exists(image_path):
            return ai_culture_generator.generate_culture_elements(culture, image_path)
        else:
            return [
                {"type": "symbol", "name": "Cultural Motif", "description": "Traditional cultural symbols"},
                {"type": "pattern", "name": "Geometric", "description": "Geometric design patterns"},
                {"type": "color", "name": "Traditional", "description": "Culture-specific color palette"}
            ]
    except Exception as e:
        logger.error(f"Error generating elements for {culture}: {e}")
        return [
            {"type": "symbol", "name": "Cultural Motif", "description": "Traditional cultural symbols"},
            {"type": "pattern", "name": "Geometric", "description": "Geometric design patterns"},
            {"type": "color", "name": "Traditional", "description": "Culture-specific color palette"}
        ]

def export_to_css(palette: Dict[str, Any], filename: str = "palette.css") -> str:
    """
    Export color palette to CSS variables.
    Args:
        palette (Dict[str, Any]): Palette dictionary.
        filename (str): Output filename (not used in function, for compatibility).
    Returns:
        str: CSS content as a string.
    """
    css_content = f"""/* {palette.get('note', 'Cultural Color Palette')} */\n:root {{\n"""
    for i, color in enumerate(palette.get('colors', [])):
        css_content += f"  --color-{i+1}: {color};\n"
    if 'primary' in palette:
        css_content += f"  --primary: {palette['primary']};\n"
    if 'secondary' in palette:
        css_content += f"  --secondary: {palette['secondary']};\n"
    if 'accent' in palette:
        css_content += f"  --accent: {palette['accent']};\n"
    css_content += "}\n"
    return css_content

def export_to_json(assets_data: Any, filename: str = "assets.json") -> str:
    """
    Export assets data to JSON format.
    Args:
        assets_data (Any): Data to export.
        filename (str): Output filename (not used in function, for compatibility).
    Returns:
        str: JSON string.
    """
    return json.dumps(assets_data, indent=2)

def image_to_base64_svg(image_path: str, width: int = 200, height: int = 200) -> Optional[str]:
    """
    Convert image to base64-encoded SVG for embedding.
    Args:
        image_path (str): Path to the image file.
        width (int): Width of the SVG.
        height (int): Height of the SVG.
    Returns:
        Optional[str]: SVG string or None if conversion fails.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            svg_content = f"""<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">\n  <image href=\"data:image/png;base64,{img_base64}\" width=\"{width}\" height=\"{height}\"/>\n</svg>"""
            return svg_content
    except Exception as e:
        logger.error(f"Error converting image to SVG: {e}")
        return None

def create_figma_plugin_data(kit_metadata: Dict[str, Any], kit_dir: str) -> Dict[str, Any]:
    """
    Create data structure for Figma plugin integration with AI-generated data.
    Args:
        kit_metadata (Dict[str, Any]): Metadata for the kit.
        kit_dir (str): Directory containing kit assets.
    Returns:
        Dict[str, Any]: Figma plugin data structure.
    """
    culture = kit_metadata['culture']
    ai_analysis = kit_metadata.get('ai_analysis', {})
    fonts = ai_analysis.get('fonts', []) if ai_analysis.get('fonts') else get_culture_specific_fonts(culture)
    elements = ai_analysis.get('elements', []) if ai_analysis.get('elements') else get_culture_specific_elements(culture)
    figma_data: Dict[str, Any] = {
        "name": f"{culture.title()} Cultural Design Kit",
        "description": f"AI-generated design assets inspired by {culture} culture",
        "colors": [],
        "images": [],
        "fonts": fonts,
        "elements": elements,
        "ai_analysis": ai_analysis,
        "metadata": kit_metadata
    }
    for palette in kit_metadata['assets']['palettes']:
        if 'colors' in palette:
            figma_data['colors'].extend(palette['colors'])
    if ai_analysis.get('ai_colors'):
        figma_data['colors'].extend(ai_analysis['ai_colors'])
    seen = set()
    unique_colors = []
    for color in figma_data['colors']:
        if color not in seen:
            seen.add(color)
            unique_colors.append(color)
    figma_data['colors'] = unique_colors
    for pattern_name in kit_metadata['assets']['patterns']:
        pattern_path = os.path.join(kit_dir, pattern_name)
        if os.path.exists(pattern_path):
            figma_data['images'].append({
                "name": pattern_name,
                "path": pattern_name,
                "type": "pattern",
                "size": os.path.getsize(pattern_path)
            })
    return figma_data

def create_canva_template_data(kit_metadata: Dict[str, Any], kit_dir: str) -> Dict[str, Any]:
    """
    Create data structure for Canva template integration with AI-generated data.
    Args:
        kit_metadata (Dict[str, Any]): Metadata for the kit.
        kit_dir (str): Directory containing kit assets.
    Returns:
        Dict[str, Any]: Canva template data structure.
    """
    culture = kit_metadata['culture']
    ai_analysis = kit_metadata.get('ai_analysis', {})
    fonts = ai_analysis.get('fonts', []) if ai_analysis.get('fonts') else get_culture_specific_fonts(culture)
    elements = ai_analysis.get('elements', []) if ai_analysis.get('elements') else get_culture_specific_elements(culture)
    canva_data: Dict[str, Any] = {
        "template_name": f"{culture.title()} Cultural Template",
        "brand_kit": {
            "colors": [],
            "fonts": fonts,
            "elements": elements
        },
        "assets": kit_metadata['assets'],
        "ai_analysis": ai_analysis,
        "usage_guidelines": f"Use these {culture} cultural elements respectfully and authentically",
        "generated_at": kit_metadata.get('generated_at', ''),
        "version": "2.0"
    }
    for palette in kit_metadata['assets']['palettes']:
        if 'colors' in palette:
            canva_data['brand_kit']['colors'].extend(palette['colors'])
    if ai_analysis.get('ai_colors'):
        canva_data['brand_kit']['colors'].extend(ai_analysis['ai_colors'])
    seen = set()
    unique_colors = []
    for color in canva_data['brand_kit']['colors']:
        if color not in seen:
            seen.add(color)
            unique_colors.append(color)
    canva_data['brand_kit']['colors'] = unique_colors
    return canva_data

def export_kit_formats(kit_dir: str, kit_metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Export kit in multiple formats for different platforms.
    Args:
        kit_dir (str): Directory to export files to.
        kit_metadata (Dict[str, Any]): Metadata for the kit.
    Returns:
        Dict[str, str]: Mapping of format names to file paths.
    """
    exports: Dict[str, str] = {}
    if kit_metadata['assets']['palettes']:
        css_content = export_to_css(kit_metadata['assets']['palettes'][0])
        css_path = os.path.join(kit_dir, "palette.css")
        with open(css_path, 'w') as f:
            f.write(css_content)
        exports['css'] = css_path
    json_content = export_to_json(kit_metadata)
    json_path = os.path.join(kit_dir, "kit_data.json")
    with open(json_path, 'w') as f:
        f.write(json_content)
    exports['json'] = json_path
    figma_data = create_figma_plugin_data(kit_metadata, kit_dir)
    figma_path = os.path.join(kit_dir, "figma_plugin.json")
    with open(figma_path, 'w') as f:
        json.dump(figma_data, f, indent=2)
    exports['figma'] = figma_path
    canva_data = create_canva_template_data(kit_metadata, kit_dir)
    canva_path = os.path.join(kit_dir, "canva_template.json")
    with open(canva_path, 'w') as f:
        json.dump(canva_data, f, indent=2)
    exports['canva'] = canva_path
    return exports 