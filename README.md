---
title: Pitch Visualizer
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---
# 🎬 Context-Aware Storyboard Engine (Pitch Visualizer)

> **Transform unstructured business pitches into cinematic, human-centric visual storyboards through multi-agent AI orchestration.**

The Pitch Visualizer is a monolithic, server-side rendered FastAPI web application designed to bridge the gap between abstract product ideation and tangible UX vision. Instead of forcing teams to manually sketch use-cases, this engine ingests rough business pitches and automatically engineers a 5-to-8 panel storyboard

---

## 🌟 Key Capabilities

- **Automated UX Flow Extraction:** Translates raw text into an industry-standard narrative arc (Pain Point → Discovery → Interaction → Solution → Reflection).
- **Agnostic Image Generation Engine:** Seamlessly dynamically routes inference requests across your choice of frontier models (**Hugging Face FLUX.1**, **Black Forest Labs**, **OpenAI DALL-E 3**, **Google Nano Banana**, and **AWS Bedrock**).
- **Zero-Disk Security Model:** Complete session isolation. External API credentials (both for the Director LLM and Image Generators) are provided dynamically via the web UI and held strictly in volatile, in-memory storage during generation.
- **Custom Style Injection:** Generates frames in highly opinionated art profiles (e.g., *Noir & Neon*, *Corporate Vector*) or via user-defined custom prompt blueprints.
- **Live SSE Streaming:** Uses Server-Sent Events to stream generation progress (text analysis, concept art, frames) directly to the UI in real-time.

---

## 🧠 Methodology & Prompt Engineering Architecture

One of the most notoriously difficult challenges with sequential AI image generation is **Visual Drift**—characters and environments spontaneously changing appearance, clothing, and structure from frame to frame. We engineered a multi-stage pipeline to strictly eliminate this.

### Phase 1: The Director (UX Extraction)
We utilize a heavily engineered **Chain-of-Thought System Prompt** feeding into Google Gemini. The LLM does not just blindly write prompts. Instead, it is forced to:
1. Extract a single **User Persona**.
2. Build a **Visual Identity Bible** (locking exact hair color, clothing style, and architectural metadata etc).
3. Map an exact 5-to-8 step emotional flow heavily interleaving *real-world* moments with *app/UI* interactions.
4. Output a rigid JSON schema mapping explicit "Captions" for human reading and 70-word "Refined Image Prompts" for the generative models.

### Phase 2: The Asset Forge (Visual Continuity Engine)
Before generating a single storyboard frame, the backend  kicks in:
1. **Blueprint Locking:** It formats the Director's extracted "Entity" definitions into hardcoded prompt appendages.
2. **Concept Art Generation (Optional):** It generates initial, static reference images of the protagonist.
3. **Multi-Reference Generation:** For all subsequent frames, the engine forces the image model to strictly adhere to the previously generated textual blueprints (and visual reference images where supported), mathematically anchoring the visual aesthetic across the entire 8-panel journey.

---

## 🛠️ Setup & Execution

Unlike convoluted microservice architectures, we stripped the application down to a lightning-fast, zero-build FastAPI server serving pure vanilla HTML/Jinja2 templates. There is no React/NPM build step required.

### 1. Environment Configuration
Ensure you have Python 3.10+ installed. Navigate to the `backend` directory and set up your environment:

```bash
cd backend
python -m venv .venv
# Activate the virtual environment
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Base API Configuration (Optional)
The system is entirely plug-and-play via the browser UI. However, if you are a developer hosting the system, you can seed default API keys to avoid typing them repeatedly.
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY="your-google-gemini-key-here"
```

### 3. Running the Server
Run the FastAPI application via `uvicorn`:
```bash
uvicorn app.main:app --reload --port 8000
```
**Open your browser to: [http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔑 Using the Application (API Key Management)

The application is designed to be publicly hostable. All compute costs are deferred securely back to the user via "Bring Your Own Key" (BYOK) inputs directly in the UX.

1. **Load the Web Interface:** Insert your raw, unstructured product pitch.
2. **Director LLM Key:** The system requires a Google Gemini key to parse the pitch text into the structured JSON data format. Input this in the designated `Director LLM Details` box.
3. **Image Provider Selection:** Select the engine that will actually draw the images. You can choose:
   - **Hugging Face:** Input your HF Access Token. Optionally specify a Serverless Inference Model (e.g., `black-forest-labs/FLUX.1-schnell`).
   - **AWS Bedrock:** Select this option to drop down dedicated input fields for your AWS Access Key and Secret Key.
   - **OpenAI / BFL:** Input your standard API keys.
4. **Generate:** The backend receives your temporary keys, runs the isolated multi-agent inference via Server-Sent Events, and wipes the session upon server shutdown.

---

## 📂 Repository Structure

- `backend/app/main.py` — The core FastAPI application and Jinja2 router.
- `backend/app/templates/` — The purely server-side rendered HTML/CSS frontend.
- `backend/app/services/director.py` — The Google GenAI agent responsible for UX extraction and JSON schema locking.
- `backend/app/services/asset_forge.py` — The event-stream generator orchestrating visual continuity.
- `backend/app/services/providers/` — The dynamic routing layer containing completely decoupled integrations for Hugging Face, Bedrock, OpenAI, and Nano Banana.
