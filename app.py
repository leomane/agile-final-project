import base64
import json
import os
import random
import socketserver
from http.server import SimpleHTTPRequestHandler
from typing import Optional, Tuple

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(os.getenv("OPENAI_API_KEY"))


def load_dotenv_if_present() -> None:
    """Load environment variables from a local .env file if one exists.

    This keeps the app dependency-free while still supporting the common
    pattern of storing API keys in a .env file. Values already set in the
    process environment are left untouched.
    """

    dotenv_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(dotenv_path):
        return

    loaded_keys = []
    try:
        with open(dotenv_path, "r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                key = key.strip()
                if not key or key in os.environ:
                    continue
                value = value.strip().strip("'\"")
                os.environ[key] = value
                loaded_keys.append(key)
    except OSError as exc:  # pragma: no cover - non-critical helper
        print(f"Warning: Unable to read {dotenv_path}: {exc}")
    else:
        if loaded_keys:
            print(f"Loaded {len(loaded_keys)} values from .env: {', '.join(loaded_keys)}")

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None

load_dotenv_if_present()

ANIMALS = [
    "Lion",
    "Elephant",
    "Penguin",
    "Kangaroo",
    "Giraffe",
    "Panda",
    "Koala",
    "Falcon",
    "Octopus",
    "Dolphin",
    "Crocodile",
    "Armadillo",
    "Rabbit",
    "Hedgehog",
    "Otter",
    "Zebra",
    "Hippo",
    "Parrot",
    "Cheetah",
    "Meerkat",
    "Chameleon",
    "Wolf",
    "Fennec Fox",
    "Capybara",
    "Moose",
]

ADJECTIVES = [
    "Giggly",
    "Sneaky",
    "Glittery",
    "Turbo",
    "Cosmic",
    "Whimsical",
    "Neon",
    "Electric",
    "Dizzy",
    "Galactic",
]

PUNCHLINES = [
    "Certified chaos on paws",
    "Banned from every zoo talent show",
    "Eats only gourmet snacks and compliments",
    "Can and will steal your picnic blanket",
    "World champion of awkward high-fives",
    "Part-time lifeguard, full-time menace",
    "Possesses questionable superpowers",
    "Believes it invented jazz",
    "Won't share its playlists",
    "Makes its own sound effects",
]

OPENAI_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")


def openai_available() -> bool:
    return OpenAI is not None and bool(os.environ.get("OPENAI_API_KEY", "").strip())


def openai_status() -> Tuple[bool, str]:
    if OpenAI is None:
        return False, "Missing 'openai' package (pip install openai)"
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return False, "OPENAI_API_KEY not set (export/set it or place it in .env)"
    return True, "Configured"


def make_openai_client() -> Optional[OpenAI]:
    if OpenAI is None:
        print("OpenAI client unavailable: package not installed. Serving fallback art.")
        return None
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def mash_name(animal_a: str, animal_b: str) -> str:
    start = animal_a[:3].rstrip().capitalize()
    end = animal_b[-3:].lstrip().capitalize()
    adjective = random.choice(ADJECTIVES)
    return f"{adjective} {start}{end}"


def palette_for_animal(animal: str) -> Tuple[int, int, int]:
    random.seed(hash(animal) & 0xFFFFFFFF)
    return (
        random.randint(70, 230),
        random.randint(60, 210),
        random.randint(80, 240),
    )


def svg_block(x: int, width: int, animal: str, color: Tuple[int, int, int]) -> str:
    r, g, b = color
    label = animal[:8]
    return f"""
    <g transform=\"translate({x},0)\">
      <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"220\" rx=\"22\" fill=\"rgba({r},{g},{b},0.82)\" stroke=\"rgba(10,10,16,0.4)\" stroke-width=\"6\"/>
      <text x=\"{width/2}\" y=\"120\" font-size=\"52\" fill=\"#f8fafc\" font-weight=\"800\" text-anchor=\"middle\" font-family=\"'Inter','Segoe UI',system-ui,sans-serif\">{label}</text>
      <text x=\"{width/2}\" y=\"160\" font-size=\"22\" fill=\"#cbd5e1\" text-anchor=\"middle\" font-family=\"'Inter','Segoe UI',system-ui,sans-serif\">DNA donor</text>
    </g>
    """


def generate_svg(animal_a: str, animal_b: str, species_name: str) -> str:
    width = 900
    height = 500
    left_color = palette_for_animal(animal_a)
    right_color = palette_for_animal(animal_b)
    flavor_line = random.choice(PUNCHLINES)

    svg = f"""
    <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\" role=\"img\" aria-label=\"Mashup of {animal_a} and {animal_b}\">
      <defs>
        <linearGradient id=\"bg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">
          <stop offset=\"0%\" stop-color=\"rgba({left_color[0]},{left_color[1]},{left_color[2]},0.9)\" />
          <stop offset=\"100%\" stop-color=\"rgba({right_color[0]},{right_color[1]},{right_color[2]},0.9)\" />
        </linearGradient>
        <filter id=\"grain\"> <feTurbulence type=\"fractalNoise\" baseFrequency=\"0.8\" numOctaves=\"2\" stitchTiles=\"stitch\"/> <feColorMatrix type=\"saturate\" values=\"0.2\"/> <feComponentTransfer> <feFuncR type=\"linear\" slope=\"0.4\"/> <feFuncG type=\"linear\" slope=\"0.4\"/> <feFuncB type=\"linear\" slope=\"0.4\"/> </feComponentTransfer> <feBlend in=\"SourceGraphic\" mode=\"overlay\"/> </filter>
      </defs>
      <rect width=\"100%\" height=\"100%\" fill=\"url(#bg)\" />
      <g filter=\"url(#grain)\">{svg_block(40, 300, animal_a, left_color)}{svg_block(560, 300, animal_b, right_color)}</g>
      <g transform=\"translate(40,300)\">
        <rect width=\"820\" height=\"160\" rx=\"26\" fill=\"rgba(12, 15, 35, 0.62)\" stroke=\"rgba(15,15,25,0.8)\" stroke-width=\"6\"/>
        <text x=\"26\" y=\"70\" font-size=\"54\" fill=\"#e5e7eb\" font-weight=\"800\" font-family=\"'Inter','Segoe UI',system-ui,sans-serif\">{species_name}</text>
        <text x=\"26\" y=\"116\" font-size=\"24\" fill=\"#cbd5e1\" font-family=\"'Inter','Segoe UI',system-ui,sans-serif\">{flavor_line}</text>
      </g>
    </svg>
    """
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def generate_ai_image(animal_a: str, animal_b: str, species_name: str) -> Tuple[str, str]:
    prompt = (
        "Create a bright, imaginative poster illustration of a fictional animal that "
        f"combines a {animal_a} and a {animal_b}. Focus on a friendly, whimsical style with "
        "bold colors, studio lighting, and a simple background. Include a small caption of "
        f"the name '{species_name}' in the lower area."
    )
    client = make_openai_client()
    if client:
        try:
            response = client.images.generate(
                model=OPENAI_MODEL,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                response_format="b64_json",
                n=1,
            )
            image_b64 = response.data[0].b64_json
            if image_b64:
                return f"data:image/png;base64,{image_b64}", "ai"
            print("OpenAI image generation returned no base64 payload; using fallback SVG.")
        except Exception as exc:  # noqa: BLE001
            print(f"OpenAI image generation failed, falling back to SVG: {exc}")
    else:
        available, reason = openai_status()
        print(f"OpenAI client unavailable; fallback illustrator engaged. Reason: {reason}")
    return generate_svg(animal_a, animal_b, species_name), "fallback"


class MashupHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/templates/index.html"
            return super().do_GET()

        if self.path == "/api/config":
            available, reason = openai_status()
            payload = {
                "openaiConfigured": available,
                "model": OPENAI_MODEL if available else None,
                "reason": reason,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/spin":
            primary, secondary = random.sample(ANIMALS, 2)
            species_name = mash_name(primary, secondary)
            image_data, source = generate_ai_image(primary, secondary, species_name)
            payload = {
                "animals": [primary, secondary],
                "speciesName": species_name,
                "imageData": image_data,
                "imageSource": source,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        return  # Silence noisy default logging


def run_server(port: int = 8000) -> None:
    with socketserver.TCPServer(("", port), MashupHandler) as httpd:
        print(f"Serving Splice Safari on http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_server(port)
