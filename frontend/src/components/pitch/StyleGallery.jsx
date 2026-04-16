import { motion } from "framer-motion";
import usePitchStore from "../../store/pitchStore";
import { STYLES } from "../../utils/constants";

export default function StyleGallery() {
  const { selectedStyle, setSelectedStyle } = usePitchStore();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <span className="section-label">Choose Your Visual Style</span>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
          gap: 12,
        }}
      >
        {STYLES.map((style, i) => {
          const isSelected = selectedStyle === style.id;
          return (
            <motion.button
              key={style.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelectedStyle(style.id)}
              style={{
                background: isSelected ? "#0a0a0a" : "#fff",
                border: `1px solid ${isSelected ? "#0a0a0a" : "#e0e0e0"}`,
                borderRadius: 10,
                padding: "16px",
                cursor: "pointer",
                textAlign: "left",
                display: "flex",
                flexDirection: "column",
                gap: 8,
                transition: "all 0.15s",
              }}
            >
              {/* Emoji */}
              <span style={{ fontSize: 24 }}>{style.emoji}</span>

              {/* Name */}
              <span
                style={{
                  fontSize: 13,
                  fontWeight: 700,
                  color: isSelected ? "#fff" : "#0a0a0a",
                  letterSpacing: "-0.01em",
                }}
              >
                {style.name}
              </span>

              {/* Description */}
              <span
                style={{
                  fontSize: 12,
                  lineHeight: 1.5,
                  color: isSelected ? "rgba(255,255,255,0.65)" : "#6b6b6b",
                }}
              >
                {style.description}
              </span>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
