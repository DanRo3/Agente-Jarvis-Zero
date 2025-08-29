import { BrainCircuit, Hammer, Eye } from "lucide-react";
import type { MonitoringStep as MonitoringStepType } from "../../types/types";

interface MonitoringStepProps {
  step: MonitoringStepType;
}

const ICONS = {
  thought: <BrainCircuit size={20} className="text-purple-400" />,
  tool_start: <Hammer size={20} className="text-amber-400" />,
  tool_end: <Eye size={20} className="text-cyan-400" />,
};

export function MonitoringStep({ step }: MonitoringStepProps) {
  // Ignoramos el renderizado de 'final_answer' aquí, ya que va al chat principal
  if (step.type === "final_answer") return null;

  const icon = ICONS[step.type as keyof typeof ICONS];

  return (
    <div className="flex items-start space-x-3 p-3 bg-gray-800/50 rounded-lg text-sm">
      <div className="flex-shrink-0 mt-0.5">{icon}</div>
      <p className="text-gray-300 whitespace-pre-wrap font-mono break-words">
        {step.content}
      </p>
    </div>
  );
}
