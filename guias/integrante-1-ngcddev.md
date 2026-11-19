# Guía · Integrante 1 · @ngcddev

<!-- Pasos del coordinador: pruebas por API, integración del informe y entrega (issues #8 y #11). -->

**Tu parte:** coordinar y revisar los PR, hacer las pruebas por API, armar el informe y entregar.
El repositorio, el entorno Docker y el script de API ya están hechos.

## Durante la semana

- Revisar y fusionar los PR del equipo (*Merge pull request → Create a merge commit*).
- Seguir el orden: **la base de Mesiahs es el cuello de botella**. Si se atrasa, todos esperan.
- Cada uno debe tener **varios commits propios**. Revisar *Insights → Contributors* a mitad de semana.

## Issue #8 · Pruebas por API e interfaz (cuando exista el modelo)

```powershell
python api/test_openwebui_api.py
```

- El JSON queda en `evidencias/api/`. Tomar una captura de la terminal: `evidencias/api/prueba-api.png`.
- Hacer las mismas 5 preguntas en el chat de Open WebUI y capturarlas.
- Escribir tu parte de `informe/secciones/f1-pruebas-ui-api.md`.

## Issue #11 · Informe y entrega (al final)

1. Escribir `a-portada.md` (título, curso, docente, integrantes y fecha) y `c-introduccion.md`.
2. Unir las secciones en un solo documento (Word o Google Docs): portada, **índice automático** y
   secciones C a G, con las imágenes.
3. Exportar a `informe/Informe-modelo-rag-CloudOps-Client-Hub.pdf` y subirlo en un PR.
4. Comprobar que *Insights → Contributors* muestre a los 5 y que la tabla de aportes del README esté completa.
5. Enviar **un solo correo** a profesordiegorivera@gmail.com con el enlace del repositorio.

## Prompt para tu IA (introducción)

```text
Redacta la introducción (2 o 3 párrafos, en español formal) de un informe académico titulado
"Informe del modelo RAG — CloudOps Client Hub". Trata de un asistente de soporte y PQRS para los
clientes de una agencia digital ficticia (Forja Digital), construido con Ollama + Open WebUI, con
una base de conocimiento propia, un modelo personalizado (qwen2.5:3b-instruct) con system prompt y
políticas, y evaluado con un golden dataset de 50 casos usando métricas de latencia, palabras
clave y un modelo juez. Explica de qué trata el documento y cómo está organizado
(problema, definición del modelo, implementación y pruebas, conclusiones).
```
