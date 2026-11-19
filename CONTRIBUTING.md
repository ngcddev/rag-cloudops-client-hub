# Cómo trabajamos en este repositorio

<!-- Reglas de colaboración del equipo: ramas, commits, PR y revisión. -->

El docente revisa quién aporta en el historial de commits. Quien no aparezca queda fuera de la
nota, así que **cada integrante hace sus commits desde su propia cuenta y su propio PC**.

## Antes del primer commit (una sola vez)

1. Aceptar la invitación al repositorio (llega al correo de GitHub).
2. Revisar que el correo de git esté verificado en tu cuenta (*GitHub → Settings → Emails*).
   Si no coincide, tus commits **no cuentan como tuyos**:

   ```bash
   git config --global user.name  "Tu Nombre"
   git config --global user.email "el-correo-de-tu-cuenta@ejemplo.com"
   ```

3. Clonar:

   ```bash
   git clone https://github.com/ngcddev/rag-cloudops-client-hub.git
   cd rag-cloudops-client-hub
   ```

## Flujo por cada tarea

1. Asignarte el issue en *Issues* y moverlo a "En curso".
2. Actualizar `main` y crear tu rama:

   ```bash
   git checkout main && git pull
   git checkout -b feat/<numero-issue>-<slug>      # ej. feat/3-golden-dataset
   ```

3. Commits pequeños y frecuentes, en español con Conventional Commits:
   `feat(golden): 20 casos fuera de alcance`, `docs(informe): sección E`, `fix(eval): ...`.
4. Subir y abrir el PR:

   ```bash
   git push -u origin feat/3-golden-dataset
   ```

   En la descripción del PR escribir `Closes #3`.
5. Pedir revisión a **otro integrante**. `main` está protegida: sin una aprobación no se fusiona.
6. Al aprobar, fusionar con **"Create a merge commit"** y borrar la rama.

## Reglas

- Nada de secretos: la API key va en `.env` (ignorado por git), nunca en el código.
- Cada quien trabaja en su carpeta; si tienes que tocar la de otro, avísale.
- Los textos van en español; los nombres de código, en inglés.
- No subir modelos, volúmenes de Docker ni el entorno virtual.
- Tu línea en la tabla "Aportes de cada integrante" del README la escribes tú, en un PR.
