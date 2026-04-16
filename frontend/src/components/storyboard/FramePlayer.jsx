import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, X, Play, Pause } from "lucide-react";
import { EMOTION_EMOJIS } from "../../utils/constants";

export default function FramePlayer({ frames, startIndex = 0, onClose }) {
  const [current, setCurrent] = useState(startIndex);
  const [isPlaying, setIsPlaying] = useState(false);
  const frame = frames[current];

  const goNext = useCallback(() => setCurrent((c) => (c + 1) % frames.length), [frames.length]);
  const goPrev = useCallback(() => setCurrent((c) => (c - 1 + frames.length) % frames.length), [frames.length]);

  useEffect(() => {
    if (!isPlaying) return;
    const timer = setInterval(goNext, 4000);
    return () => clearInterval(timer);
  }, [isPlaying, goNext]);

  useEffect(() => {
    const handler = (e) => {
      if (e.key === "ArrowRight") goNext();
      else if (e.key === "ArrowLeft") goPrev();
      else if (e.key === "Escape") onClose();
      else if (e.key === " ") { e.preventDefault(); setIsPlaying((p) => !p); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [goNext, goPrev, onClose]);

  if (!frame) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 100,
        background: "rgba(0,0,0,0.95)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 24,
      }}
      onClick={onClose}
    >
      <div
        style={{ maxWidth: 1000, width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close */}
        <button
          onClick={onClose}
          style={{
            position: "absolute",
            top: 20,
            right: 20,
            background: "rgba(255,255,255,0.12)",
            border: "none",
            borderRadius: "50%",
            width: 36,
            height: 36,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            color: "#fff",
          }}
        >
          <X size={16} />
        </button>

        {/* Image */}
        <AnimatePresence mode="wait">
          <motion.img
            key={frame.scene_id}
            src={frame.image_url}
            alt={frame.scene_title}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            style={{
              maxHeight: "65vh",
              width: "100%",
              objectFit: "contain",
              borderRadius: 8,
            }}
          />
        </AnimatePresence>

        {/* Caption */}
        <motion.div
          key={`cap-${current}`}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ marginTop: 24, textAlign: "center", maxWidth: "80%" }}
        >
          <div style={{ fontSize: 16, color: "#fff", lineHeight: 1.5 }}>
            {frame.scene_action}
          </div>
          <div style={{ marginTop: 8, fontSize: 13, color: "rgba(255,255,255,0.5)" }}>
            {frame.cinematic_shot}
            &nbsp;·&nbsp;{current + 1} / {frames.length}
          </div>
        </motion.div>

        {/* Controls */}
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 28 }}>
          <button
            onClick={goPrev}
            style={{
              background: "rgba(255,255,255,0.1)",
              border: "none",
              borderRadius: "50%",
              width: 40,
              height: 40,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              color: "#fff",
            }}
          >
            <ChevronLeft size={20} />
          </button>

          <button
            onClick={() => setIsPlaying((p) => !p)}
            style={{
              background: "#fff",
              border: "none",
              borderRadius: 6,
              padding: "10px 24px",
              fontWeight: 600,
              fontSize: 14,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 6,
              color: "#0a0a0a",
              fontFamily: "inherit",
            }}
          >
            {isPlaying ? <><Pause size={15} /> Pause</> : <><Play size={15} /> Play</>}
          </button>

          <button
            onClick={goNext}
            style={{
              background: "rgba(255,255,255,0.1)",
              border: "none",
              borderRadius: "50%",
              width: 40,
              height: 40,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              color: "#fff",
            }}
          >
            <ChevronRight size={20} />
          </button>
        </div>

        {/* Dots */}
        <div style={{ display: "flex", gap: 6, marginTop: 20 }}>
          {frames.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrent(i)}
              style={{
                background: i === current ? "#fff" : "rgba(255,255,255,0.25)",
                border: "none",
                borderRadius: 999,
                width: i === current ? 24 : 6,
                height: 6,
                cursor: "pointer",
                padding: 0,
                transition: "width 0.2s, background 0.2s",
              }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
