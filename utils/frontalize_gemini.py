import os
import traceback
from google import genai

API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not API_KEY:
    API_KEY = "AIzaSyCGVcc4OclgLrTHc7HLQw-sDyTKMph6VHk"  # put key if needed

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.0-flash-exp-image-generation"  # ONLY image model supported

MAX_REF_IMAGES = 6


def _img_part(path):
    with open(path, "rb") as f:
        return {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": f.read()
            }
        }


def frontalize_with_gemini(detected_face_path: str, output_dir: str, ref_image_paths=None):
    if ref_image_paths is None:
        ref_image_paths = []

    try:
        # -------------------------
        # Build prompt + image parts
        # -------------------------
        parts = [{
            "text": (
                "You are an identity-preserving face frontalization AI. "
                "Input: first image = detected face from video. Other images = same person reference photos. "
                "Output: generate a clear 512x512 realistic FRONTAL face. "
                "Do not beautify. Keep identity EXACT."
            )
        }]

        # detected face
        parts.append(_img_part(detected_face_path))

        # reference images
        for ref in ref_image_paths[:MAX_REF_IMAGES]:
            parts.append(_img_part(ref))

        content = [{"role": "user", "parts": parts}]

        # -------------------------
        # Gemini image generation call
        # -------------------------
        try:
            result = client.models.generate_content(
                model=MODEL,
                contents=content
            )
        except Exception as e:
            print("[Gemini] API ERROR:", e)
            traceback.print_exc()
            return None

        # -------------------------
        # Extract image bytes
        # -------------------------
        out_bytes = None
        try:
            candidate = result.candidates[0]
            for p in candidate.content.parts:
                if hasattr(p, "inline_data") and hasattr(p.inline_data, "data"):
                    out_bytes = p.inline_data.data
                    break

            if out_bytes is None:
                print("[Gemini] ERROR: No image returned.")
                return None

        except Exception as e:
            print("[Gemini] PARSE ERROR:", e)
            traceback.print_exc()
            return None

        # -------------------------
        # Save output
        # -------------------------
        os.makedirs(output_dir, exist_ok=True)
        out_name = os.path.basename(detected_face_path).replace(".jpg", "_frontal.jpg")
        out_path = os.path.join(output_dir, out_name)

        with open(out_path, "wb") as f:
            f.write(out_bytes)

        print("[Gemini] Saved:", out_path)
        return out_path

    except Exception as e:
        print("[Gemini] Unexpected error:", e)
        traceback.print_exc()
        return None
