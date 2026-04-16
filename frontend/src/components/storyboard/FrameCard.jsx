import { motion } from "framer-motion";
import { EMOTION_EMOJIS } from "../../utils/constants";

export default function FrameCard({ frame, index, onClick }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.1 }}
      onClick={onClick}
      style={{
        background: "#fff",
        border: "1px solid #e0e0e0",
        borderRadius: 10,
        overflow: "hidden",
        cursor: "pointer",
        transition: "border-color 0.15s, transform 0.15s",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = "#0a0a0a";
        e.currentTarget.style.transform = "translateY(-3px)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = "#e0e0e0";
        e.currentTarget.style.transform = "translateY(0)";
      }}
    >
      {/* Image */}
      <div style={{ position: "relative", aspectRatio: "16/9", overflow: "hidden", background: "#f5f5f5" }}>
        <img
          src={frame.image_url}
          alt={frame.scene_title}
          style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
          loading="lazy"
        />
        {/* Frame number */}
        <div
          style={{
            position: "absolute",
            top: 10,
            left: 10,
            background: "#0a0a0a",
            color: "#fff",
            fontSize: 11,
            fontWeight: 700,
            padding: "3px 8px",
            borderRadius: 4,
          }}
        >
          {index + 1}
        </div>
        {/* Shot type */}
        <div
          style={{
            position: "absolute",
            top: 10,
            right: 10,
            background: "rgba(255,255,255,0.92)",
            color: "#0a0a0a",
            fontSize: 11,
            fontWeight: 600,
            padding: "3px 8px",
            borderRadius: 4,
          }}
        >
          {frame.cinematic_shot}
        </div>
      </div>

      {/* Footer */}
      <div style={{ padding: "12px 14px", borderTop: "1px solid #f0f0f0" }}>
        <div style={{ fontSize: 13, color: "#0a0a0a", lineHeight: 1.5 }}>
          {frame.scene_action}
        </div>
      </div>
    </motion.div>
  );
}
