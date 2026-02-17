import React from "react";
import { BarraActividad } from "./BarraActividad";

interface PropiedadesPanelCanal {
  titulo: string;
  descripcion?: string;
  nivelAudio: number;
  estaHablando: boolean;
}

export const PanelCanal: React.FC<PropiedadesPanelCanal> = ({
  titulo,
  descripcion,
  nivelAudio,
  estaHablando
}) => {
  return (
    <div className="flex items-center justify-between rounded-xl bg-slate-900/70 px-6 py-4 border border-slate-700">
      <div className="flex flex-col">
        <span className="text-sm text-slate-400 font-semibold uppercase tracking-wide">
          {titulo}
        </span>
        {descripcion && <span className="text-xs text-slate-500 mt-1">{descripcion}</span>}
        {estaHablando && (
          <span className="mt-2 text-xs text-emerald-400">Hablando...</span>
        )}
      </div>
      <BarraActividad nivel={nivelAudio} />
    </div>
  );
};

