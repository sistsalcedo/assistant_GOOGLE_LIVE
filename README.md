# Chat de voz con Gemini 2.5 Flash

Aplicación web de atención por voz tipo PersonaPlex: el usuario pulsa "Iniciar atención" y mantiene una conversación de voz con un agente IA (Gemini Live API), con memoria durante la sesión e interrupciones. El backend guarda las conversaciones en SQLite para análisis y ajustes futuros.

## Requisitos

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Cuenta en Google AI Studio** y API key de Gemini
- Micrófono en el navegador

## Abrir el proyecto en otra PC

### Opción A: Clonar desde un repositorio remoto

Si subes este repo a GitHub, GitLab o similar:

```bash
git clone <URL_DEL_REPOSITORIO>
cd chat_estilo_personlplex
```

### Opción B: Copiar la carpeta del proyecto

Copia toda la carpeta del proyecto (incluida la carpeta `.git`) a la otra PC. Luego en esa PC:

```bash
cd chat_estilo_personlplex
```

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

## Estructura

- `backend/` – FastAPI, Gemini Live (`google-genai`), SQLite para conversaciones
- `frontend/` – React + Vite + TypeScript + Tailwind, UI de dos canales (agente / usuario)
- `Checklist.md` – Lista de tareas del plan de implementación

## Notas

- El archivo `.env` con la API key **no** se sube a git; cada PC debe tener su propio `backend/.env`.
- En unidades de red o virtuales (p. ej. Z:), si Vite da error EISDIR al hacer watch, el script `npm run dev` ya usa `CHOKIDAR_USEPOLLING=1` para evitarlo.
