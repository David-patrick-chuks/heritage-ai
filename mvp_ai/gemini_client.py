import os
import time
import requests
import json
import logging
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini and Imagen APIs, with robust retry and error handling."""
    def __init__(self) -> None:
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.retry_delay_429 = int(os.getenv('RETRY_DELAY_429', 2000))
        self.retry_delay_503 = int(os.getenv('RETRY_DELAY_503', 3000))
        self.retry_delay_500 = int(os.getenv('RETRY_DELAY_500', 2000))
        
        # API endpoints
        self.imagen_url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
        self.text_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.image_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.upload_url = "https://generativelanguage.googleapis.com/upload/v1beta/files"
        
        if not self.api_keys:
            raise ValueError("No Gemini API keys found in environment variables")
    
    def _load_api_keys(self) -> List[str]:
        """Load multiple API keys from environment variables"""
        keys = []
        i = 1
        while True:
            key = os.getenv(f'GEMINI_API_KEY_{i}')
            if not key:
                break
            keys.append(key)
            i += 1
        
        # Fallback to single key for backward compatibility
        if not keys:
            single_key = os.getenv('GEMINI_API_KEY')
            if single_key:
                keys = [single_key]
        
        return keys
    
    def _get_current_api_key(self) -> str:
        """Get current API key"""
        return self.api_keys[self.current_key_index]
    
    def _switch_api_key(self):
        """Switch to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.warning(f"🔄 Switched to API key {self.current_key_index + 1}/{len(self.api_keys)}")
    
    def _handle_error(self, error: Exception, retry_count: int, max_retries: int) -> bool:
        """Handle different types of errors and decide whether to retry"""
        error_msg = str(error).lower()
        
        if retry_count >= max_retries:
            logger.error(f"❌ Maximum retry attempts ({max_retries}) reached")
            return False
        
        if "429" in error_msg or "too many requests" in error_msg:
            logger.warning(f"🚨 API key {self.current_key_index + 1} limit exhausted, switching...")
            self._switch_api_key()
            time.sleep(self.retry_delay_429 / 1000)
            return True
        
        elif "503" in error_msg or "service unavailable" in error_msg:
            logger.warning(f"⏳ Service is unavailable. Retrying in {self.retry_delay_503/1000} seconds...")
            time.sleep(self.retry_delay_503 / 1000)
            return True
        
        elif "500" in error_msg or "internal server error" in error_msg:
            logger.warning(f"⚠️ Internal server error. Retrying in {self.retry_delay_500/1000} seconds...")
            time.sleep(self.retry_delay_500 / 1000)
            return True
        
        elif "timeout" in error_msg:
            logger.warning(f"⏱️ Request timeout. Retrying in 2 seconds...")
            time.sleep(2)
            return True
        
        else:
            logger.error(f"⚠️ Unexpected error: {error}")
            return False
    
    def generate_image(self, prompt: str, sample_count: int = 4, filename: Optional[str] = None, aspect_ratio: str = "1:1") -> Optional[List[str]]:
        """Generate image with retry logic"""
        return self._make_request_with_retry(
            self._generate_image_request,
            prompt=prompt,
            sample_count=sample_count,
            filename=filename,
            aspect_ratio=aspect_ratio
        )
    
    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate text with retry logic"""
        return self._make_request_with_retry(
            self._generate_text_request,
            prompt=prompt
        )
    
    def _make_request_with_retry(self, request_func, **kwargs):
        """Generic retry wrapper for API requests"""
        for retry_count in range(self.max_retries + 1):
            try:
                return request_func(**kwargs)
            except Exception as e:
                if not self._handle_error(e, retry_count, self.max_retries):
                    raise e
        
        raise Exception(f"Failed after {self.max_retries} retry attempts")
    
    def _generate_image_request(self, prompt: str, sample_count: int = 1, filename: Optional[str] = None, aspect_ratio: str = "1:1") -> Optional[List[str]]:
        """Make image generation request"""
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._get_current_api_key()
        }
        
        data = {
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": sample_count, "aspectRatio": aspect_ratio}
        }
        
        response = requests.post(self.imagen_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Process and save images
        image_paths = []
        for idx, img_obj in enumerate(result.get("predictions", [])):
            image_data = img_obj.get("bytesBase64Encoded")
            if image_data:
                import base64
                image_bytes = base64.b64decode(image_data)
                
                # Generate filename if not provided
                if not filename:
                    filename = f"generated_image_{int(time.time())}.png"
                
                out_name = filename if sample_count == 1 else f"{filename.rstrip('.png')}_{idx+1}.png"
                image_path = os.path.join(os.path.dirname(__file__), 'assets', out_name)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_paths.append(image_path)
        
        return image_paths[0] if sample_count == 1 else image_paths
    
    def _generate_text_request(self, prompt: str) -> Optional[str]:
        """Make text generation request"""
        headers = {"Content-Type": "application/json"}
        params = {"key": self._get_current_api_key()}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(self.text_url, headers=headers, params=params, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()

    def analyze_image_with_prompt(self, image_path: str, prompt: str) -> Optional[str]:
        """Analyze image with Gemini using file upload and robust retry logic"""
        return self._make_request_with_retry(
            self._analyze_image_with_prompt_request,
            image_path=image_path,
            prompt=prompt
        )

    def _analyze_image_with_prompt_request(self, image_path: str, prompt: str) -> Optional[str]:
        """Upload image, send prompt, and return Gemini's text response"""
        file_uri = self._upload_image_to_gemini(image_path)
        if not file_uri:
            raise Exception("Failed to upload image to Gemini")
        mime_type = self._get_mime_type(image_path)
        headers = {
            "x-goog-api-key": self._get_current_api_key(),
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{
                "parts": [
                    {
                        "file_data": {
                            "mime_type": mime_type,
                            "file_uri": file_uri
                        }
                    },
                    {"text": prompt}
                ]
            }]
        }
        response = requests.post(self.image_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()

    def _upload_image_to_gemini(self, image_path: str) -> Optional[str]:
        """Upload image to Gemini and return file URI"""
        try:
            mime_type = self._get_mime_type(image_path)
            num_bytes = os.path.getsize(image_path)
            display_name = os.path.basename(image_path)
            headers = {
                "x-goog-api-key": self._get_current_api_key(),
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(num_bytes),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": "application/json"
            }
            data = {"file": {"display_name": display_name}}
            response = requests.post(self.upload_url, headers=headers, json=data)
            response.raise_for_status()
            upload_url = response.headers.get("X-Goog-Upload-URL")
            if not upload_url:
                raise Exception("No upload URL received")
            with open(image_path, 'rb') as f:
                file_data = f.read()
            upload_headers = {
                "x-goog-api-key": self._get_current_api_key(),
                "Content-Length": str(num_bytes),
                "X-Goog-Upload-Offset": "0",
                "X-Goog-Upload-Command": "upload, finalize"
            }
            upload_response = requests.post(upload_url, headers=upload_headers, data=file_data)
            upload_response.raise_for_status()
            file_info = upload_response.json()
            file_uri = file_info.get("file", {}).get("uri")
            return file_uri
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None

    def _get_mime_type(self, image_path: str) -> str:
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'image/jpeg')

    def generate_culture_details(self, culture: str) -> str:
        """Generate a detailed, visually descriptive paragraph about a culture's textile motifs, symbols, colors, and techniques using Gemini."""
        prompt = (
            f"For the {culture.title()} culture, provide:\n"
            "- 3 to 5 of the most iconic textile motifs or symbols (with names and meanings if possible)\n"
            "- The traditional color palette (with color names or hex codes)\n"
            "- The typical arrangement style of motifs (e.g., rows, bands, all-over, grid)\n"
            "- Notable textile techniques or materials\n"
            "- One or two 'do's and don'ts' for authentic design\n"
            "Return your answer as a concise, richly descriptive paragraph."
        )
        try:
            details = self.generate_text(prompt)
            return details.strip() if details else ""
        except Exception as e:
            logger.error(f"Error generating culture details for {culture}: {e}")
            return ""

# Global client instance
gemini_client = GeminiClient() 