# Splice Safari

A playful web app that spins two animal roulette wheels and generates a quirky AI-style poster of the mashed-up species.

## Running the app

This project uses only the Python standard library for the backend server and vanilla HTML/CSS/JS on the frontend.

```bash
python app.py  # defaults to http://localhost:8000
```

Open the printed URL in your browser and click **Spin the wheels** to generate a new creature. The API endpoint lives at `/api/spin` and returns the selected animals, the blended species name, and a base64-encoded SVG poster.
