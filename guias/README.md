# Guías paso a paso

<!-- Índice de las guías por integrante y pasos comunes de preparación. -->

Cada integrante tiene su guía, con los pasos, el criterio de terminado y un **prompt listo para
pegar en tu IA** (ChatGPT, Claude, Copilot, etc.) para avanzar rápido.

| Integrante | Guía | Issues |
|---|---|---|
| 1 · @ngcddev | [integrante-1-ngcddev.md](integrante-1-ngcddev.md) | #8, #11 |
| 2 · @Mesiahs | [integrante-2-mesiahs.md](integrante-2-mesiahs.md) | #2, #3 |
| 3 · @sebastianpaja-debug | [integrante-3-sebastian.md](integrante-3-sebastian.md) | #4 |
| 4 · @yiselandrea13 | [integrante-4-yisel.md](integrante-4-yisel.md) | #5 |
| 5 · @Andres-Duqu | [integrante-5-andres.md](integrante-5-andres.md) | #6, #7 |

## Cronograma de HOY (todo se entrega hoy)

Hora 0 es cuando empezamos. Cada bloque tiene una salida concreta: si alguien se atrasa, avisa en
el grupo de inmediato. **Lo más importante es que cada uno haga commits propios.**

| Hora | @Mesiahs (2) | @sebastianpaja-debug (3) | @yiselandrea13 (4) | @Andres-Duqu (5) | @ngcddev (1) |
|---|---|---|---|---|---|
| **0:00–0:20** | Paso 0 + `docker compose up` y bajar modelos (tarda: déjalo corriendo) | Igual que Mesiahs | Paso 0 (no necesita Docker) | Igual que Mesiahs | Paso 0, coordinar |
| **0:20–2:00** | Servicio propuesto + 6 documentos **con IA** → **PR antes de la hora 2** | System prompt con IA → PR | 30 casos con IA desde las fuentes de CloudOps → PR | Adaptar `evaluate_rag.py` con IA → PR | Revisar y fusionar PR al momento |
| **2:00–3:00** | Corte 500/50 en Open WebUI, capturas 01–02, `estrategia-de-corte.md` | Cargar la base y crear el modelo, capturas 03–07, `configuracion.md` | Completar 50+ casos revisando contra los documentos de Mesiahs | Cargar base + prompt en su Open WebUI, probar el script con 5 casos | Mismo montaje, `api/test_openwebui_api.py` y capturas |
| **3:00–4:00** | Escribir secciones D y E.1 | Escribir E.2 y F.1 (interfaz) | Escribir F.2 | **Corrida de los 50** (20–40 min) | Portada, introducción, F.1 (API) |
| **4:00–5:00** | Si hay que ajustar documentos o corte, hacerlo ya | Si hay que ajustar el prompt (v2), hacerlo ya | Ajustar palabras clave si Andrés lo pide | Corrida v2 si quedó < 70 %, `resultados.md`, F.3 | Revisar *Insights → Contributors* |
| **5:00–6:00** | Línea de aportes + párrafo de G | Igual | Igual | Igual | Unir informe → PDF → correo al profe |

**Atajos para que alcance el tiempo:**

- Mesiahs: sube los documentos aunque no estén perfectos; se mejoran después en otro PR.
- Sebastián, Andrés y Nicolás: **no esperen** el PR de Mesiahs para montar Open WebUI; carguen
  los documentos apenas estén en su rama.
- Andrés: la corrida final se hace **en un solo PC** (el más potente). Si el juez de 7B va muy
  lento, usa `JUDGE_MODEL=qwen2.5:3b-instruct` y anótalo en `resultados.md`.
- Nadie espera aprobación: Nicolás fusiona los PR apenas lleguen.

## Paso 0, para todos (una sola vez)

1. Aceptar la invitación: https://github.com/ngcddev/rag-cloudops-client-hub/invitations
2. Configurar git con **el mismo correo de tu cuenta de GitHub** (*GitHub → Settings → Emails*).
   Si no coincide, tus commits no cuentan para la nota:

   ```powershell
   git config --global user.name "Tu Nombre"
   git config --global user.email "correo-de-tu-cuenta@ejemplo.com"
   ```

3. Clonar y entrar:

   ```powershell
   git clone https://github.com/ngcddev/rag-cloudops-client-hub.git
   cd rag-cloudops-client-hub
   ```

4. Marcar tu casilla en el issue #1 y asignarte tus issues (*Assignees → assign yourself*).

## Levantar el entorno (quien necesite Open WebUI: integrantes 1, 2, 3 y 5)

Requisitos: Docker Desktop abierto y unos 10 GB libres. **Empieza la descarga de los modelos de primeras**: tarda.

```powershell
Copy-Item .env.example .env
docker compose up -d
docker exec -it ollama-rag-cloudops ollama pull qwen2.5:3b-instruct
docker exec -it ollama-rag-cloudops ollama pull qwen2.5:7b-instruct
```

Abrir http://localhost:3000 y crear tu usuario (el primero que se crea queda como administrador).
Cada quien tiene su propio Open WebUI en su PC: lo que se comparte es lo que está en el repo
(documentos, prompt, parámetros), y cada quien lo carga igual en su entorno.

Si Open WebUI se queda en "Restarting": `docker rm -f open-webui-rag-cloudops`, luego
`docker compose up -d` y revisar con `docker logs -f open-webui-rag-cloudops`.

## Cómo subir tu trabajo (siempre igual)

```powershell
git checkout main
git pull
git checkout -b feat/<numero-issue>-<slug>        # ej. feat/5-golden-dataset
# ... trabajar ...
git add .
git commit -m "feat(golden): casos de planes y SLA"
git push -u origin feat/5-golden-dataset
```

En GitHub aparece el botón **Compare & pull request**. En la descripción escribe `Closes #<issue>`
y pide revisión a @ngcddev. Haz **varios commits pequeños** mientras avanzas, no uno al final.

**Sin consola:** en GitHub puedes usar *Add file → Create new file* (o el lápiz para editar),
elegir **"Create a new branch… and start a pull request"** y listo. También cuenta como tu commit.

## Regla para usar IA

- La IA te ayuda a redactar, pero **tú revisas** que todo coincida con la base de conocimiento.
- No pegues la API key de Open WebUI ni tu `.env` en ninguna IA.
- Los datos del proyecto (Forja Digital, La Sazón, El Tornillo, Dental Popayán) son ficticios, así
  que se pueden compartir.
