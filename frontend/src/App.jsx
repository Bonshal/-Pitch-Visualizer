import { AnimatePresence, motion } from "framer-motion";
import Header from "./components/layout/Header";
import ProgressStepper from "./components/layout/ProgressStepper";
import PitchInput from "./components/pitch/PitchInput";
import OutlinePreview from "./components/review/OutlinePreview";
import StoryboardGallery from "./components/storyboard/StoryboardGallery";
import usePitchStore from "./store/pitchStore";

const pageVariants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit:    { opacity: 0, y: -12 },
};

function PhaseRouter() {
  const { phase } = usePitchStore();
  return (
    <AnimatePresence mode="wait">
      {phase === "input" && (
        <motion.div key="input" {...pageVariants} transition={{ duration: 0.28 }}>
          <PitchInput />
        </motion.div>
      )}
      {phase === "review" && (
        <motion.div key="review" {...pageVariants} transition={{ duration: 0.28 }}>
          <OutlinePreview />
        </motion.div>
      )}
      {phase === "generate" && (
        <motion.div key="generate" {...pageVariants} transition={{ duration: 0.28 }}>
          <StoryboardGallery />
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", background: "#fff" }}>
      <Header />
      <ProgressStepper />
      <main style={{ flex: 1 }}>
        <PhaseRouter />
      </main>
      <footer
        style={{
          borderTop: "1px solid #e0e0e0",
          padding: "20px 24px",
          textAlign: "center",
          fontSize: 12,
          color: "#a0a0a0",
        }}
      >
        Pitch Visualizer — Powered by Gemini &amp; FLUX.2 [max]
      </footer>
    </div>
  );
}
