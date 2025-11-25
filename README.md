# Splice Safari

A playful web app that spins two animal roulette wheels and generates a quirky AI-style poster of the mashed-up species.

## Running the app

Install dependencies and run the server:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here  # required for real AI images
python app.py  # defaults to http://localhost:8000
```

On Windows PowerShell, set the key for the current session with:

```powershell
$env:OPENAI_API_KEY="your_key_here"
python app.py
```

You can also drop a `.env` file (same folder as `app.py`) containing `OPENAI_API_KEY=your_key_here` and the server will load it
automatically at startup.

If `openai` isn't installed or the key/base URL are missing, the server will stay up and fall back to the built-in SVG illustrator instead of erroring out. The OpenAI status pill in the UI will call this out with a short reason (e.g., "Missing 'openai' package" or "OPENAI_API_KEY not set") so you know what to fix.

Image responses work with both base64 (`b64_json`) and hosted URLs returned by the OpenAI Images API. The server automatically downloads and inlines URL responses so the browser can render them without CORS headaches, and avoids the deprecated `response_format` parameter that can trigger `unknown_parameter` errors on newer endpoints.

Open the printed URL in your browser and click **Spin the wheels** to generate a new creature. The API endpoint lives at `/api/spin` and returns the selected animals, the blended species name, and a base64-encoded PNG (AI) or SVG (fallback) poster. The OpenAI model defaults to `gpt-image-1`; override with `OPENAI_IMAGE_MODEL` or point at a compatible proxy with `OPENAI_BASE_URL`.

The UI now reports whether the server can reach the configured OpenAI model via a status pill beneath the spin button so you can quickly tell if you're seeing AI renderings or the built-in illustrated posters.
