import { create } from "zustand";

// Provider definitions (metadata for the UI)
export const PROVIDERS = [
  {
    id:          "bfl",
    name:        "Black Forest Labs",
    shortName:   "BFL FLUX.2",
    description: "Best quality. Native multi-reference character consistency.",
    fields:      ["api_key"],
  },
  {
    id:          "openai",
    name:        "OpenAI DALL-E 3",
    shortName:   "DALL·E 3",
    description: "High quality, fast. Text-to-image only (no character references).",
    fields:      ["api_key"],
  },
  {
    id:          "nano_banana",
    name:        "Google Nano Banana",
    shortName:   "Nano Banana",
    description: "Google DeepMind's Gemini Image models. Supports up to 14 reference images.",
    fields:      ["api_key"],
  },
  {
    id:          "bedrock",
    name:        "AWS Bedrock",
    shortName:   "Bedrock",
    description: "Stable Diffusion XL or Amazon Titan via your AWS account.",
    fields:      ["aws_access_key_id", "aws_secret_access_key", "region", "model_id"],
  },
];

const usePitchStore = create((set, get) => ({
  // ── Phase ────────────────────────────────────────────────────────────
  phase:    "input",
  setPhase: (phase) => set({ phase }),

  // ── Pitch input ──────────────────────────────────────────────────────
  pitchText:    "",
  setPitchText: (pitchText) => set({ pitchText }),

  selectedStyle:    null,
  setSelectedStyle: (selectedStyle) => set({ selectedStyle }),

  // ── Director output ──────────────────────────────────────────────────
  entities: [],
  scenes:   [],
  setOutline: (entities, scenes) => set({ entities, scenes }),

  updateEntity: (id, updates) =>
    set((s) => ({ entities: s.entities.map((e) => (e.id === id ? { ...e, ...updates } : e)) })),

  updateScene: (id, updates) =>
    set((s) => ({ scenes: s.scenes.map((sc) => (sc.id === id ? { ...sc, ...updates } : sc)) })),

  deleteScene: (id) =>
    set((s) => ({ scenes: s.scenes.filter((sc) => sc.id !== id) })),

  // ── Provider / credentials ───────────────────────────────────────────
  provider:        "bfl",      // provider id
  setProvider:     (provider) => set({ provider, credentials: {} }),

  credentials:     {},         // { api_key, aws_access_key_id, ... }
  setCredential:   (field, value) =>
    set((s) => ({ credentials: { ...s.credentials, [field]: value } })),

  // ── Generation state ─────────────────────────────────────────────────
  isAnalyzing:      false,
  setIsAnalyzing:   (v) => set({ isAnalyzing: v }),

  isGenerating:     false,
  setIsGenerating:  (v) => set({ isGenerating: v }),

  statusMessage:    "",
  setStatusMessage: (msg) => set({ statusMessage: msg }),

  conceptImages:  {},
  addConceptImage: (entityId, url) =>
    set((s) => ({ conceptImages: { ...s.conceptImages, [entityId]: url } })),

  frames:    [],
  addFrame:  (frame) => set((s) => ({ frames: [...s.frames, frame] })),

  resetGeneration: () => set({ isGenerating: false, statusMessage: "", conceptImages: {}, frames: [] }),

  resetAll: () =>
    set({
      phase: "input", pitchText: "", selectedStyle: null,
      entities: [], scenes: [],
      isAnalyzing: false, isGenerating: false,
      statusMessage: "", conceptImages: {}, frames: [],
    }),
}));

export default usePitchStore;
