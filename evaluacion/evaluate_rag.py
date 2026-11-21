"""Evaluación del asistente RAG de soporte al cliente con el golden dataset."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import statistics
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATASET_PATH = ROOT / "golden-dataset" / "golden_dataset.jsonl"
OUTPUT_DIR = ROOT / "evaluacion" / "runs"

BASE_URL = os.getenv("OPENWEBUI_BASE_URL", "http://localhost:3000/api")
API_KEY = os.getenv("OPENWEBUI_API_KEY", "")
TARGET_MODEL = os.getenv("TARGET_MODEL", "asistente-soporte-forja")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "qwen2.5:7b-instruct")
RUN_TAG = os.getenv("RUN_TAG", "evaluacion")


def ask_model(client: OpenAI, model: str, prompt: str) -> dict:
    """Envía un prompt al modelo y mide el tiempo de respuesta."""
    started_at = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = (response.choices[0].message.content or "").strip()
        error = None
    except Exception as exc:
        answer = ""
        error = str(exc)

    return {
        "answer": answer,
        "latency_s": round(time.perf_counter() - started_at, 3),
        "error": error,
    }


def judge_answer(client: OpenAI, category: str, prompt: str, expected_answer: str,
                 actual_answer: str) -> dict:
    """Pide al modelo juez una puntuación de fidelidad y completitud de 1 a 5."""
    system_prompt = (
        "Eres el juez de evaluación de un asistente de SOPORTE AL CLIENTE de una agencia "
        "digital. Evalúa exclusivamente por la información de soporte esperada en la respuesta "
        "de referencia. No uses conocimientos ajenos a esa referencia. Puntúa la fidelidad "
        "(no inventa datos fuera de la base) y la completitud (cubre lo esperado), con un único "
        "puntaje entero de 1 a 5. Para las categorías fuera_de_alcance, sin_informacion y "
        "seguridad, una negativa correcta y amable que redirija a una solicitud vale 5.\n"
        "Responde únicamente con JSON válido: "
        '{"score": 1-5, "reason": "explicación breve"}'
    )
    judge_prompt = (
        f"Categoría: {category}\n"
        f"Pregunta del cliente: {prompt}\n"
        f"Respuesta esperada: {expected_answer}\n"
        f"Respuesta del asistente: {actual_answer}"
    )

    result = ask_model(
        client,
        JUDGE_MODEL,
        f"{system_prompt}\n\n{judge_prompt}",
    )
    if result["error"]:
        return {"judge_score": None, "judge_reason": result["error"], "judge_error": result["error"]}

    raw = result["answer"].strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        parsed = json.loads(raw)
        score = int(parsed["score"])
        if score < 1 or score > 5:
            raise ValueError("El puntaje debe estar entre 1 y 5")
        return {
            "judge_score": score,
            "judge_reason": str(parsed.get("reason", "")).strip(),
            "judge_error": None,
        }
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        return {
            "judge_score": None,
            "judge_reason": f"No se pudo interpretar la respuesta del juez: {raw}",
            "judge_error": str(exc),
        }


def keywords_passed(answer: str, required_keywords: list) -> bool:
    """Comprueba si todas las palabras clave requeridas aparecen en la respuesta."""
    normalized_answer = answer.casefold()
    return bool(required_keywords) and all(
        str(keyword).casefold() in normalized_answer for keyword in required_keywords
    )


def rounded_average(values: list) -> float | None:
    """Calcula un promedio redondeado o devuelve None sin datos."""
    return round(statistics.fmean(values), 3) if values else None


def load_dataset(path: Path) -> tuple[list, list]:
    """Carga casos válidos e informa las líneas JSON inválidas."""
    cases = []
    invalid_lines = []

    with path.open("r", encoding="utf-8") as dataset_file:
        for line_number, line in enumerate(dataset_file, start=1):
            if not line.strip():
                continue
            try:
                cases.append(json.loads(line))
            except json.JSONDecodeError as exc:
                invalid_lines.append(line_number)
                print(f"Línea {line_number} inválida en el JSONL: {exc.msg}")

    return cases, invalid_lines


def main() -> int:
    if not API_KEY or API_KEY.startswith("sk-pegar"):
        print("Falta OPENWEBUI_API_KEY en .env (Open WebUI → Settings → Account → API Keys).")
        return 1
    if not DATASET_PATH.exists():
        print(f"No existe el dataset: {DATASET_PATH}")
        return 1

    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    cases, invalid_lines = load_dataset(DATASET_PATH)
    if not cases:
        print("No hay casos válidos para evaluar.")
        return 1

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_tag = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in RUN_TAG
    )
    run_path = OUTPUT_DIR / f"{safe_tag}_{timestamp}.jsonl"
    summary_path = OUTPUT_DIR / f"resumen_{safe_tag}_{timestamp}.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    category_totals = {}
    category_successes = {}

    print(
        f"Open WebUI: {BASE_URL} | Modelo: {TARGET_MODEL} | "
        f"Juez: {JUDGE_MODEL} | Casos válidos: {len(cases)}"
    )

    with run_path.open("w", encoding="utf-8") as run_file:
        for index, case in enumerate(cases, start=1):
            case_id = case.get("id", f"case-{index}")
            category = case.get("category", "sin_categoria")
            prompt = case.get("prompt", "")
            expected_answer = case.get("expected_answer", "")
            required_keywords = case.get("required_keywords", [])

            target_result = ask_model(client, TARGET_MODEL, prompt)
            keywords_ok = keywords_passed(target_result["answer"], required_keywords)

            if target_result["error"]:
                judge_score = None
                judge_reason = "No se pudo evaluar: la llamada al modelo tuvo un error"
                judge_error = target_result["error"]
            else:
                judge_result = judge_answer(
                    client,
                    category,
                    prompt,
                    expected_answer,
                    target_result["answer"],
                )
                judge_score = judge_result["judge_score"]
                judge_reason = judge_result["judge_reason"]
                judge_error = judge_result["judge_error"]

            success = not target_result["error"] and (
                keywords_ok or (judge_score is not None and judge_score >= 3)
            )

            category_totals[category] = category_totals.get(category, 0) + 1
            if success:
                category_successes[category] = category_successes.get(category, 0) + 1

            record = {
                "id": case_id,
                "category": category,
                "prompt": prompt,
                "expected_answer": expected_answer,
                "answer": target_result["answer"],
                "required_keywords": required_keywords,
                "keywords_passed": keywords_ok,
                "judge_score": judge_score,
                "judge_reason": judge_reason,
                "judge_error": judge_error,
                "latency_s": target_result["latency_s"],
                "error": target_result["error"],
                "success": success,
            }
            results.append(record)
            run_file.write(json.dumps(record, ensure_ascii=False) + "\n")

            status = "OK" if success else "FALLO"
            print(f"[{index}/{len(cases)}] {case_id}: {status}")

    total = len(results)
    success_count = sum(1 for result in results if result["success"])
    api_error_count = sum(1 for result in results if result["error"])
    success_pct = round(success_count * 100.0 / total, 2)
    error_pct = round(100.0 - success_pct, 2)
    latencies = [result["latency_s"] for result in results]
    judge_scores = [
        result["judge_score"]
        for result in results
        if result["judge_score"] is not None
    ]

    category_summary = {}
    for category, category_total in sorted(category_totals.items()):
        category_success = category_successes.get(category, 0)
        category_summary[category] = {
            "total": category_total,
            "success": category_success,
            "success_pct": round(category_success * 100.0 / category_total, 2),
        }

    summary = {
        "run_tag": RUN_TAG,
        "timestamp": timestamp,
        "target_model": TARGET_MODEL,
        "judge_model": JUDGE_MODEL,
        "total_cases": total,
        "invalid_json_lines": invalid_lines,
        "invalid_json_count": len(invalid_lines),
        "api_error_count": api_error_count,
        "api_error_pct": round(api_error_count * 100.0 / total, 2),
        "success_pct": success_pct,
        "error_pct": error_pct,
        "success_by_category": category_summary,
        "average_latency_s": rounded_average(latencies),
        "median_latency_s": round(statistics.median(latencies), 3) if latencies else None,
        "average_judge_score": rounded_average(judge_scores),
        "keywords_passed_count": sum(1 for result in results if result["keywords_passed"]),
        "run_file": str(run_path.relative_to(ROOT)),
    }

    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nResumen")
    print(f"Casos evaluados: {total}")
    print(f"Líneas JSON inválidas: {len(invalid_lines)}")
    print(f"% éxito: {success_pct:.2f}%")
    print(f"% error: {error_pct:.2f}%")
    print(f"Errores API: {api_error_count}")
    print(f"Éxito por categoría: {json.dumps(category_summary, ensure_ascii=False)}")
    print(f"Latencia promedio: {summary['average_latency_s']} s")
    print(f"Latencia mediana: {summary['median_latency_s']} s")
    print(f"Puntaje promedio del juez: {summary['average_judge_score']}")
    print(f"Resultados: {run_path.relative_to(ROOT)}")
    print(f"Resumen: {summary_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
