import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, ArrowLeft, Users, Clapperboard, KeyRound } from "lucide-react";
import usePitchStore, { PROVIDERS } from "../../store/pitchStore";
import EntityCard from "./EntityCard";
import SceneCard from "./SceneCard";
import { startGeneration } from "../../api/client";

export default function OutlinePreview() {
  const {
    entities, scenes, selectedStyle,
    setPhase, isGenerating, setIsGenerating,
    setStatusMessage, addConceptImage, addFrame, resetGeneration,
    provider, credentials,
  } = usePitchStore();

  const [error, setError] = useState(null);

  const currentProvider = PROVIDERS.find((p) => p.id === provider);
  const hasCredentials  = currentProvider?.fields.some((f) => !!credentials[f]);

  const handleApprove = () => {
    // Validate credentials before firing
    if (!hasCredentials) {
      setError("Please configure your image API credentials in Settings before generating.");
      return;
    }
    setError(null);
    resetGeneration();
    setIsGenerating(true);
    setPhase("generate");

    // Build provider_config from store state
    const providerConfig = { name: provider, ...credentials };

    startGeneration(
      { entities, scenes, selected_style: selectedStyle, provider_config: providerConfig },
      (event) => {
        switch (event.type) {
          case "status":   setStatusMessage(event.message); break;
          case "concept":  addConceptImage(event.entity_id, event.image_url); break;
          case "frame":    addFrame(event); break;
          case "complete": setIsGenerating(false); setStatusMessage(event.message || "Complete!"); break;
          case "error":    setStatusMessage(`Error: ${event.message}`); setIsGenerating(false); break;
        }
      }
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ maxWidth: 900, margin: "0 auto", padding: "48px 24px" }}
    >
      {/* Header */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 32, fontWeight: 800, letterSpacing: "-0.03em", color: "#0a0a0a", margin: "0 0 8px" }}>
          Review your storyboard outline.
        </h2>
        <p style={{ fontSize: 15, color: "#6b6b6b", margin: 0 }}>
          Edit entities and scenes before generating. Changes here define your visual output.
        </p>
      </div>

      {/* Entities */}
      <section style={{ marginBottom: 40 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
          <Users size={15} color="#3a3a3a" />
          <span style={{ fontSize: 14, fontWeight: 700, color: "#0a0a0a" }}>
            Asset Bible — Entities ({entities.length})
          </span>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 12 }}>
          {entities.map((entity, i) => (
            <EntityCard key={entity.id} entity={entity} index={i} />
          ))}
        </div>
      </section>

      <div className="divider" style={{ marginBottom: 40 }} />

      {/* Scenes */}
      <section style={{ marginBottom: 48 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
          <Clapperboard size={15} color="#3a3a3a" />
          <span style={{ fontSize: 14, fontWeight: 700, color: "#0a0a0a" }}>
            Scene Sequence — {scenes.length} Frames
          </span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {scenes.map((scene, i) => (
            <SceneCard key={scene.id} scene={scene} index={i} />
          ))}
        </div>
      </section>

      {/* Credentials warning */}
      {!hasCredentials && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "12px 16px",
            border: "1px solid #e0e0e0",
            borderRadius: 8,
            marginBottom: 20,
            fontSize: 13,
            color: "#3a3a3a",
            background: "#f5f5f5",
          }}
        >
          <KeyRound size={14} color="#6b6b6b" />
          No API credentials configured. Click{" "}
          <strong style={{ color: "#0a0a0a" }}>"Set API Key"</strong>{" "}
          in the top-right corner before generating.
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          style={{
            padding: "12px 16px",
            border: "1px solid #e0e0e0",
            borderRadius: 8,
            marginBottom: 20,
            fontSize: 13,
            color: "#3a3a3a",
            background: "#f5f5f5",
          }}
        >
          {error}
        </div>
      )}

      {/* Actions */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button className="btn-secondary" onClick={() => setPhase("input")}>
          <ArrowLeft size={15} />
          Back to Pitch
        </button>

        <button
          className="btn-primary"
          onClick={handleApprove}
          disabled={isGenerating}
          style={{ fontSize: 15, padding: "14px 36px" }}
        >
          <CheckCircle2 size={16} />
          Approve &amp; Generate
        </button>
      </div>
    </motion.div>
  );
}
