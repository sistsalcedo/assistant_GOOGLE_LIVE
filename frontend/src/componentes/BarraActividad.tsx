import React from "react";

interface PropiedadesBarraActividad {
  nivel: number;
}

/**
 * Renderiza un pequeño grupo de barras verticales cuyo tamaño depende del nivel.
 */
export const BarraActividad: React.FC<PropiedadesBarraActividad> = ({ nivel }) => {
  const barras = [0, 1, 2, 3, 4];
  const alturaBase = Math.max(0.2, Math.min(1, nivel));

  return (
    <div className="flex items-end gap-1 h-8">
      {barras.map((indice) => {
        const factor = 0.5 + indice * 0.1;
        const altura = `${alturaBase * factor * 100}%`;
        return (
          <div
            key={indice}
            className="w-1 rounded bg-emerald-400 transition-all duration-75"
            style={{ height: altura }}
          />
        );
      })}
    </div>
  );
};

