import { useState } from "react";
import { motion } from "framer-motion";
import { Send, Loader2 } from "lucide-react";
import usePitchStore from "../../store/pitchStore";
import { analyzePitch } from "../../api/client";
import StyleGallery from "./StyleGallery";

export default function PitchInput() {
  const {
    pitchText, setPitchText,
    selectedStyle,
    isAnalyzing, setIsAnalyzing,
    setOutline, setPhase,
  } = usePitchStore();

  const [error, setError] = useState(null);
  const canSubmit = pitchText.trim().length >= 20 && selectedStyle && !isAnalyzing;

  const handleSubmit = async () => {
    if (!canSubmit) return;
    setError(null);
    setIsAnalyzing(true);
    try {
      const result = await analyzePitch(pitchText, selectedStyle);
      setOutline(result.entities, result.scenes);
      setPhase("review");
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      style={{ maxWidth: 900, margin: "0 auto", padding: "56px 24px" }}
    >
      {/* Hero */}
      <div style={{ marginBottom: 48 }}>
        <h2
          style={{
            fontSize: 42,
            fontWeight: 800,
            letterSpacing: "-0.04em",
            color: "#0a0a0a",
            lineHeight: 1.1,
            margin: 0,
          }}
        >
          Turn your pitch
          <br />
          into a storyboard.
        </h2>
        <p
          style={{
            marginTop: 16,
            fontSize: 16,
            color: "#6b6b6b",
            lineHeight: 1.6,
            maxWidth: 520,
          }}
        >
          Paste your business pitch, pick a visual style, and our AI director
          will craft a cinematic storyboard — frame by frame.
        </p>
      </div>

      {/* Style Gallery */}
      <div style={{ marginBottom: 36 }}>
        <StyleGallery />
      </div>

      {/* Pitch Text Area */}
      <div style={{ marginBottom: 24 }}>
        <span className="section-label" style={{ display: "block", marginBottom: 8 }}>
          Your Pitch
        </span>
        <textarea
          id="pitch-text"
          rows={7}
          placeholder="Paste or type your pitch here — describe the problem you solve, your target user, and the transformation your product delivers."
          value={pitchText}
          onChange={(e) => setPitchText(e.target.value)}
          className="input"
          style={{ fontSize: 15, lineHeight: 1.7, padding: "16px 20px" }}
        />
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: 6,
            fontSize: 12,
            color: "#a0a0a0",
          }}
        >
          <span>
            {pitchText.length < 20
              ? `${20 - pitchText.length} more characters needed`
              : `${pitchText.length} characters`}
          </span>
          {selectedStyle && (
            <span style={{ fontWeight: 500, color: "#3a3a3a" }}>
              Style: {selectedStyle.replace(/_/g, " ")}
            </span>
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            marginBottom: 20,
            padding: "12px 16px",
            background: "#f5f5f5",
            border: "1px solid #e0e0e0",
            borderRadius: 8,
            fontSize: 13,
            color: "#3a3a3a",
          }}
        >
          {error}
        </motion.div>
      )}

      {/* Submit */}
      <button
        className="btn-primary"
        onClick={handleSubmit}
        disabled={!canSubmit}
        style={{ fontSize: 15, padding: "14px 36px" }}
      >
        {isAnalyzing ? (
          <>
            <Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} />
            Analyzing...
          </>
        ) : (
          <>
            <Send size={16} />
            Analyze &amp; Storyboard
          </>
        )}
      </button>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </motion.div>
  );
}
