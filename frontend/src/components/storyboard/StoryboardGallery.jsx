import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Play, RotateCcw, ImageIcon } from "lucide-react";
import usePitchStore from "../../store/pitchStore";
import FrameCard from "./FrameCard";
import FramePlayer from "./FramePlayer";

export default function StoryboardGallery() {
  const { frames, conceptImages, isGenerating, statusMessage, entities, setPhase } = usePitchStore();
  const [playerOpen, setPlayerOpen] = useState(false);
  const [playerStart, setPlayerStart] = useState(0);

  const openPlayer = (index) => { setPlayerStart(index); setPlayerOpen(true); };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ maxWidth: 1100, margin: "0 auto", padding: "48px 24px" }}
    >
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <h2 style={{ fontSize: 32, fontWeight: 800, letterSpacing: "-0.03em", color: "#0a0a0a", margin: "0 0 8px" }}>
          {isGenerating ? "Generating frames..." : "Your Storyboard"}
        </h2>
        {statusMessage && (
          <motion.div
            key={statusMessage}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 14, color: "#6b6b6b" }}
          >
            {isGenerating && <Loader2 size={14} style={{ animation: "spin 1s linear infinite", flexShrink: 0 }} />}
            {statusMessage}
          </motion.div>
        )}
      </div>

      {/* Concept Art strip */}
      {Object.keys(conceptImages).length > 0 && (
        <section style={{ marginBottom: 36 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
            <ImageIcon size={13} color="#6b6b6b" />
            <span className="section-label">Concept Art</span>
          </div>
          <div style={{ display: "flex", gap: 12, overflowX: "auto", paddingBottom: 4 }}>
            {Object.entries(conceptImages).map(([entityId, url]) => {
              const entity = entities.find((e) => e.id === entityId);
              return (
                <motion.div
                  key={entityId}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  style={{
                    flexShrink: 0,
                    width: 140,
                    border: "1px solid #e0e0e0",
                    borderRadius: 8,
                    overflow: "hidden",
                    background: "#fff",
                  }}
                >
                  <img src={url} alt={entity?.name} style={{ width: 140, height: 140, objectFit: "cover", display: "block" }} />
                  <div style={{ padding: "8px 10px", fontSize: 12, fontWeight: 600, color: "#3a3a3a" }}>
                    {entity?.name || entityId}
                  </div>
                </motion.div>
              );
            })}
          </div>
          <div className="divider" style={{ marginTop: 24 }} />
        </section>
      )}

      {/* Shimmer placeholders */}
      {isGenerating && frames.length === 0 && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
          {[1, 2, 3].map((i) => (
            <div key={i} style={{ border: "1px solid #e0e0e0", borderRadius: 10, overflow: "hidden" }}>
              <div style={{ aspectRatio: "16/9" }} className="shimmer" />
              <div style={{ padding: 14 }}>
                <div style={{ height: 13, width: "60%", borderRadius: 4, marginBottom: 8 }} className="shimmer" />
                <div style={{ height: 11, width: "35%", borderRadius: 4 }} className="shimmer" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Frame grid */}
      {frames.length > 0 && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
          {frames.map((frame, i) => (
            <FrameCard key={frame.scene_id} frame={frame} index={i} onClick={() => openPlayer(i)} />
          ))}
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              style={{
                border: "1px dashed #e0e0e0",
                borderRadius: 10,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                aspectRatio: "16/9",
                gap: 10,
              }}
            >
              <Loader2 size={24} color="#a0a0a0" style={{ animation: "spin 1s linear infinite" }} />
              <span style={{ fontSize: 13, color: "#a0a0a0" }}>Next frame...</span>
            </motion.div>
          )}
        </div>
      )}

      {/* Empty state — generation finished but no frames (API error) */}
      {!isGenerating && frames.length === 0 && (
        <div
          style={{
            border: "1px solid #e0e0e0",
            borderRadius: 12,
            padding: "48px 32px",
            textAlign: "center",
            maxWidth: 480,
            margin: "0 auto",
          }}
        >
          <div style={{ fontSize: 32, marginBottom: 16 }}>⚠️</div>
          <div style={{ fontSize: 16, fontWeight: 700, color: "#0a0a0a", marginBottom: 8 }}>
            No frames were generated
          </div>
          <div style={{ fontSize: 14, color: "#6b6b6b", lineHeight: 1.6, marginBottom: 24 }}>
            {statusMessage?.includes("Error") || statusMessage?.includes("credits")
              ? statusMessage
              : "Image generation failed — this is usually a BFL API credit or key issue. Check your .env and dashboard.bfl.ai balance."}
          </div>
          <button className="btn-secondary" onClick={() => setPhase("review")}>
            <RotateCcw size={14} />
            Back to Outline
          </button>
        </div>
      )}

      {/* Actions */}
      {!isGenerating && frames.length > 0 && (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 12, marginTop: 40 }}>
          <button className="btn-secondary" onClick={() => setPhase("review")}>
            <RotateCcw size={14} />
            Re-edit Outline
          </button>
          <button className="btn-primary" onClick={() => openPlayer(0)} style={{ padding: "14px 36px", fontSize: 15 }}>
            <Play size={16} />
            Play Storyboard
          </button>
        </div>
      )}

      <AnimatePresence>
        {playerOpen && (
          <FramePlayer frames={frames} startIndex={playerStart} onClose={() => setPlayerOpen(false)} />
        )}
      </AnimatePresence>

      <style>{`@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }`}</style>
    </motion.div>
  );
}
