# Evaluación

<!-- Qué va en esta carpeta y qué debe medir el responsable (punto 5 de la actividad). -->

**Responsable:** Integrante 5 (@Andres-Duqu).

## Qué va aquí

- `evaluate_rag.py`: adaptado del ejemplo de clase. Lee `../golden-dataset/golden_dataset.jsonl`
  y el `.env` de la raíz. El juez debe hablar de soporte al cliente, no de fitness.
- `runs/`: un `.jsonl` por corrida, nombrado con `RUN_TAG` (por ejemplo `v1_chunk500_ov50`).
  **Sí se sube**: es la evidencia.
- `resultados.md`: tabla comparativa de corridas con casos, errores, % de éxito por palabras
  clave, % de éxito por juez (puntaje de 3 o más), puntaje promedio, latencia promedio y mediana,
  y % de error. La meta es **70 % de eficiencia o más**.

## Cómo correrlo

```bash
python evaluacion/evaluate_rag.py
RUN_TAG=v2_chunk400_ov40 python evaluacion/evaluate_rag.py
```

Si la primera corrida no llega al 70 %, ajustar el corte, el prompt o las palabras clave, volver
a correr y documentar qué cambió. Esa comparación también va en el informe.

## Estado de la tarea

- [x] Script adaptado: `evaluate_rag.py`.
- [x] Corrida final del golden dataset: 50 casos, 70 % de éxito.
- [x] Documento `resultados.md`.
- [x] Análisis F.3 del informe.
- [ ] PR de la tarea.

Responsable: Integrante 5, Andrés Felipe (`@Andres-Duqu`).
