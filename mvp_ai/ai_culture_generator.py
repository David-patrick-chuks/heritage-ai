"""
ai_culture_generator.py - AI-powered generation of culture-specific design elements, colors, fonts, patterns, and briefs from images.
"""
import json
import re
import os
import logging
from typing import List, Dict, Any, Optional
from gemini_client import gemini_client
from color_palette import extract_palette

logger = logging.getLogger(__name__)

class AICultureGenerator:
    """Generate culture-specific design elements using AI image analysis."""
    
    def __init__(self) -> None:
        """Initialize the AICultureGenerator with a Gemini client."""
        self.gemini_client = gemini_client
    
    def generate_culture_fonts(self, culture: str, image_path: str) -> List[str]:
        """Generate a list of culture-specific fonts by analyzing the image."""
        prompt = f"""
        Analyze this {culture} cultural design image and identify 4-6 appropriate fonts that would complement the visual style.
        
        Consider:
        - The overall aesthetic and mood of the design
        - Cultural authenticity and respect
        - Readability and modern usability
        - Font availability on common platforms
        
        Return ONLY a JSON array of font names, like:
        ["Font Name 1", "Font Name 2", "Font Name 3"]
        
        Focus on fonts that would work well with this specific design style.
        """
        try:
            response = self.gemini_client.analyze_image_with_prompt(image_path, prompt)
            if response:
                fonts = self._extract_json_array(response)
                return fonts if fonts else self._get_fallback_fonts(culture)
            return self._get_fallback_fonts(culture)
        except Exception as e:
            logger.error(f"Error generating fonts for {culture}: {e}")
            return self._get_fallback_fonts(culture)
    
    def generate_culture_elements(self, culture: str, image_path: str) -> List[Dict[str, str]]:
        """Generate a list of culture-specific design elements by analyzing the image."""
        prompt = f"""
        Analyze this {culture} cultural design image and identify 3-5 key design elements present.
        
        For each element you see, provide:
        - type: "symbol", "pattern", "motif", "shape", "texture", or "element"
        - name: A descriptive name for what you see
        - description: Brief explanation of what the element is and its visual characteristics
        
        Return ONLY a JSON array like:
        [
            {{"type": "symbol", "name": "Element Name", "description": "Description of what you see"}},
            {{"type": "pattern", "name": "Pattern Name", "description": "Description of the pattern"}}
        ]
        
        Focus on actual elements visible in the image, not general cultural knowledge.
        """
        try:
            response = self.gemini_client.analyze_image_with_prompt(image_path, prompt)
            if response:
                elements = self._extract_json_array(response)
                return elements if elements else self._get_fallback_elements(culture)
            return self._get_fallback_elements(culture)
        except Exception as e:
            logger.error(f"Error generating elements for {culture}: {e}")
            return self._get_fallback_elements(culture)
    
    def generate_culture_colors(self, culture: str, image_path: str) -> List[str]:
        """Extract a color palette from the image using ColorThief."""
        try:
            colors, _ = extract_palette(image_path, palette_size=8)
            return colors
        except Exception as e:
            logger.error(f"Error extracting colors for {culture}: {e}")
            return self._get_fallback_colors(culture)
    
    def generate_culture_patterns(self, culture: str, image_path: str) -> List[Dict[str, str]]:
        """Generate pattern descriptions by analyzing the image."""
        prompt = f"""
        Analyze this {culture} cultural design image and describe the patterns you see.
        
        For each pattern visible in the image, provide:
        - name: Pattern name based on what you see
        - description: Detailed description of the pattern's visual characteristics
        - style: Visual style (geometric, organic, abstract, etc.)
        - usage: How this pattern appears to be used in the design
        
        Return ONLY a JSON array like:
        [
            {{
                "name": "Pattern Name",
                "description": "Detailed description of what you see",
                "style": "geometric",
                "usage": "How it's used in the design"
            }}
        ]
        
        Focus on actual patterns visible in the image, not general cultural patterns.
        """
        try:
            response = self.gemini_client.analyze_image_with_prompt(image_path, prompt)
            if response:
                patterns = self._extract_json_array(response)
                return patterns if patterns else self._get_fallback_patterns(culture)
            return self._get_fallback_patterns(culture)
        except Exception as e:
            logger.error(f"Error generating patterns for {culture}: {e}")
            return self._get_fallback_patterns(culture)
    
    def generate_culture_brief(self, culture: str, image_path: str, style: str = "modern") -> Dict[str, str]:
        """Generate a comprehensive design brief by analyzing the image."""
        prompt = f"""
        Analyze this {culture} cultural design image and create a comprehensive design brief.
        
        Based on what you see in the image, provide:
        - cultural_context: What cultural elements or style you observe
        - design_principles: Key design principles evident in this image
        - color_philosophy: How colors are used and their visual impact
        - typography_approach: What typography would complement this style
        - pattern_usage: How patterns are used in this design
        - modern_adaptation: How this style could be adapted to {style} design
        - cultural_sensitivity: Guidelines for respectful use of this style
        
        Return ONLY a JSON object with these fields.
        Focus on what you actually see in the image, not general cultural knowledge.
        """
        try:
            response = self.gemini_client.analyze_image_with_prompt(image_path, prompt)
            if response:
                brief = self._extract_json_object(response)
                return brief if brief else self._get_fallback_brief(culture, style)
            return self._get_fallback_brief(culture, style)
        except Exception as e:
            logger.error(f"Error generating brief for {culture}: {e}")
            return self._get_fallback_brief(culture, style)
    
    def generate_culture_metadata(self, culture: str, image_path: str) -> Dict[str, Any]:
        """Generate comprehensive culture metadata by analyzing the image."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return {
            "culture": culture,
            "source_image": image_path,
            "fonts": self.generate_culture_fonts(culture, image_path),
            "elements": self.generate_culture_elements(culture, image_path),
            "colors": self.generate_culture_colors(culture, image_path),
            "patterns": self.generate_culture_patterns(culture, image_path),
            "brief": self.generate_culture_brief(culture, image_path),
            "generated_by": "AI Image Analysis",
            "version": "2.0"
        }
    
    def _extract_json_array(self, text: str) -> Optional[List[Any]]:
        """Extract a JSON array from AI response text."""
        try:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return None
        except json.JSONDecodeError:
            return None
    
    def _extract_json_object(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract a JSON object from AI response text."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return None
        except json.JSONDecodeError:
            return None
    
    def _get_fallback_fonts(self, culture: str) -> List[str]:
        """Return fallback fonts if AI generation fails."""
        return ['Nunito', 'Open Sans', 'Roboto', 'Lato']
    
    def _get_fallback_elements(self, culture: str) -> List[Dict[str, str]]:
        """Return fallback elements if AI generation fails."""
        return [
            {"type": "symbol", "name": "Cultural Motif", "description": "Traditional cultural symbols"},
            {"type": "pattern", "name": "Geometric", "description": "Geometric design patterns"},
            {"type": "color", "name": "Traditional", "description": "Culture-specific color palette"}
        ]
    
    def _get_fallback_colors(self, culture: str) -> List[str]:
        """Return fallback colors if AI generation fails."""
        return ['#8B4513', '#D2691E', '#CD853F', '#F4A460', '#DEB887']
    
    def _get_fallback_patterns(self, culture: str) -> List[Dict[str, str]]:
        """Return fallback patterns if AI generation fails."""
        return [
            {
                "name": "Traditional Pattern",
                "description": "Traditional geometric pattern",
                "style": "geometric",
                "usage": "Decorative elements"
            }
        ]
    
    def _get_fallback_brief(self, culture: str, style: str) -> Dict[str, str]:
        """Return fallback brief if AI generation fails."""
        return {
            "cultural_context": f"Design inspired by {culture} culture",
            "design_principles": "Respect cultural authenticity while creating modern designs",
            "color_philosophy": "Use colors that reflect traditional materials and symbolism",
            "typography_approach": "Choose fonts that complement cultural aesthetics",
            "pattern_usage": "Incorporate traditional patterns thoughtfully",
            "modern_adaptation": f"Adapt traditional elements to {style} style",
            "cultural_sensitivity": "Ensure respectful and accurate representation"
        }

# Global instance
ai_culture_generator = AICultureGenerator() 