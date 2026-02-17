# Checklist implementación chat de voz con Gemini 2.5 Flash

## 1. Base del proyecto

- [x] Crear estructura `frontend/` y `backend/` según el plan.
- [x] Inicializar `.gitignore` adecuado (para `node_modules`, `.venv`, `.env`, etc.).
- [x] Inicializar repositorio git y rama `main`.
- [x] Subir el proyecto a GitHub (repo: `sistsalcedo/assistant_GOOGLE_LIVE`).

---

## 2. Backend

### 2.1 Dependencias y configuración

- [x] Crear `backend/requirements.txt` con:
  - [x] `fastapi`, `uvicorn[standard]`
  - [x] `google-genai`
  - [x] `python-dotenv`, `pydantic`, `pydantic-settings`
  - [x] `sqlalchemy`, `alembic`
  - [x] `ruff`, `mypy`, `pytest`
- [x] Crear `backend/.env.example` con:
  - [x] `GEMINI_API_KEY`
  - [x] `GEMINI_MODELO` (actualizar al valor sin `models/`)
  - [x] `BACKEND_HOST`, `BACKEND_PORT`, `DB_URL`
  - [x] parámetros del asistente (`ASISTENTE_MAX_TOKENS_RESPUESTA`, `ASISTENTE_TEMPERATURA`, `ASISTENTE_PROMPT_SISTEMA`)
- [x] Crear y rellenar `backend/.env` real con tu `GEMINI_API_KEY` y el modelo correcto.

### 2.2 Núcleo de la app

- [x] Implementar `app/core/configuracion.py`:
  - [x] Clase `ConfiguracionAplicacion` que lee `.env`.
  - [x] Función `obtener_configuracion()` cacheada.
- [x] Implementar `app/main.py`:
  - [x] Instancia de `FastAPI`.
  - [x] Configuración CORS.
  - [x] Inclusión de routers (`rutas_sesion`, `rutas_voz`).

### 2.3 Servicio Gemini Live

- [x] Implementar `app/servicios/servicio_gemini_live.py` con:
  - [x] `ServicioGeminiLive` que crea el cliente `genai.Client` con `GEMINI_API_KEY`.
  - [x] `SesionGeminiLive` que:
    - [x] Usa `client.aio.live.connect(model=GEMINI_MODELO, config=...)`.
    - [x] Expone `enviar_audio_usuario(...)` (esqueleto con `audio/pcm`).
    - [x] Expone `iterar_respuestas_agente()` (esqueleto que itera respuestas).
    - [x] Cierra la sesión con `cerrar()`.

> Nota: la parte de **mapear exactamente la estructura de mensajes de Gemini (audio binario real)** sigue siendo esqueleto; falta completar cuando integremos el formato exacto.

### 2.4 Almacenamiento de conversaciones

- [x] Implementar modelos SQLAlchemy en `app/modelos/conversacion.py`:
  - [x] Tabla `sesiones` con `id_sesion`, `fecha_inicio`, `fecha_fin`, `duracion_segundos`, `configuracion_usada`.
  - [x] Tabla `turnos` con `id`, `id_sesion`, `tipo_emisor`, `marca_tiempo`, `texto_transcrito`, `longitud_respuesta_tokens`.
- [x] Implementar `app/servicios/servicio_conversaciones.py`:
  - [x] `ServicioConversaciones` con conexión a SQLite (`DB_URL`).
  - [x] `crear_sesion(id_sesion, configuracion_usada)`.
  - [x] `marcar_sesion_finalizada(id_sesion)`.
  - [x] `guardar_turno(id_sesion, tipo_emisor, texto_transcrito, longitud_tokens)`.
  - [x] `obtener_conversacion(id_sesion)` y `iterar_turnos(id_sesion)`.

### 2.5 Rutas API y WebSocket

- [x] Implementar `app/modelos/mensajes_voz.py` (Pydantic) para:
  - [x] `PeticionIniciarSesion`, `RespuestaIniciarSesion`.
  - [x] `MensajeWebSocketCliente`, `MensajeWebSocketServidor`.
- [x] Implementar `app/api/rutas_sesion.py`:
  - [x] `POST /sesion` que:
    - [x] Genera `id_sesion` (UUID).
    - [x] Crea `SesionGeminiLive` y la guarda en `sesiones_activas`.
    - [x] Registra la sesión en BD mediante `ServicioConversaciones`.
    - [x] Devuelve `{ id_sesion, url_websocket: "/voz" }`.
- [x] Implementar `app/api/rutas_voz.py` (esqueleto funcional) que:
  - [x] Acepta WebSocket `/voz?id_sesion=...`.
  - [x] Busca la `SesionGeminiLive` correspondiente.
  - [x] Gestiona un timeout de inactividad.
  - [x] Envía eventos JSON al cliente (`inicio_respuesta_agente`, `fin_respuesta_agente`, `sesion_finalizada`, `error`).
  - [ ] Envía y reproduce **audio real del agente** (actualmente usa `send_bytes(b"")` como placeholder).
  - [ ] Usa audio real del usuario (por ahora asume que todo mensaje binario es audio, pero falta conectar con el flujo del frontend).

---

## 3. Frontend

### 3.1 Configuración base

- [x] Configurar proyecto Vite + React + TypeScript + Tailwind en `frontend/`:
  - [x] `package.json`, `tsconfig.json`, `vite.config.ts`, `tailwind.config.cjs`, `postcss.config.cjs`.
  - [x] `index.html` y `src/main.tsx` con `PaginaAtencion`.
  - [x] `src/estilos.css` con Tailwind importado.
- [x] Proxy en `vite.config.ts`: reescritura `/api` → backend (`rewrite` para que `POST /api/sesion` llegue como `/sesion`).
- [x] Script `npm run dev` con `CHOKIDAR_USEPOLLING=1` (evitar error EISDIR en unidades de red/virtuales).

### 3.2 Servicios y hooks

- [x] Implementar `src/servicios/clienteApi.ts`:
  - [x] `iniciarSesion()` que llama a `POST /api/sesion`.
- [x] Implementar `src/ganchos/useAudioUsuario.ts`:
  - [x] Captura micrófono con `getUserMedia`.
  - [x] Calcula `nivelAudio` usando `AnalyserNode`.
- [x] Implementar `src/ganchos/useConexionVoz.ts`:
  - [x] Gestiona estados de sesión (`sinSesion`, `conectando`, `enConversacion`, `finalizada`).
  - [x] Abre WebSocket `/api/voz?id_sesion=...`.
  - [x] Procesa mensajes JSON de eventos (`inicio_respuesta_agente`, `fin_respuesta_agente`, `sesion_finalizada`).
  - [ ] Envía **audio real del usuario** en chunks binarios al backend (actualmente sólo gestiona estados, no serializa el audio del `MediaStream`).
  - [ ] Procesa y reproduce **audio real del agente** a partir de los `ArrayBuffer` recibidos.

### 3.3 Componentes y flujo de UI

- [x] Implementar `src/componentes/BarraActividad.tsx` (barras de nivel de audio).
- [x] Implementar `src/componentes/PanelCanal.tsx` (panel por canal: Agente / Usuario).
- [x] Implementar `src/paginas/PaginaAtencion.tsx`:
  - [x] Muestra ambos canales con sus barras.
  - [x] Botón “Iniciar atención” que:
    - [x] Llama a `iniciarSesion()`.
    - [x] Configura `idSesion` y `urlWebSocket` para `useConexionVoz`.
  - [x] Botón “Finalizar sesión” que resetea el estado local (falta integrar comando explícito al backend).

---

## 4. Pruebas y ajustes

- [ ] Probar sesiones completas de ~5 minutos con el audio ya integrado (cuando se complete el pipeline), verificando:
  - [ ] Que Gemini mantiene contexto dentro de la misma sesión.
  - [ ] Que el usuario puede interrumpir y Gemini retoma correctamente.
- [x] Validar que el backend compila sin errores (`python -m compileall backend`).
- [x] Ejecutar linters básicos sin errores en backend y frontend.
- [ ] Confirmar manualmente que:
  - [ ] El botón “Finalizar” envía cierre de sesión al backend (comando WebSocket + limpieza en BD).
  - [ ] El timeout se dispara si no hay actividad.
  - [ ] Las sesiones y turnos se guardan correctamente en `datos_conversaciones.db`.
  - [ ] Ajustar en `.env`:
  - [ ] `ASISTENTE_MAX_TOKENS_RESPUESTA`.
  - [ ] `ASISTENTE_TEMPERATURA`.
  - [ ] `ASISTENTE_PROMPT_SISTEMA`.
  y observar cambios en el comportamiento del asistente.

---

## 5. Repositorio y documentación

- [x] `.gitignore` (`.env`, `node_modules`, `.venv`, `__pycache__`, etc.).
- [x] Repositorio Git inicializado; commits con código y documentación.
- [x] Remoto `origin` apuntando a `https://github.com/sistsalcedo/assistant_GOOGLE_LIVE.git`; push a rama `main`.
- [x] `README.md` con: requisitos, clonar en otra PC, configuración de `.env`, dependencias, comandos para ejecutar backend y frontend.
- [x] `agents.md` con guía para agentes de IA (stack, estructura, convenciones en español).
