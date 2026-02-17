# Chat de voz con Gemini 2.5 Flash

Aplicación web de atención por voz tipo PersonaPlex: el usuario pulsa "Iniciar atención" y mantiene una conversación de voz con un agente IA (Gemini Live API), con memoria durante la sesión e interrupciones. El backend guarda las conversaciones en SQLite para análisis y ajustes futuros.

## Requisitos

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Cuenta en Google AI Studio** y API key de Gemini
- Micrófono en el navegador

## Repositorio

- **GitHub:** https://github.com/sistsalcedo/assistant_GOOGLE_LIVE
- Rama por defecto: **main**

## Sincronizar con GitHub

### En la PC donde haces los cambios: subir al repo

Cuando modifiques código y quieras guardar esos cambios en GitHub:

```bash
cd assistant_GOOGLE_LIVE   # o la carpeta del proyecto en esta PC
git add .
git status                 # opcional: revisar qué se va a subir
git commit -m "Descripción breve del cambio"
git push origin main
```

- Si es la primera vez en esta PC, puede que tengas que configurar `git config user.name` y `user.email`, y en GitHub autenticarte (token o SSH).
- No se sube `backend/.env` (está en `.gitignore`); el resto de cambios sí.

### En la otra PC: recibir los últimos cambios

En la PC donde ya tenías el proyecto (clonado o copiado) y quieres traer lo último:

```bash
cd assistant_GOOGLE_LIVE   # o la carpeta del proyecto en esa PC
git pull origin main
```

Si añadiste dependencias nuevas (por ejemplo en `requirements.txt` o `package.json`), en esa PC ejecuta también:

- **Backend:** `cd backend`, activar venv, `pip install -r requirements.txt`
- **Frontend:** `cd frontend`, `npm install`

Luego vuelve a ejecutar backend y frontend como en **Ejecutar la aplicación**.

## Abrir el proyecto en otra PC

### Opción A: Clonar desde GitHub (recomendado)

En la otra PC:

```bash
git clone https://github.com/sistsalcedo/assistant_GOOGLE_LIVE.git
cd assistant_GOOGLE_LIVE
```

Luego sigue la sección **Configuración (primera vez en cada PC)** y **Ejecutar la aplicación**.

### Opción B: Copiar la carpeta del proyecto

Copia toda la carpeta del proyecto (incluida la carpeta `.git`) a la otra PC. Luego en esa PC:

```bash
cd assistant_GOOGLE_LIVE
```

y continúa con **Configuración** y **Ejecutar la aplicación**.

## Configuración (primera vez en cada PC)

1. **Backend – variables de entorno**

   - En `backend/` crea un archivo `.env` (no se sube a git).
   - Copia el contenido de `backend/.env.example` y rellena tu API key:

   ```env
   GEMINI_API_KEY=tu_clave_de_Google_AI_Studio
   GEMINI_MODELO=gemini-2.5-flash-native-audio-preview-12-2025
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8000
   DB_URL=sqlite:///./datos_conversaciones.db
   ASISTENTE_MAX_TOKENS_RESPUESTA=256
   ASISTENTE_TEMPERATURA=0.7
   ASISTENTE_PROMPT_SISTEMA="Eres un asistente amable que responde de forma breve y clara."
   ```

2. **Backend – dependencias Python**

   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Frontend – dependencias Node**

   ```bash
   cd frontend
   npm install
   ```

## Ejecutar la aplicación

1. **Terminal 1 – Backend**

   ```bash
   cd backend
   .venv\Scripts\activate
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Terminal 2 – Frontend**

   ```bash
   cd frontend
   npm run dev
   ```

3. Abre en el navegador: **http://localhost:5173**  
   Pulsa "Iniciar atención" y acepta el permiso del micrófono.  
   El frontend envía las peticiones a `/api` al backend (puerto 8000) mediante el proxy configurado en Vite.

## Estructura

- `backend/` – FastAPI, Gemini Live (`google-genai`), SQLite para conversaciones
- `frontend/` – React + Vite + TypeScript + Tailwind, UI de dos canales (agente / usuario)
- `README.md` – Este archivo (requisitos, clonar, configurar, ejecutar)
- `Checklist.md` – Lista de tareas del plan de implementación
- `agents.md` – Guía para agentes de IA (stack, estructura, convenciones)

## Notas

- El archivo `.env` con la API key **no** se sube a git; cada PC debe tener su propio `backend/.env`.
- En unidades de red o virtuales (p. ej. Z:), si Vite da error EISDIR al hacer watch, el script `npm run dev` ya usa `CHOKIDAR_USEPOLLING=1` para evitarlo.
