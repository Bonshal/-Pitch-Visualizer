import { motion } from "framer-motion";
import { User, MapPin, Package } from "lucide-react";
import usePitchStore from "../../store/pitchStore";

const TYPE_ICONS = { character: User, environment: MapPin, object: Package };

export default function EntityCard({ entity, index }) {
  const { updateEntity } = usePitchStore();
  const Icon = TYPE_ICONS[entity.type] || Package;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08 }}
      className="card"
      style={{ padding: "20px" }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <div
          style={{
            width: 30,
            height: 30,
            background: "#f0f0f0",
            borderRadius: 6,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
        >
          <Icon size={14} color="#3a3a3a" />
        </div>
        <input
          value={entity.name}
          onChange={(e) => updateEntity(entity.id, { name: e.target.value })}
          style={{
            flex: 1,
            background: "transparent",
            border: "none",
            fontSize: 14,
            fontWeight: 700,
            color: "#0a0a0a",
            outline: "none",
            fontFamily: "inherit",
          }}
        />
        <span className="pill">{entity.type}</span>
      </div>

      {/* Description */}
      <textarea
        value={entity.description}
        onChange={(e) => updateEntity(entity.id, { description: e.target.value })}
        rows={3}
        className="input"
        style={{ fontSize: 13, color: "#3a3a3a", marginBottom: 10 }}
      />

      {/* Role */}
      <div style={{ fontSize: 12, color: "#a0a0a0" }}>
        <span style={{ fontWeight: 600, color: "#6b6b6b" }}>Role: </span>
        <input
          value={entity.emotional_role}
          onChange={(e) => updateEntity(entity.id, { emotional_role: e.target.value })}
          style={{
            background: "transparent",
            border: "none",
            fontSize: 12,
            color: "#6b6b6b",
            outline: "none",
            fontFamily: "inherit",
            width: "85%",
          }}
        />
      </div>
    </motion.div>
  );
}
