# ---------------------------------------------------------
# TEST IMAGEN 4.0 WITH YOUR GOOGLE GEMINI SDK VERSION
# ---------------------------------------------------------

from google import genai

API_KEY = "AIzaSyCupzRTdM68y5FmH7z-Is_F-jqiwEhNTAY"
MODEL_NAME = "models/imagen-4.0-ultra-generate-001"

def test_imagen():
    try:
        print("🔍 Checking API key...")
        client = genai.Client(api_key=API_KEY)

        print("📡 Fetching available models...")
        models = client.models.list()

        model_names = [m.name for m in models]
        print("\n🧾 Available Models:")
        for m in model_names:
            print(" -", m)

        if MODEL_NAME not in model_names:
            print(f"\n❌ ERROR: Model '{MODEL_NAME}' not found!")
            return

        print(f"\n✅ Model '{MODEL_NAME}' exists.")

        print("\n🖼️ Testing image generation using YOUR SDK method...")

        # ⭐ The only method your SDK supports:
        result = client.generate_image(
            model=MODEL_NAME,
            prompt="A red apple on a wooden table"
        )

        image_bytes = result.image  # only field returned in your SDK

        with open("test_output.png", "wb") as f:
            f.write(image_bytes)

        print("🎉 SUCCESS: Image generated → test_output.png")

    except Exception as e:
        print("\n❌ FATAL ERROR:", e)


if __name__ == "__main__":
    test_imagen()
