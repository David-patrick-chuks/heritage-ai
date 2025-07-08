# HeritageAI - Robust API Client with Retry Logic

## 🚀 Enhanced Reliability Features

The HeritageAI platform now includes a robust API client with automatic retry logic and support for multiple Gemini API keys to ensure high availability and reliability.

## 🔑 Multiple API Key Setup

### 1. Environment Configuration

Create a `.env` file in the `mvp_ai` directory with multiple API keys:

```bash
# Primary API Key (for backward compatibility)
GEMINI_API_KEY=your_primary_gemini_api_key_here

# Multiple API Keys for redundancy (recommended)
GEMINI_API_KEY_1=your_first_gemini_api_key_here
GEMINI_API_KEY_2=your_second_gemini_api_key_here
GEMINI_API_KEY_3=your_third_gemini_api_key_here

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY_429=2000
RETRY_DELAY_503=3000
RETRY_DELAY_500=2000
```

### 2. How Multiple Keys Work

- **Automatic Key Rotation**: When one key hits rate limits, the system automatically switches to the next available key
- **Fallback Support**: If multiple keys aren't configured, it falls back to the single `GEMINI_API_KEY`
- **Load Balancing**: Keys are used in round-robin fashion when rate limits are hit

## 🔄 Retry Logic

### Error Handling

The system automatically handles these error types:

| Error Type | Action | Delay |
|------------|--------|-------|
| **429 (Rate Limit)** | Switch API key | 2 seconds |
| **503 (Service Unavailable)** | Retry with same key | 3 seconds |
| **500 (Internal Server Error)** | Retry with same key | 2 seconds |
| **Timeout** | Retry with same key | 2 seconds |

### Retry Configuration

```bash
MAX_RETRIES=3          # Maximum retry attempts per request
RETRY_DELAY_429=2000   # Delay for rate limit errors (ms)
RETRY_DELAY_503=3000   # Delay for service unavailable (ms)
RETRY_DELAY_500=2000   # Delay for internal server errors (ms)
```

## 🧪 Testing the Setup

Run the test suite to verify your configuration:

```bash
python test_retry.py
```

This will test:
- ✅ API key loading
- ✅ Text generation with retry logic
- ✅ Image generation with retry logic
- ✅ Error handling

## 📊 Usage Examples

### Basic Usage (No Changes Required)

```python
from imagegen_gemini import generate_pattern_image
from gemini_notes import generate_cultural_note

# These now automatically use retry logic
image_path = generate_pattern_image('yoruba', 'Traditional pattern')
cultural_note = generate_cultural_note('yoruba')
```

### Direct Client Usage

```python
from gemini_client import gemini_client

# Generate image with automatic retry
image_path = gemini_client.generate_image(
    prompt="Traditional Yoruba pattern",
    sample_count=1,
    filename="yoruba_pattern.png"
)

# Generate text with automatic retry
text = gemini_client.generate_text("Explain Yoruba culture")
```

## 🎯 Benefits

1. **High Availability**: Multiple API keys ensure service continuity
2. **Automatic Recovery**: No manual intervention needed for temporary failures
3. **Rate Limit Handling**: Seamless switching between keys when limits are hit
4. **Backward Compatibility**: Existing code continues to work without changes
5. **Configurable**: Easy to adjust retry behavior via environment variables

## 🔧 Troubleshooting

### Common Issues

1. **No API Keys Found**
   ```
   ValueError: No Gemini API keys found in environment variables
   ```
   **Solution**: Ensure at least one API key is set in `.env`

2. **All Keys Rate Limited**
   ```
   ❌ Maximum retry attempts (3) reached
   ```
   **Solution**: Wait for rate limits to reset or add more API keys

3. **Service Unavailable**
   ```
   ⏳ Service is unavailable. Retrying in 3 seconds...
   ```
   **Solution**: This is normal - the system will automatically retry

### Monitoring

The system provides detailed logging:
- 🔄 Key switching events
- ⏳ Retry attempts and delays
- ❌ Final failures after all retries
- ✅ Successful requests

## 🚀 Production Deployment

For production use, we recommend:

1. **Multiple API Keys**: Use at least 3 different API keys
2. **Monitoring**: Set up alerts for repeated failures
3. **Rate Limiting**: Monitor usage across all keys
4. **Backup Keys**: Keep additional keys ready for emergencies

---

**Next Steps**: Update your `.env` file with multiple API keys and test the system with `python test_retry.py` 