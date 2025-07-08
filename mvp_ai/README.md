# HeritageAI MVP AI Backend

This directory contains the MVP AI backend for HeritageAI, focused on generating culturally-inspired design assets using AI models including Google Gemini and CLIP.

## Features
- **AI-Powered Image Analysis**: Uses Gemini to analyze actual images and extract culture-specific fonts, elements, colors, and patterns
- **Flexible Culture Support**: Any culture can be input - no predefined limitations
- **CLIP-based Visual Analysis**: For pattern matching and style extraction
- **Multi-API Key Support**: Robust retry logic with automatic API key rotation
- **Comprehensive Asset Generation**: Patterns, color palettes, design briefs, and metadata
- **Multiple Export Formats**: CSS, JSON, Figma plugin data, Canva templates
- **Web API & CLI**: Both command-line and web interfaces available
- **Professional Codebase**: Type hints, docstrings, and logging throughout for maintainability

## Structure
- `main.py` — CLI entry point with subcommands for different operations
- `web_api.py` — Flask web API for browser-based interaction
- `ai_culture_generator.py` — AI-powered image analysis for culture metadata generation
- `gemini_client.py` — Robust Gemini API client with retry logic and logging
- `clip_model.py` — CLIP integration for visual analysis
- `export_formats.py` — Multi-format export (CSS, JSON, Figma, Canva)
- `color_palette.py` — Color palette extraction from images
- `assets/` — Generated design assets and kits
- `test_ai_culture.py` — Test script for AI image analysis

## Usage

### CLI Commands
```bash
# Generate pattern images
python main.py generate --culture yoruba --count 3

# Generate complete design kit
python main.py generate-kit --culture celtic

# Generate AI-powered culture metadata from image analysis
python main.py generate-culture-metadata --culture japanese --image path/to/image.png

# Extract color palettes from images
python main.py palette

# Generate cultural briefs
python main.py brief

# Score images with CLIP
python main.py clip-score --prompt "traditional geometric pattern"
```

### Web API
```bash
# Start the web server
python web_api.py

# Then visit http://localhost:5000 in your browser
```

### AI Image Analysis (Python API)
```python
from ai_culture_generator import ai_culture_generator

# Generate comprehensive culture metadata from image
metadata = ai_culture_generator.generate_culture_metadata("aztec", "path/to/aztec_image.png")

# Generate specific components from image
fonts = ai_culture_generator.generate_culture_fonts("persian", "path/to/persian_image.png")
elements = ai_culture_generator.generate_culture_elements("egyptian", "path/to/egyptian_image.png")
colors = ai_culture_generator.generate_culture_colors("indian", "path/to/indian_image.png")
patterns = ai_culture_generator.generate_culture_patterns("celtic", "path/to/celtic_image.png")
```

## AI-Powered Features
- **Image Analysis**: AI analyzes actual cultural design images to extract authentic elements
- **Font Generation**: AI identifies appropriate fonts based on the visual style of the image
- **Element Detection**: AI identifies and describes design elements visible in the image
- **Color Extraction**: Uses ColorThief to extract actual color palettes from images
- **Pattern Analysis**: AI describes patterns and their usage based on visual content
- **Design Briefs**: AI generates comprehensive design briefs based on image analysis
- **Fallback System**: If image analysis fails, falls back to safe defaults

## Requirements
- Python 3.8+
- `openai-clip` or `transformers` (for CLIP)
- `requests` (for Gemini API)
- `Flask` (for web API)
- `Pillow` (for image processing)
- `python-dotenv` (for environment variables)
- `colorthief` (for color extraction)

## Environment Variables
Create a `.env` file with your Gemini API keys:
```
GEMINI_API_KEY_1=your_first_api_key
GEMINI_API_KEY_2=your_second_api_key
# Add more keys as needed for retry logic
```

## Logging, Type Hints, and Error Handling
- All modules use Python's `logging` for error and status reporting.
- Type hints are present throughout for clarity and maintainability.
- All public functions and classes include docstrings.
- Robust error handling and fallback logic ensure reliability in production and research settings.

## Contributing & Code Style
- Follow PEP8 and PEP257 for code and docstring style.
- Use type hints for all function arguments and return values.
- Add/expand docstrings for all public functions, classes, and modules.
- Use `logging` (not `print`) for all status and error messages.
- Write modular, testable code. Add or update tests in `test_ai_culture.py` and related files.
- Submit pull requests with clear descriptions and reference related issues if applicable.

## Testing
```bash
# Test AI image analysis
python test_ai_culture.py

# Test retry logic
python test_retry.py
```

## Next Steps
- Expand AI model support (DALL-E, Midjourney, etc.)
- Add more export formats (Adobe Creative Suite, Sketch)
- Implement culture-specific image generation prompts
- Add user authentication and project management 