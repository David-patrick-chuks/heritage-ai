# HeritageAI

## Overview

**HeritageAI** is an AI-powered platform for generating, analyzing, and exporting culturally-inspired design assets. It leverages advanced AI models (including Google Gemini and CLIP) to create patterns, color palettes, design briefs, and metadata for various world cultures. The project provides both a command-line interface (CLI) and a web API/UI for users to interact with the system.

---

## Project Structure

```
heritage-ai/
│
├── mvp_ai/
│   ├── main.py                  # CLI and orchestration module
│   ├── ai_culture_generator.py  # AI-powered culture-specific design analysis
│   ├── web_api.py               # Flask web API and UI
│   ├── clip_model.py            # CLIP-based image scoring
│   ├── gemini_client.py         # Gemini API client
│   ├── imagegen_gemini.py       # Pattern image generation using Gemini
│   ├── color_palette.py         # Color palette extraction utilities
│   ├── export_formats.py        # Exporting assets in various formats
│   ├── gemini_notes.py          # Cultural note generation
│   ├── assets/                  # Generated images, palettes, notes, kits
│   └── ... (tests, docs)
└── README.md
```

---

## Key Features

### 1. Pattern and Palette Generation
- Generate culturally-inspired pattern images using AI.
- Extract color palettes from generated or uploaded images.

### 2. AI-Powered Analysis
- Analyze images to extract:
  - Fonts that match the cultural style
  - Key design elements and motifs
  - Color palettes
  - Pattern descriptions
  - Comprehensive design briefs

### 3. Bundling and Export
- Bundle images, palettes, and notes into a single kit.
- Export kits in multiple formats (SVG, PNG, CSS, JSON, Figma, Canva).

### 4. Web API and UI
- Flask-based web interface for generating and downloading design kits.
- RESTful API endpoints for integration and automation.

### 5. CLI Tools
- Command-line tools for batch processing, analysis, and export.

---

## Main Components

### `main.py` (CLI & Orchestration)
- Provides CLI commands for:
  - Generating patterns and palettes
  - Extracting palettes from images
  - Generating cultural notes
  - Bundling assets
  - Scoring images with CLIP
  - Generating complete design kits
  - Generating culture metadata via AI analysis
- Handles orchestration and logging.

### `ai_culture_generator.py` (AI Analysis)
- `AICultureGenerator` class:
  - Uses Gemini API to analyze images and extract:
    - Fonts
    - Design elements
    - Colors
    - Patterns
    - Design briefs
  - Provides fallback values if AI analysis fails.
  - Exposes a single method to generate comprehensive metadata for a culture and image.

### `web_api.py` (Web API & UI)
- Flask app with:
  - Web UI for generating and downloading kits for preset or custom cultures.
  - API endpoints:
    - `/api/generate-kit` (POST): Generate a design kit for a culture.
    - `/api/download-kit/<culture>` (GET): Download a zipped kit.
    - `/api/cultures` (GET): List available cultures.
    - `/api/clip-score` (POST): Score images with CLIP.
    - `/api/generate-culture-metadata` (POST): Generate metadata for a culture/image.
- Simple, modern UI using the Nunito font.

### Supporting Modules
- `clip_model.py`: Handles image scoring using CLIP.
- `gemini_client.py`: Handles communication with the Gemini API.
- `imagegen_gemini.py`: Generates pattern images using Gemini.
- `color_palette.py`: Extracts color palettes from images.
- `export_formats.py`: Exports assets in various formats.
- `gemini_notes.py`: Generates cultural notes using Gemini.

---

## Usage

### CLI

Run the CLI for various tasks (examples):

```bash
python -m mvp_ai.main generate --culture yoruba --count 3 --aspect-ratio 1:1
python -m mvp_ai.main palette
python -m mvp_ai.main brief
python -m mvp_ai.main bundle
python -m mvp_ai.main clip-score --prompt "Yoruba textile pattern"
python -m mvp_ai.main generate-kit --culture edo
python -m mvp_ai.main generate-culture-metadata --culture maori --image path/to/image.png
```

### Web UI

1. Start the Flask server:
   ```bash
   python -m mvp_ai.web_api
   ```
2. Open your browser to `http://localhost:5000`
3. Use the UI to generate and download design kits.

### API Endpoints

- `POST /api/generate-kit` with `{ "culture": "yoruba" }`
- `GET /api/download-kit/yoruba`
- `GET /api/cultures`
- `POST /api/clip-score` with `{ "prompt": "..." }`
- `POST /api/generate-culture-metadata` with `{ "culture": "...", "image": "..." }`

---

## Extending the Project

- Add new cultures by updating the UI or using the CLI/API with a new culture name.
- Integrate with other AI models by extending `gemini_client.py` or adding new modules.
- Add new export formats in `export_formats.py`.

---

## Dependencies

- Python 3.x
- Flask
- Gemini API (Google)
- CLIP model
- Pillow, ColorThief (for image and color processing)
- Other dependencies listed in `mvp_ai/requirements.txt`

---

## Assets

- All generated images, palettes, notes, and kits are stored in the `mvp_ai/assets/` directory.

---

## License & Credits

(Add your license and credits here.) 