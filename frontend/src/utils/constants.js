/**
 * Art style definitions — mirrored from the backend for UI rendering.
 */
export const STYLES = [
  {
    id: "corporate_vector",
    name: "Corporate Vector",
    description:
      "Clean flat illustrations with minimal shapes and a professional palette. Perfect for SaaS, fintech, and enterprise pitches.",
    emoji: "📊",
    gradient: "from-blue-500 to-cyan-400",
  },
  {
    id: "cinematic_3d",
    name: "Cinematic 3D",
    description:
      "Photorealistic 3D renders with dramatic lighting and depth. Ideal for product showcases and high-impact presentations.",
    emoji: "🎬",
    gradient: "from-amber-500 to-red-500",
  },
  {
    id: "watercolor_story",
    name: "Watercolor Story",
    description:
      "Soft hand-painted textures with warm earthy tones. Great for storytelling, education, and human-centered narratives.",
    emoji: "🎨",
    gradient: "from-rose-400 to-orange-300",
  },
  {
    id: "noir_neon",
    name: "Noir & Neon",
    description:
      "High-contrast cyberpunk aesthetic with neon glows on dark surfaces. Perfect for tech, AI, and futuristic themes.",
    emoji: "🌃",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    id: "retro_pixel",
    name: "Retro Pixel",
    description:
      "Vibrant 16-bit pixel art with nostalgic arcade charm. Ideal for gaming, social media, and playful brand stories.",
    emoji: "👾",
    gradient: "from-green-400 to-emerald-500",
  },
];

/**
 * Phase labels for the progress stepper.
 */
export const PHASES = [
  { id: "input", label: "Write Your Pitch", icon: "Pen" },
  { id: "review", label: "Review Outline", icon: "ScanEye" },
  { id: "generate", label: "Generate Storyboard", icon: "Clapperboard" },
];

/**
 * Emotion emoji map for UI badges.
 */
export const EMOTION_EMOJIS = {
  frustration: "😤",
  confusion: "😕",
  curiosity: "🤔",
  discovery: "💡",
  hope: "🌅",
  determination: "💪",
  breakthrough: "🚀",
  relief: "😌",
  confidence: "😎",
  triumph: "🏆",
  collaboration: "🤝",
  vision: "🔮",
};
