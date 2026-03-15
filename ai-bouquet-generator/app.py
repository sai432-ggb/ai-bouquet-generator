import os
import base64
import json
import re
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_bouquet_description(user_prompt: str, occasion: str, style: str, colors: list) -> dict:
    """Use Gemini to generate a detailed bouquet description and prompt."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_context = f"""You are a master florist and floral designer with 20+ years of experience.
    Generate a detailed, poetic bouquet design for the following request.
    
    User Request: {user_prompt}
    Occasion: {occasion}
    Style: {style}
    Preferred Colors: {', '.join(colors) if colors else 'No preference'}
    
    Respond with a JSON object containing:
    {{
        "bouquet_name": "Creative name for the bouquet",
        "description": "Poetic 2-3 sentence description of the bouquet",
        "flowers": ["list", "of", "specific", "flowers"],
        "color_palette": ["specific", "color", "names"],
        "arrangement_style": "How it's arranged",
        "symbolism": "What this bouquet represents",
        "care_tips": "Brief care instructions",
        "image_prompt": "Detailed image generation prompt for creating a photorealistic bouquet image"
    }}
    
    Return ONLY valid JSON, no markdown, no explanation."""

    response = model.generate_content(system_context)
    text = response.text.strip()

    # Clean up markdown fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "bouquet_name": "Artisan Garden Bouquet",
            "description": user_prompt,
            "flowers": ["Roses", "Lilies", "Baby's Breath"],
            "color_palette": colors or ["Pink", "White", "Green"],
            "arrangement_style": style,
            "symbolism": "Love and beauty",
            "care_tips": "Keep in cool water, change water every 2 days.",
            "image_prompt": f"A beautiful {style} bouquet with {', '.join(colors or ['mixed'])} flowers, professional photography, soft natural lighting",
        }


def generate_bouquet_image(image_prompt: str) -> str | None:
    """Generate bouquet image using Gemini Imagen."""
    try:
        # Use Gemini's image generation
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        full_prompt = f"""Create a photorealistic image of: {image_prompt}
        Style: professional floral photography, soft natural lighting, white or soft bokeh background, 
        high detail, beautiful composition, magazine quality."""
        
        response = model.generate_content(
            full_prompt,
            generation_config={"response_mime_type": "image/png"}
        )
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return base64.b64encode(part.inline_data.data).decode('utf-8')
    except Exception as e:
        print(f"Image generation error: {e}")
    
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_prompt = data.get("prompt", "A romantic bouquet")
    occasion = data.get("occasion", "General")
    style = data.get("style", "Classic")
    colors = data.get("colors", [])

    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured. Please set it in your .env file."}), 400

    try:
        # Step 1: Generate bouquet description
        bouquet_data = generate_bouquet_description(user_prompt, occasion, style, colors)

        # Step 2: Try to generate image
        image_base64 = None
        if bouquet_data.get("image_prompt"):
            image_base64 = generate_bouquet_image(bouquet_data["image_prompt"])

        return jsonify({
            "success": True,
            "bouquet": bouquet_data,
            "image": image_base64,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
