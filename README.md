# Splice Safari

A playful web app that spins two animal roulette wheels and generates a quirky AI-style poster of the mashed-up species.

## Running the app

Install dependencies and run the server:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here  # required for real AI images
python app.py  # defaults to http://localhost:8000
```

Open the printed URL in your browser and click **Spin the wheels** to generate a new creature. The API endpoint lives at `/api/spin` and returns the selected animals, the blended species name, and a base64-encoded PNG (AI) or SVG (fallback) poster. The OpenAI model defaults to `gpt-image-1`; override with `OPENAI_IMAGE_MODEL` or point at a compatible proxy with `OPENAI_BASE_URL`.
