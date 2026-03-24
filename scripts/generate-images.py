#!/usr/bin/env python3
"""
Generate images for Kirameki Farm LP using Google's Gemini API (Imagen 3).

Usage:
    export GEMINI_API_KEY="your-api-key"
    python3 scripts/generate-images.py

Or pass the key as an argument:
    python3 scripts/generate-images.py --api-key YOUR_KEY

Requirements:
    pip install google-generativeai Pillow
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    from PIL import Image
    import io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# Output directory
IMAGES_DIR = Path(__file__).parent.parent / "public" / "images"

# Image prompts: (filename, prompt, aspect_ratio_hint)
IMAGE_PROMPTS = [
    (
        "hero.webp",
        "A beautiful Japanese fruit orchard at golden hour, apple and grape trees in rows, "
        "mountains (South Alps) visible in the background, warm sunlight filtering through leaves, "
        "Nagano Prefecture landscape, cinematic photography style, 16:9 aspect ratio",
        "16:9",
    ),
    (
        "knowledge.webp",
        "Close-up of a Japanese farmer's hands carefully inspecting a red apple on a branch, "
        "with a digital thermometer and notebook visible, soft natural lighting, documentary photography style",
        "4:3",
    ),
    (
        "climate.webp",
        "Panoramic view of Takayama Village in Nagano Prefecture Japan from 700m altitude, "
        "misty mountains, dramatic sky with clouds, lush green orchards in foreground, landscape photography",
        "2:1",
    ),
    (
        "soil.webp",
        "Rich dark soil in a Japanese orchard, close-up with visible organic matter and roots, "
        "earthworms visible, soft morning light, macro photography style",
        "4:3",
    ),
    (
        "philosophy.webp",
        "A lone Japanese farmer walking through apple orchard rows at dawn, silhouette against "
        "morning light, peaceful and contemplative mood, wide angle, cinematic",
        "3:2",
    ),
    (
        "marquee-1.webp",
        "Ripe red apples on tree branch with water droplets, bokeh background of green leaves, natural light",
        "3:2",
    ),
    (
        "marquee-2.webp",
        "Green Shine Muscat grapes hanging on vine, translucent in sunlight, Japanese vineyard",
        "3:2",
    ),
    (
        "marquee-3.webp",
        "Japanese farmer pruning apple tree in winter, snow-capped mountains background",
        "3:2",
    ),
    (
        "marquee-4.webp",
        "Close-up of apple blossoms in spring, pink and white flowers, soft bokeh",
        "3:2",
    ),
    (
        "marquee-5.webp",
        "Wooden crate full of freshly harvested apples, rustic farmhouse background",
        "3:2",
    ),
    (
        "marquee-6.webp",
        "Sunset over grape vineyard in Japanese countryside, golden hour, rows of vines",
        "3:2",
    ),
    (
        "shinano-sweet.webp",
        "Beautiful red Shinano Sweet apple, studio photography on natural wood surface, "
        "warm lighting, food photography style",
        "1:1",
    ),
    (
        "shine-muscat.webp",
        "Gorgeous green Shine Muscat grapes bunch, studio photography, water droplets, elegant presentation",
        "1:1",
    ),
    (
        "sun-fuji.webp",
        "Sun Fuji apple cut in half showing honey core (蜜入り), studio photography, warm lighting",
        "1:1",
    ),
    (
        "kyoho.webp",
        "Dark purple Kyoho grapes bunch, studio photography, dramatic lighting, Japanese premium fruit",
        "1:1",
    ),
    (
        "village.webp",
        "Aerial view of Takayama Village Nagano Japan, patchwork of orchards and rice fields, "
        "mountains surrounding, autumn colors",
        "3:2",
    ),
]


def generate_with_genai_sdk(api_key: str):
    """Generate images using the google-generativeai Python SDK."""
    if not HAS_GENAI:
        print("ERROR: google-generativeai package not installed.")
        print("Install with: pip install google-generativeai Pillow")
        sys.exit(1)

    genai.configure(api_key=api_key)

    # Use Imagen 3 model
    imagen_model = genai.ImageGenerationModel("imagen-3.0-generate-002")

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for i, (filename, prompt, aspect_ratio) in enumerate(IMAGE_PROMPTS, 1):
        output_path = IMAGES_DIR / filename
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}] Generating: {filename}")
        print(f"  Prompt: {prompt[:80]}...")

        try:
            result = imagen_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            )

            if result.images:
                image_data = result.images[0]
                # Save as webp
                if HAS_PIL:
                    img = Image.open(io.BytesIO(image_data._image_bytes))
                    img.save(str(output_path), "WEBP", quality=85)
                else:
                    # Fallback: save as PNG if PIL not available
                    png_path = output_path.with_suffix(".png")
                    with open(png_path, "wb") as f:
                        f.write(image_data._image_bytes)
                    print(f"  Saved as PNG (install Pillow for WebP): {png_path}")
                    continue

                print(f"  Saved: {output_path}")
            else:
                print(f"  WARNING: No image generated for {filename}")

        except Exception as e:
            print(f"  ERROR generating {filename}: {e}")
            continue

    print(f"\nDone! Images saved to {IMAGES_DIR}/")


def generate_with_gemini_api(api_key: str):
    """
    Alternative: Generate images using Gemini's generateContent endpoint
    with image generation capability. This is a fallback if Imagen model
    is not available.
    """
    import urllib.request

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"

    for i, (filename, prompt, _) in enumerate(IMAGE_PROMPTS, 1):
        output_path = IMAGES_DIR / filename
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}] Generating: {filename}")
        print(f"  Prompt: {prompt[:80]}...")

        payload = json.dumps({
            "contents": [{"parts": [{"text": f"Generate a high quality photograph: {prompt}"}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        }).encode("utf-8")

        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            # Extract image from response
            candidates = data.get("candidates", [])
            for candidate in candidates:
                parts = candidate.get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        image_bytes = base64.b64decode(part["inlineData"]["data"])
                        mime = part["inlineData"].get("mimeType", "image/png")

                        if HAS_PIL:
                            img = Image.open(io.BytesIO(image_bytes))
                            img.save(str(output_path), "WEBP", quality=85)
                            print(f"  Saved: {output_path}")
                        else:
                            ext = ".png" if "png" in mime else ".jpg"
                            fallback = output_path.with_suffix(ext)
                            with open(fallback, "wb") as f:
                                f.write(image_bytes)
                            print(f"  Saved (raw): {fallback}")
                        break
                else:
                    continue
                break
            else:
                print(f"  WARNING: No image data in response for {filename}")

        except Exception as e:
            print(f"  ERROR generating {filename}: {e}")
            continue

    print(f"\nDone! Images saved to {IMAGES_DIR}/")


def generate_with_curl_imagen(api_key: str):
    """
    Alternative: Generate images using Imagen 3 predict endpoint via urllib.
    """
    import urllib.request

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

    for i, (filename, prompt, aspect_ratio) in enumerate(IMAGE_PROMPTS, 1):
        output_path = IMAGES_DIR / filename
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}] Generating: {filename}")
        print(f"  Prompt: {prompt[:80]}...")

        payload = json.dumps({
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": aspect_ratio,
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            predictions = data.get("predictions", [])
            if predictions:
                image_b64 = predictions[0].get("bytesBase64Encoded", "")
                if image_b64:
                    image_bytes = base64.b64decode(image_b64)
                    if HAS_PIL:
                        img = Image.open(io.BytesIO(image_bytes))
                        img.save(str(output_path), "WEBP", quality=85)
                        print(f"  Saved: {output_path}")
                    else:
                        fallback = output_path.with_suffix(".png")
                        with open(fallback, "wb") as f:
                            f.write(image_bytes)
                        print(f"  Saved (PNG fallback): {fallback}")
                else:
                    print(f"  WARNING: No image bytes in response for {filename}")
            else:
                print(f"  WARNING: No predictions in response for {filename}")

        except Exception as e:
            print(f"  ERROR generating {filename}: {e}")
            continue

    print(f"\nDone! Images saved to {IMAGES_DIR}/")


def main():
    parser = argparse.ArgumentParser(description="Generate images for Kirameki Farm LP")
    parser.add_argument("--api-key", help="Gemini API key (or set GEMINI_API_KEY / GOOGLE_API_KEY env var)")
    parser.add_argument(
        "--method",
        choices=["sdk", "gemini", "imagen"],
        default="imagen",
        help="Generation method: 'sdk' (google-generativeai), 'gemini' (generateContent), 'imagen' (predict endpoint). Default: imagen",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: No API key provided.")
        print("Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable,")
        print("or pass --api-key YOUR_KEY")
        sys.exit(1)

    print(f"Kirameki Farm LP — Image Generator")
    print(f"Method: {args.method}")
    print(f"Output: {IMAGES_DIR}/")
    print(f"Images to generate: {len(IMAGE_PROMPTS)}")

    if args.method == "sdk":
        generate_with_genai_sdk(api_key)
    elif args.method == "gemini":
        generate_with_gemini_api(api_key)
    elif args.method == "imagen":
        generate_with_curl_imagen(api_key)


if __name__ == "__main__":
    main()
