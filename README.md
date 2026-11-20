# Asistente RAG de soporte — CloudOps Client Hub

<!-- README principal del repositorio de la Actividad 2 del Módulo 6 (servicio de IA generativa con RAG). -->

Asistente de **soporte y PQRS** para los clientes de **Forja Digital**, la agencia ficticia del
proyecto integrador [CloudOps Client Hub](https://github.com/ngcddev/CloudOps). Responde preguntas de las PyMEs
(planes, tiempos de atención, prioridades, estados de una solicitud, qué significa un aviso del
portal) usando **solo** la base de conocimiento de este repositorio.

Corre en local: **Ollama + Open WebUI** con una base de conocimiento (RAG) y un modelo
personalizado. Ningún dato sale a servicios de IA externos.

> Actividad 2 · Módulo 6 · Diplomado CloudForge AI 5.0 · Docente: Diego Fernando Rivera Vásquez.
> Basado en el ejemplo de clase [FerchoRV/ejemplo-rag-openwebui](https://github.com/FerchoRV/ejemplo-rag-openwebui).

## Contenido del repositorio

| Carpeta | Qué contiene | Punto de la actividad |
|---|---|---|
| [`conocimiento/`](conocimiento/) | Documentos de la base de conocimiento y la estrategia de corte | 1 y 2 |
| [`modelo/`](modelo/) | System prompt, políticas e hiperparámetros del modelo personalizado | 3 |
| [`golden-dataset/`](golden-dataset/) | Golden dataset (50 o más casos: prompt y comportamiento esperado) | 4 |
| [`evaluacion/`](evaluacion/) | Script de evaluación, corridas y métricas (latencia, éxito, palabras clave, juez de 1 a 5) | 5 |
| [`api/`](api/) | Prueba del modelo por la API de Open WebUI | 6.F |
| [`evidencias/`](evidencias/) | Capturas de la interfaz y salidas de la API | 6.E y 6.F |
| [`informe/`](informe/) | Secciones del informe y el PDF `Informe-modelo-rag-CloudOps-Client-Hub.pdf` | 6 |

## Cómo levantarlo

Requisitos: Docker Desktop y Python 3.11 o superior.

```bash
cp .env.example .env              # luego pegar la API key de Open WebUI
docker compose up -d              # Ollama en :11434 y Open WebUI en :3000
docker exec -it ollama-rag-cloudops ollama pull qwen2.5:3b-instruct
docker exec -it ollama-rag-cloudops ollama pull qwen2.5:7b-instruct   # modelo juez
pip install -r requirements.txt
```

1. Abrir http://localhost:3000 y crear el usuario administrador.
2. *Workspace → Knowledge*: crear la base con los archivos de `conocimiento/documentos/`, en visibilidad **Public**.
3. *Admin → Settings → Documents*: fijar el tamaño de corte y el solapamiento de [`conocimiento/estrategia-de-corte.md`](conocimiento/estrategia-de-corte.md).
4. *Workspace → Models*: crear el modelo personalizado con [`modelo/system-prompt.md`](modelo/system-prompt.md) y los parámetros de [`modelo/configuracion.md`](modelo/configuracion.md), en visibilidad **Public**.
5. *Settings → Account → API Keys*: crear la key y pegarla en `.env`.

```bash
python api/test_openwebui_api.py      # prueba por API
python evaluacion/evaluate_rag.py     # corre el golden dataset
```

## Resultados

_Pendiente: se completa con la corrida final de `evaluacion/` (casos, % de éxito, % de error, latencia y puntaje del juez)._

## Cómo trabajamos

Guía paso a paso de cada integrante (con prompt para IA): [`guias/`](guias/README.md).

Ver [CONTRIBUTING.md](CONTRIBUTING.md): una rama y un PR por tarea, revisión del coordinador y
commits desde la cuenta de cada quien.

## Aportes de cada integrante

> Cada integrante escribe **su nombre y su propia línea** en un PR desde su cuenta.

| Integrante | Usuario | Aporte |
|---|---|---|
| Integrante 1 · Nicolás Gaviria | @ngcddev | Repositorio, flujo de trabajo, entorno Docker (Ollama + Open WebUI), prueba por API, integración del informe |
| Integrante 2 · Eric Mesias | @Mesiahs | Servicio propuesto, base de conocimiento y estrategia de corte |
| Integrante 3 | @sebastianpaja-debug | Modelo personalizado, system prompt, políticas e hiperparámetros |
| Integrante 4 | @yiselandrea13 | Golden dataset |
| Integrante 5 | @Andres-Duqu | Evaluación de las pruebas, métricas y análisis de resultados |
