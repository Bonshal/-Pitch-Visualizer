import { motion } from "framer-motion";
import { Pen, ScanEye, Clapperboard, Check } from "lucide-react";
import usePitchStore from "../../store/pitchStore";

const STEPS = [
  { id: "input", label: "Write Pitch", Icon: Pen },
  { id: "review", label: "Review Outline", Icon: ScanEye },
  { id: "generate", label: "Generate", Icon: Clapperboard },
];

const phaseOrder = ["input", "review", "generate"];

export default function ProgressStepper() {
  const { phase } = usePitchStore();
  const currentIdx = phaseOrder.indexOf(phase);

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 0,
        padding: "24px",
        borderBottom: "1px solid #e0e0e0",
        background: "#fff",
      }}
    >
      {STEPS.map((step, i) => {
        const isActive = i === currentIdx;
        const isComplete = i < currentIdx;
        const Icon = step.Icon;

        return (
          <div key={step.id} style={{ display: "flex", alignItems: "center" }}>
            {/* Step */}
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <motion.div
                animate={{
                  background: isComplete ? "#0a0a0a" : isActive ? "#0a0a0a" : "#f0f0f0",
                  borderColor: isActive ? "#0a0a0a" : "transparent",
                }}
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: "50%",
                  border: "2px solid",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                {isComplete ? (
                  <Check size={14} color="#fff" />
                ) : (
                  <Icon size={14} color={isActive ? "#fff" : "#a0a0a0"} />
                )}
              </motion.div>
              <span
                style={{
                  fontSize: 13,
                  fontWeight: isActive ? 600 : 400,
                  color: isActive || isComplete ? "#0a0a0a" : "#a0a0a0",
                  whiteSpace: "nowrap",
                }}
              >
                {step.label}
              </span>
            </div>

            {/* Connector */}
            {i < STEPS.length - 1 && (
              <div
                style={{
                  width: 60,
                  height: 1,
                  background: isComplete ? "#0a0a0a" : "#e0e0e0",
                  margin: "0 16px",
                  flexShrink: 0,
                  transition: "background 0.3s",
                }}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
