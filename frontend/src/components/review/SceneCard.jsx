import { motion } from "framer-motion";
import { Trash2 } from "lucide-react";
import usePitchStore from "../../store/pitchStore";
import { EMOTION_EMOJIS } from "../../utils/constants";

export default function SceneCard({ scene, index }) {
  const { updateScene, deleteScene, scenes } = usePitchStore();
  const canDelete = scenes.length > 1;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ delay: index * 0.06 }}
      className="card"
      style={{ padding: "20px" }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 14 }}>
        {/* Frame number */}
        <div
          style={{
            width: 28,
            height: 28,
            background: "#0a0a0a",
            borderRadius: 6,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            marginTop: 2,
          }}
        >
          <span style={{ fontSize: 11, fontWeight: 700, color: "#fff" }}>{index + 1}</span>
        </div>

        <div style={{ flex: 1 }}>
          <textarea
            value={scene.action}
            onChange={(e) => updateScene(scene.id, { action: e.target.value })}
            rows={2}
            placeholder="Brief sentence describing the visual action of the scene..."
            className="input"
            style={{
              width: "100%",
              fontSize: 14,
              color: "#0a0a0a",
              lineHeight: 1.5,
              resize: "none",
            }}
          />
        </div>

        {canDelete && (
          <button
            onClick={() => deleteScene(scene.id)}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "4px",
              color: "#b0b0b0",
              display: "flex",
              transition: "color 0.15s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#0a0a0a")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "#b0b0b0")}
          >
            <Trash2 size={15} />
          </button>
        )}
      </div>

      {/* Shot + Lighting */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div>
          <span className="section-label" style={{ display: "block", marginBottom: 6 }}>Shot Type</span>
          <input
            value={scene.cinematic_shot}
            onChange={(e) => updateScene(scene.id, { cinematic_shot: e.target.value })}
            className="input"
            style={{ fontSize: 13 }}
          />
        </div>
        <div>
          <span className="section-label" style={{ display: "block", marginBottom: 6 }}>Lighting</span>
          <input
            value={scene.lighting_mood}
            onChange={(e) => updateScene(scene.id, { lighting_mood: e.target.value })}
            className="input"
            style={{ fontSize: 13 }}
          />
        </div>
      </div>
    </motion.div>
  );
}
