"""
web_api.py - Flask web API and UI for HeritageAI cultural design asset generation and download.
"""
from flask import Flask, request, jsonify, send_file, render_template_string
import os
import json
import zipfile
import io
import logging
from datetime import datetime
from main import cli_generate_kit, cli_clip_score, cli_generate_culture_metadata
from export_formats import export_kit_formats
from ai_culture_generator import ai_culture_generator
import argparse
from typing import Any

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Simple HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HeritageAI - Cultural Design Assets</title>
    <style>
        body { font-family: 'Nunito', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .culture-card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .loading { display: none; }
        .custom-culture { background: #f8f9fa; border: 2px dashed #007bff; }
        .custom-culture input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🎨 HeritageAI</h1>
    <p>Generate culturally inspired design assets using AI</p>
    
    <div class="culture-card">
        <h3>Yoruba Culture</h3>
        <p>Traditional Nigerian patterns and colors</p>
        <button class="btn" onclick="generateKit('yoruba')">Generate Kit</button>
        <div id="yoruba-status" class="loading">Generating...</div>
    </div>
    
    <div class="culture-card">
        <h3>Edo Culture</h3>
        <p>Benin Kingdom artistic traditions</p>
        <button class="btn" onclick="generateKit('edo')">Generate Kit</button>
        <div id="edo-status" class="loading">Generating...</div>
    </div>
    
    <div class="culture-card">
        <h3>Maori Culture</h3>
        <p>Indigenous New Zealand designs</p>
        <button class="btn" onclick="generateKit('maori')">Generate Kit</button>
        <div id="maori-status" class="loading">Generating...</div>
    </div>
    
    <div class="culture-card custom-culture">
        <h3>Custom Culture</h3>
        <p>Enter any culture name to generate unique design assets</p>
        <input type="text" id="custom-culture-input" placeholder="e.g., celtic, aztec, japanese, persian, etc.">
        <button class="btn" onclick="generateCustomKit()">Generate Custom Kit</button>
        <div id="custom-status" class="loading">Generating...</div>
    </div>
    
    <script>
        function generateKit(culture) {
            document.getElementById(culture + '-status').style.display = 'block';
            fetch('/api/generate-kit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({culture: culture})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/api/download-kit/' + culture;
                } else {
                    alert('Error: ' + data.error);
                }
                document.getElementById(culture + '-status').style.display = 'none';
            });
        }
        
        function generateCustomKit() {
            const culture = document.getElementById('custom-culture-input').value.trim();
            if (!culture) {
                alert('Please enter a culture name');
                return;
            }
            
            document.getElementById('custom-status').style.display = 'block';
            fetch('/api/generate-kit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({culture: culture})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/api/download-kit/' + culture;
                } else {
                    alert('Error: ' + data.error);
                }
                document.getElementById('custom-status').style.display = 'none';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index() -> Any:
    """Render the main web UI for HeritageAI."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate-kit', methods=['POST'])
def api_generate_kit() -> Any:
    """API endpoint to generate a design kit for a given culture."""
    try:
        data = request.get_json()
        culture = data.get('culture')
        if not culture:
            logger.error("Culture is required for kit generation.")
            return jsonify({'success': False, 'error': 'Culture is required'})
        class MockArgs:
            def __init__(self, culture):
                self.culture = culture
        args = MockArgs(culture)
        cli_generate_kit(args)
        logger.info(f"Kit generated for culture: {culture}")
        return jsonify({'success': True, 'culture': culture})
    except Exception as e:
        logger.error(f"Error generating kit: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download-kit/<culture>')
def download_kit(culture: str) -> Any:
    """API endpoint to download a generated design kit as a zip file."""
    try:
        kit_dir = os.path.join('assets', f'{culture}_kit')
        if not os.path.exists(kit_dir):
            logger.error(f"Kit not found for culture: {culture}")
            return jsonify({'error': 'Kit not found'})
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for root, dirs, files in os.walk(kit_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, kit_dir)
                    zf.write(file_path, arc_name)
        memory_file.seek(0)
        logger.info(f"Kit zipped and sent for culture: {culture}")
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{culture}_design_kit.zip'
        )
    except Exception as e:
        logger.error(f"Error downloading kit: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/cultures')
def get_cultures() -> Any:
    """API endpoint to get a list of example and popular cultures."""
    default_cultures = [
        {
            'id': 'yoruba',
            'name': 'Yoruba',
            'description': 'Traditional Nigerian patterns and colors',
            'region': 'West Africa'
        },
        {
            'id': 'edo',
            'name': 'Edo',
            'description': 'Benin Kingdom artistic traditions',
            'region': 'West Africa'
        },
        {
            'id': 'maori',
            'name': 'Maori',
            'description': 'Indigenous New Zealand designs',
            'region': 'Oceania'
        }
    ]
    popular_cultures = [
        {
            'id': 'celtic',
            'name': 'Celtic',
            'description': 'Ancient European knotwork and spirals',
            'region': 'Europe'
        },
        {
            'id': 'aztec',
            'name': 'Aztec',
            'description': 'Mesoamerican geometric and symbolic designs',
            'region': 'Americas'
        },
        {
            'id': 'japanese',
            'name': 'Japanese',
            'description': 'Traditional Japanese art and patterns',
            'region': 'Asia'
        },
        {
            'id': 'persian',
            'name': 'Persian',
            'description': 'Ancient Persian ornamental designs',
            'region': 'Middle East'
        }
    ]
    return jsonify({
        'default': default_cultures,
        'popular': popular_cultures,
        'note': 'You can use any culture name - these are just examples!'
    })

@app.route('/api/clip-score', methods=['POST'])
def api_clip_score() -> Any:
    """API endpoint to score images in assets/ against a prompt using CLIP."""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            logger.error("Prompt required for CLIP scoring.")
            return jsonify({'error': 'Prompt required'})
        class MockArgs:
            def __init__(self, prompt):
                self.prompt = prompt
        args = MockArgs(prompt)
        cli_clip_score(args)
        logger.info(f"CLIP scoring completed for prompt: {prompt}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error in CLIP scoring: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/generate-culture-metadata', methods=['POST'])
def api_generate_culture_metadata() -> Any:
    """API endpoint to generate AI-powered culture metadata from an uploaded image."""
    try:
        if 'image' not in request.files:
            logger.error("Image file is required for culture metadata generation.")
            return jsonify({'success': False, 'error': 'Image file is required'})
        image_file = request.files['image']
        culture = request.form.get('culture')
        if not culture:
            logger.error("Culture is required for culture metadata generation.")
            return jsonify({'success': False, 'error': 'Culture is required'})
        if image_file.filename == '':
            logger.error("No image selected for culture metadata generation.")
            return jsonify({'success': False, 'error': 'No image selected'})
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            image_file.save(tmp_file.name)
            image_path = tmp_file.name
        try:
            metadata = ai_culture_generator.generate_culture_metadata(culture, image_path)
            logger.info(f"Culture metadata generated for {culture}")
            return jsonify({
                'success': True, 
                'culture': culture,
                'metadata': metadata
            })
        finally:
            if os.path.exists(image_path):
                os.unlink(image_path)
    except Exception as e:
        logger.error(f"Error generating culture metadata: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 