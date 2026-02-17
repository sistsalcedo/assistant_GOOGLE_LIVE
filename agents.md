# Guía para agentes (IA / Cursor)

Este documento orienta a asistentes de código (Cursor, Copilot, etc.) que trabajen en el repositorio **assistant_GOOGLE_LIVE**.

## Resumen del proyecto

- **Qué es:** Aplicación web de atención por voz con un agente IA (Gemini 2.5 Flash Live API). El usuario pulsa "Iniciar atención", habla por el micrófono y mantiene una conversación con memoria e interrupciones. Inspirado en PersonaPlex.
- **Repositorio:** https://github.com/sistsalcedo/assistant_GOOGLE_LIVE (rama `main`).
- **Idioma:** Código, comentarios, nombres de carpetas/funciones/clases y documentación en **español**, salvo APIs externas (p. ej. `google-genai`).

## Stack

| Capa        | Tecnología                          |
|------------|--------------------------------------|
| Backend    | Python 3.11+, FastAPI, Uvicorn      |
| IA / Voz   | Google Gemini Live API (`google-genai`), modelo `gemini-2.5-flash-native-audio-preview-12-2025` |
| BD         | SQLAlchemy, SQLite (sesiones y turnos de conversación) |
| Frontend   | React 18, Vite, TypeScript, Tailwind |
| Comunicación | WebSocket (navegador ↔ backend); backend ↔ Gemini Live |

## Estructura de carpetas

- `backend/` – API y lógica de voz
  - `app/core/configuracion.py` – Lectura de `.env`
  - `app/servicios/servicio_gemini_live.py` – Conexión con Gemini Live
  - `app/servicios/servicio_conversaciones.py` – Guardado de sesiones/turnos
  - `app/api/rutas_sesion.py` – `POST /sesion`
  - `app/api/rutas_voz.py` – WebSocket `/voz`
- `frontend/` – UI React
  - `src/paginas/PaginaAtencion.tsx` – Página principal
  - `src/ganchos/useConexionVoz.ts`, `useAudioUsuario.ts` – Audio y WebSocket
  - `src/componentes/` – BarraActividad, PanelCanal, etc.
- `backend/.env` – No se sube a git; cada PC usa su propio `.env` con `GEMINI_API_KEY`. Plantilla: `backend/.env.example`.

## Cómo ejecutar (para pruebas o desarrollo)

1. **Backend:** desde `backend/`, activar venv, `pip install -r requirements.txt`, luego `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
2. **Frontend:** desde `frontend/`, `npm install` y `npm run dev`. Abrir http://localhost:5173.
3. El proxy de Vite reescribe `/api` → backend en `http://localhost:8000` (ver `frontend/vite.config.ts`).

## Convenciones al editar

- Mantener nombres en español en backend y frontend (carpetas, funciones, clases, comentarios).
- No commitear `backend/.env` ni claves; sí mantener actualizado `backend/.env.example`.
- Documentación de usuario y pasos para otra PC: actualizar `README.md` cuando cambien requisitos o comandos.

## Referencias rápidas

- Plan de implementación y checklist: `Checklist.md`
- Configuración del asistente (límites, prompt): variables en `backend/.env` y `app/core/configuracion.py`.
