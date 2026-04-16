import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, KeyRound, ChevronDown } from "lucide-react";
import usePitchStore, { PROVIDERS } from "../../store/pitchStore";

const FIELD_LABELS = {
  api_key:               "API Key",
  aws_access_key_id:     "AWS Access Key ID",
  aws_secret_access_key: "AWS Secret Access Key",
  region:                "AWS Region",
  model_id:              "Model ID (optional)",
};

const FIELD_PLACEHOLDERS = {
  api_key:               "sk-... or your provider key",
  aws_access_key_id:     "AKIA...",
  aws_secret_access_key: "Your secret access key",
  region:                "us-east-1",
  model_id:              "stability.stable-diffusion-xl-v1",
};

export default function SettingsModal({ onClose }) {
  const { provider, setProvider, credentials, setCredential } = usePitchStore();
  const overlayRef = useRef(null);

  const currentProvider = PROVIDERS.find((p) => p.id === provider) || PROVIDERS[0];

  // Close on Escape
  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      ref={overlayRef}
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 200,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 16,
      }}
    >
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.97 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.97 }}
        transition={{ duration: 0.2 }}
        style={{
          background: "#fff",
          border: "1px solid #e0e0e0",
          borderRadius: 14,
          width: "100%",
          maxWidth: 520,
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "20px 24px",
            borderBottom: "1px solid #e0e0e0",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div
              style={{
                width: 32,
                height: 32,
                background: "#0a0a0a",
                borderRadius: 8,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <KeyRound size={14} color="#fff" />
            </div>
            <div>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#0a0a0a" }}>
                Image API Settings
              </div>
              <div style={{ fontSize: 12, color: "#a0a0a0" }}>
                Credentials stay in your browser — never stored on our server
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              color: "#a0a0a0",
              display: "flex",
              padding: 4,
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: "24px" }}>
          {/* Provider selector */}
          <div style={{ marginBottom: 20 }}>
            <span className="section-label" style={{ display: "block", marginBottom: 8 }}>
              Image Generation Provider
            </span>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {PROVIDERS.map((p) => (
                <button
                  key={p.id}
                  onClick={() => setProvider(p.id)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "12px 16px",
                    border: `1px solid ${provider === p.id ? "#0a0a0a" : "#e0e0e0"}`,
                    borderRadius: 8,
                    background: provider === p.id ? "#0a0a0a" : "#fff",
                    cursor: "pointer",
                    textAlign: "left",
                    transition: "all 0.12s",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: 14,
                        fontWeight: 600,
                        color: provider === p.id ? "#fff" : "#0a0a0a",
                        fontFamily: "inherit",
                      }}
                    >
                      {p.shortName}
                    </div>
                    <div
                      style={{
                        fontSize: 12,
                        color: provider === p.id ? "rgba(255,255,255,0.6)" : "#6b6b6b",
                        marginTop: 2,
                        fontFamily: "inherit",
                      }}
                    >
                      {p.description}
                    </div>
                  </div>
                  {provider === p.id && (
                    <div
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: "50%",
                        background: "#fff",
                        flexShrink: 0,
                        marginLeft: 12,
                      }}
                    />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Credential fields for selected provider */}
          <div style={{ borderTop: "1px solid #e0e0e0", paddingTop: 20 }}>
            <span className="section-label" style={{ display: "block", marginBottom: 12 }}>
              {currentProvider.shortName} Credentials
            </span>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {currentProvider.fields.map((field) => (
                <div key={field}>
                  <label
                    style={{
                      display: "block",
                      fontSize: 13,
                      fontWeight: 600,
                      color: "#3a3a3a",
                      marginBottom: 6,
                    }}
                  >
                    {FIELD_LABELS[field] || field}
                  </label>
                  <input
                    type={
                      field === "api_key" || field === "aws_secret_access_key"
                        ? "password"
                        : "text"
                    }
                    value={credentials[field] || ""}
                    onChange={(e) => setCredential(field, e.target.value)}
                    placeholder={FIELD_PLACEHOLDERS[field] || ""}
                    className="input"
                    style={{ fontSize: 13 }}
                    autoComplete="off"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            padding: "16px 24px",
            borderTop: "1px solid #e0e0e0",
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <button className="btn-primary" onClick={onClose} style={{ padding: "10px 24px", fontSize: 14 }}>
            Done
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
