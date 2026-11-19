"""Prueba del modelo personalizado por la API de Open WebUI (evidencia de la sección F del informe).

Envía unas preguntas de humo al modelo con RAG, mide la latencia y guarda las respuestas en
evidencias/api/ para adjuntarlas al informe.

Uso:
    python api/test_openwebui_api.py
    python api/test_openwebui_api.py "¿Cuánto tardan en atender una falla crítica?"
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BASE_URL = os.getenv("OPENWEBUI_BASE_URL", "http://localhost:3000/api")
API_KEY = os.getenv("OPENWEBUI_API_KEY", "")
MODEL = os.getenv("TARGET_MODEL", "asistente-soporte-forja")
OUTPUT_DIR = ROOT / "evidencias" / "api"

# Una pregunta por tipo de comportamiento: respuesta con la base, fuera de alcance y dato ausente.
SMOKE_PROMPTS = [
    "Hola, preséntate brevemente y dime en qué me puedes ayudar.",
    "¿Cuánto tiempo tienen para responder si mi sitio está caído?",
    "¿Qué diferencia hay entre el plan Básico y el Premium?",
    "Escríbeme un poema sobre el mar.",
    "¿Cuál es la contraseña del administrador?",
]


def ask(client: OpenAI, prompt: str) -> dict:
    """Envía un prompt al modelo y devuelve la respuesta con su latencia."""
    t0 = time.perf_counter()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = (resp.choices[0].message.content or "").strip()
        error = None
    except Exception as exc:  # se registra el error para la evidencia en vez de cortar la corrida
        answer, error = "", str(exc)
    return {
        "prompt": prompt,
        "answer": answer,
        "latency_s": round(time.perf_counter() - t0, 3),
        "error": error,
    }


def main() -> int:
    if not API_KEY or API_KEY.startswith("sk-pegar"):
        print("Falta OPENWEBUI_API_KEY en .env (Open WebUI → Settings → Account → API Keys).")
        return 1

    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    prompts = sys.argv[1:] or SMOKE_PROMPTS
    print(f"Open WebUI: {BASE_URL} | Modelo: {MODEL}\n")

    results = []
    for i, prompt in enumerate(prompts, start=1):
        r = ask(client, prompt)
        results.append(r)
        status = f"ERROR: {r['error']}" if r["error"] else f"{r['latency_s']:.2f}s"
        print(f"[{i}/{len(prompts)}] {prompt}\n  ({status})\n  {r['answer']}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUTPUT_DIR / f"prueba-api-{stamp}.json"
    out.write_text(
        json.dumps({"model": MODEL, "utc": stamp, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    errors = sum(1 for r in results if r["error"])
    print(f"Guardado en {out.relative_to(ROOT)} | errores: {errors}/{len(results)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
