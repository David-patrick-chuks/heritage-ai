from gemini_client import gemini_client

PROMPT_TEMPLATE = (
    "Provide a short, respectful cultural note (2-3 sentences) about the {culture} culture, "
    "focusing on its visual art, patterns, or symbolism. The note should be suitable for designers using generated assets."
)

def generate_cultural_note(culture):
    """Generate cultural note using the robust Gemini client with retry logic"""
    prompt = PROMPT_TEMPLATE.format(culture=culture.title())
    
    try:
        # Use the robust client with retry logic
        note = gemini_client.generate_text(prompt)
        return note
    except Exception as e:
        return f"[Gemini API error: {e}] Placeholder note for {culture.title()}." 