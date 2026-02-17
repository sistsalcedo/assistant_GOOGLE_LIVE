export interface RespuestaIniciarSesion {
  id_sesion: string;
  url_websocket: string;
}

export async function iniciarSesion(usuarioId?: string): Promise<RespuestaIniciarSesion> {
  const respuesta = await fetch("/api/sesion", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ usuario_id: usuarioId ?? null })
  });

  if (!respuesta.ok) {
    throw new Error("No se pudo iniciar la sesión de atención.");
  }

  return (await respuesta.json()) as RespuestaIniciarSesion;
}

