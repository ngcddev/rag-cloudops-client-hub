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

Requisitos: Docker Desktop abierto y unos 10 GB libres.

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
