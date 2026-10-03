# ClipForge AI: Craftora Submission (CodeBlitz 2.0)

Copy each field below into the Craftora "Create squad project" form. Fields marked **required** must be filled; the rest are optional.

---

## 1. Project basics

### Project name (required)

```
ClipForge AI
```

### Project tagline (required: max 20 words / 120 characters)

```
Chat a topic. Get an expert-level short video: researched, verified, approved by you.
```

13 words / 85 characters

### Project logo (required: square PNG or JPG, max 5 MB)

Use a square 1024x1024 image: the ClipForge AI wordmark or a "CF" mark on a black background with a neon red (#ff1744) glowing border, plus the red crewmate from the deck. Export it as PNG under 5 MB.

---

## 2. Project description (required, paste into the Markdown tab)

````markdown
# ClipForge AI

> **Chat a topic. Get an expert-level short video: researched, verified, approved by you.**

ClipForge AI is a chat-native production studio that behaves like an executive producer. You message a Telegram bot with a topic (text or voice note). It researches the topic on the live web, pitches angles, writes a fact-checked script, shows a free storyboard, and **only renders after you approve**. Every run costs $0 in API bills because it runs on free tiers.

Built by **Team Runtime Rebels** for **CodeBlitz 2.0 · AI Automation**.

## The problem

Short-form video wins attention, but making a good Short is broken:

- **Time sink:** 3-5 hours per Short for research, scripting, voiceover, clip matching and rendering.
- **AI slop:** one-click generators produce generic, unverified, hallucinated content.
- **Platform penalties:** algorithms push down low-retention, templated synthetic media.
- **No creative input:** existing tools generate blindly and never ask "what is your unique angle?"

## The solution

One chat prompt becomes one fact-checked, retention-designed video, with the human in control at every important step.

| Gate | What you see in Telegram | What happens after you tap |
|---|---|---|
| **Gate 1: Angle** | 3 angle pitches (contrarian / escalating story / curiosity gap) or your own custom angle | Web-grounded research, a 10-scene script with two hooks, and a fact-check pass |
| **Gate 2: Storyboard and hook** | A contact sheet of 10 AI frames, with Hook A / Hook B buttons | Per-scene ElevenLabs voiceover, then an ffmpeg render |
| **Gate 3: Final video** | The finished 1080x1920 video with Upload / Keep buttons | YouTube upload plus an email notification |

Because the storyboard is approved before any voice or render is generated, nothing paid is wasted on a bad idea ("**Zero Waste**").

## Key features

1. **Chat-first control:** text or voice notes through Telegram (Groq Whisper transcribes voice).
2. **Producer interview:** the agent pitches 3 angles with producer notes and extracts your unique take.
3. **Fact-checking engine:** Gemini with Google Search grounding produces research notes and a source list. A second pass flags unsupported claims in the script.
4. **Three human-in-the-loop approval gates:** Angle, Storyboard/Hook, Final video.
5. **A/B hooks:** `hook_a` (curiosity gap) vs `hook_b` (contrarian), each with a matching loop-closing line so the ending flows back into the opening.
6. **Retention design:** 10 scenes, 8-14 word narration, alternating Ken Burns zoom, word-by-word highlighted captions, keyword banners, and optional music auto-ducked under the voice.
7. **Free storyboard preview:** 10 AI frames merged into one contact sheet before any voice is generated.
8. **Creator identity:** a persistent profile (ElevenLabs voice ID, tone, language, visual style).
9. **One-tap publishing:** YouTube upload (private by default), email notification, and error alerts back to Telegram.
10. **Three.js control-room dashboard:** an animated 3D view of the pipeline with a bot mascot, approval-gate shields, fact-check status and credit meters.

## How it works

```
Telegram -> n8n trigger -> (voice? Groq Whisper) -> route
  -> Gate 1 Angle -> Research -> Script -> Fact-check -> Storyboard
  -> Gate 2 Hook -> ElevenLabs voice -> ffmpeg render
  -> Gate 3 Final -> YouTube upload + email
```

- 61-node n8n workflow orchestrates the whole flow.
- Run state lives in n8n workflow static data, with Telegram inline-button callbacks (`type|runId|arg`).
- `render.py` (ffmpeg) builds a 1080x1920 @ 30 fps video with Ken Burns motion, ASS captions and music ducking.
- Only 4 Gemini calls per video (angles, research, script, fact-check).

## Why it is different

| | Conventional AI video bots | ClipForge AI |
|---|---|---|
| Workflow | Blind single prompt to video | Interview-first, collaborative ideation |
| Accuracy | Hallucinations and fluff | Web-grounded research with cited sources plus a fact-check pass |
| User control | Zero preview, fire-and-forget | 3 approval gates |
| Cost | Paid generation on every run | Free image preview before any voice or render |
| Branding | Identical templates | Persistent creator profile and ElevenLabs voice |
| Feedback | Static generation | Roadmap: analytics feedback loop into future prompts |

## Tech stack

n8n (Docker) · Telegram Bot API · Google Gemini 2.5 Flash (Search grounding) · Groq Whisper · ElevenLabs (`eleven_multilingual_v2`) · Pollinations (Flux) · ffmpeg + Python · ngrok · YouTube Data API v3 · SMTP · Three.js / React

## Impact and roadmap

Audience rings: **solo creators -> educators -> enterprises**.

- **Phase 1 (MVP):** Telegram bot, n8n pipeline, ElevenLabs narration, YouTube Shorts upload.
- **Phase 2 (cross-platform):** WhatsApp Business, Instagram Reels, TikTok, Hindi and English voice localization.
- **Phase 3 (self-optimizing agent):** weekly YouTube Analytics pull, with retention and view metrics fed back into script prompts.

## Team: Runtime Rebels

Shiv Dixit · Shreyash Tekriwal · Subham Gupta · Rahul Yadav

> *We don't automate generic videos. We automate expertise, empowering anyone to turn an idea into trusted, high-retention content in minutes.*
````

---

## 3. Submission links

### GitHub repository (required)

```
https://github.com/<your-org>/<clipforge-repo>
```

Suggested repo contents: `ClipForge_AI.workflow.json`, `Dockerfile`, `docker-compose.yml`, `.env.example` (never commit `clipforge.env`), `clipforge/bin/render.py`, the Three.js dashboard folder, and a README.

### Live deployed link (optional)

```
https://<your-dashboard>.vercel.app
```

Deploy the Three.js dashboard (demo mode) or the landing page on Vercel. This must be the working app, not the demo video.

### Demo video (required)

```
https://youtube.com/watch?v=<video-id>
```

Suggested 3-minute walkthrough:

1. Show the problem (3-5 hours per Short, AI slop).
2. Send a voice note topic in Telegram, then tap an angle.
3. Show the research sources, the fact-check result and the storyboard contact sheet (nothing paid rendered yet).
4. Choose Hook B and show the pipeline moving through voice and render.
5. Play the final video, tap Upload to YouTube, and show the email and link.
6. Close with: 3 gates, $0 cost, fact-checked, loop-ending retention design, and the roadmap.

### Tech stack used (optional)

```
n8n, Docker, Telegram Bot API, Gemini 2.5 Flash, Groq Whisper, ElevenLabs, Pollinations (Flux), ffmpeg, Python, ngrok, YouTube Data API v3, Three.js, React
```

### Contract address (optional)

Leave blank (no smart contract).

### Extra links (optional, up to 5)

| # | Link | Purpose |
|---|---|---|
| 1 | Pitch deck (PDF, hosted on Drive or GitHub) | Problem, solution, innovation, roadmap |
| 2 | `https://t.me/<your_bot_username>` | Try the Telegram bot |
| 3 | Setup guide (README or doc link) | Reproducible setup |
| 4 | YouTube Short produced by ClipForge | Proof of output |
| 5 | LinkedIn or X post about the project | Optional |

---

## 4. Screenshots (optional: up to 3, max 500 KB each)

1. Telegram chat showing the 3 angle buttons and the storyboard contact sheet with Hook A / Hook B.
2. The Three.js dashboard with the bot, pipeline ring and approval-gate shield.
3. The n8n workflow canvas (61 nodes) or the final video frame with word-by-word captions.

Compress each to under 500 KB (JPG at 1280 px wide is usually enough).

---

## 5. Before you submit

- [ ] Run the full pipeline once end to end, and make sure what the description claims actually works on demo day.
- [ ] The pitch deck mentions Perplexity/Tavily, Creatomate and Airtable, but the built workflow uses Gemini Search grounding, ffmpeg (`render.py`) and n8n static data. Either update the slides or keep the description as written above, so judges see one consistent story.
- [ ] YouTube uploads from unverified API projects are forced private, and ElevenLabs free-tier voices have no commercial licence. Mention this if asked.
- [ ] Never commit `clipforge.env` or any API key, and don't show keys in the demo video.
- [ ] Demo video link is separate from the live app link.
- [ ] Tagline is within 20 words / 120 characters (currently 13 / 85).
- [ ] Logo is square and under 5 MB; screenshots are under 500 KB each.
