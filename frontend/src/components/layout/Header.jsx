import { useState } from "react";
import { Sparkles, RotateCcw, Settings } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import usePitchStore, { PROVIDERS } from "../../store/pitchStore";
import SettingsModal from "./SettingsModal";

export default function Header() {
  const { phase, resetAll, provider, credentials } = usePitchStore();
  const [settingsOpen, setSettingsOpen] = useState(false);

  const currentProvider = PROVIDERS.find((p) => p.id === provider);
  
  // Check if credentials are configured
  const hasCredentials = currentProvider?.fields.some((f) => !!credentials[f]);

  return (
    <>
      <header style={{ borderBottom: "1px solid #e0e0e0", background: "#fff", position: "sticky", top: 0, zIndex: 50 }}>
        <div
          style={{
            maxWidth: 1100,
            margin: "0 auto",
            padding: "14px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          {/* Logo */}
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                width: 34,
                height: 34,
                background: "#0a0a0a",
                borderRadius: 8,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Sparkles size={15} color="#fff" />
            </div>
            <div>
              <div style={{ fontWeight: 800, fontSize: 15, letterSpacing: "-0.02em", color: "#0a0a0a" }}>
                Pitch Visualizer
              </div>
              <div style={{ fontSize: 11, color: "#a0a0a0", letterSpacing: "0.04em", textTransform: "uppercase" }}>
                AI Storyboard Engine
              </div>
            </div>
          </div>

          {/* Right controls */}
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>

            {/* Provider indicator + settings button */}
            <button
              onClick={() => setSettingsOpen(true)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                padding: "8px 14px",
                border: `1px solid ${hasCredentials ? "#0a0a0a" : "#e0e0e0"}`,
                borderRadius: 8,
                background: hasCredentials ? "#0a0a0a" : "#fff",
                cursor: "pointer",
                fontFamily: "inherit",
                transition: "all 0.15s",
              }}
            >
              <Settings size={13} color={hasCredentials ? "#fff" : "#6b6b6b"} />
              <span
                style={{
                  fontSize: 13,
                  fontWeight: 600,
                  color: hasCredentials ? "#fff" : "#6b6b6b",
                }}
              >
                {hasCredentials ? currentProvider?.shortName : "Set API Key"}
              </span>
              {!hasCredentials && (
                <span
                  style={{
                    width: 6,
                    height: 6,
                    borderRadius: "50%",
                    background: "#e53e3e",
                    flexShrink: 0,
                  }}
                />
              )}
            </button>

            {phase !== "input" && (
              <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                onClick={resetAll}
                className="btn-secondary"
                style={{ fontSize: 13, padding: "8px 14px" }}
              >
                <RotateCcw size={13} />
                Start Over
              </motion.button>
            )}
          </div>
        </div>
      </header>

      {/* Settings modal */}
      <AnimatePresence>
        {settingsOpen && <SettingsModal onClose={() => setSettingsOpen(false)} />}
      </AnimatePresence>
    </>
  );
}
