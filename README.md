<!-- PROJECT LOGO -->
<!-- <p align="center">
  <img src="https://placehold.co/120x120?text=Logo" alt="HeritageAI Logo" width="120" height="120">
</p> -->

<h1 align="center">HeritageAI</h1>

<p align="center">
  <b>AI-powered platform for generating, analyzing, and exporting culturally-inspired design assets</b><br>
  <i>Patterns, palettes, briefs, and more — for any culture, powered by Google Gemini & CLIP</i>
  <br><br>
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#api-endpoints">API</a> •
  <a href="#extending-the-project">Extending</a> •
  <a href="#dependencies">Dependencies</a>
</p>

---

## 🚀 Overview

HeritageAI is a modern toolkit for designers, developers, and creators to generate authentic, culturally-inspired design assets using advanced AI models. Instantly create patterns, color palettes, design briefs, and more for any culture — with both a beautiful web UI and a powerful CLI.

---

## 🗂️ Project Structure

```text
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

## ✨ Features

| Feature                        | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| 🎨 Pattern Generation          | Generate culturally-inspired pattern images using AI                         |
| 🌈 Color Palette Extraction    | Extract color palettes from generated or uploaded images                     |
| 🤖 AI-Powered Analysis         | Analyze images for fonts, motifs, colors, patterns, and design briefs        |
| 📦 Bundling & Export           | Bundle images, palettes, and notes; export in SVG, PNG, CSS, JSON, Figma... |
| 🖥️ Web UI & REST API           | Modern Flask web interface and RESTful API                                   |
| 🛠️ CLI Tools                   | Command-line tools for batch processing, analysis, and export                |
| 🔄 Multi-API Key Support        | Robust retry logic with automatic Gemini API key rotation                    |
| 📝 Professional Codebase        | Type hints, docstrings, and logging throughout                               |

---

## 🏗️ Main Components

- **`main.py`** — CLI for all major operations (generation, analysis, export)
- **`ai_culture_generator.py`** — AI-powered image analysis for culture metadata
- **`web_api.py`** — Flask web UI & API endpoints
- **Supporting modules:**
  - `clip_model.py`, `gemini_client.py`, `imagegen_gemini.py`, `color_palette.py`, `export_formats.py`, `gemini_notes.py`

---

## 💻 Usage

### CLI (Command Line)

```bash
# Generate pattern images
python -m mvp_ai.main generate --culture yoruba --count 3 --aspect-ratio 1:1

# Generate a complete design kit
python -m mvp_ai.main generate-kit --culture edo

# Extract color palettes
python -m mvp_ai.main palette

# Generate cultural briefs
python -m mvp_ai.main brief

# Score images with CLIP
python -m mvp_ai.main clip-score --prompt "Yoruba textile pattern"

# Generate AI-powered culture metadata from an image
python -m mvp_ai.main generate-culture-metadata --culture maori --image path/to/image.png
```

### 🌐 Web UI

1. **Start the server:**
   ```bash
   python -m mvp_ai.web_api
   ```
2. **Open your browser:** [http://localhost:5000](http://localhost:5000)
3. **Generate & download kits** for any culture with a click!

---

## 🔗 API Endpoints

| Endpoint                              | Method | Description                                 |
|----------------------------------------|--------|---------------------------------------------|
| `/api/generate-kit`                    | POST   | Generate a design kit for a culture         |
| `/api/download-kit/&lt;culture&gt;`         | GET    | Download a zipped kit                       |
| `/api/cultures`                        | GET    | List available cultures                     |
| `/api/clip-score`                      | POST   | Score images with CLIP                      |
| `/api/generate-culture-metadata`       | POST   | Generate metadata for a culture/image       |

---

## 🧩 Extending the Project

- Add new cultures by using the UI or CLI/API with a new culture name
- Integrate other AI models by extending `gemini_client.py`
- Add new export formats in `export_formats.py`

---

## ⚙️ Dependencies

- Python 3.x
- Flask
- Gemini API (Google)
- CLIP model
- Pillow, ColorThief (for image and color processing)
- See `mvp_ai/requirements.txt` for full list

---

## 📁 Assets

All generated images, palettes, notes, and kits are stored in:
```
mvp_ai/assets/
```

---
---

<p align="center">
  <b>Made with ❤️ for cultural creativity</b>
</p> 