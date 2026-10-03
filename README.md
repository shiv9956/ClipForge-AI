# ClipForge AI

ClipForge AI is an autonomous, research-backed short-form video production platform designed to help creators turn raw ideas into verified, publish-ready Reels, Shorts, and TikToks. 

It uses a powerful **n8n backend** integrated directly with **Telegram** for ease of access, while providing a beautiful **React (Vite) frontend** for creators to launch and manage their studio.

![ClipForge AI Dashboard](public/screenshots/hero.jpg)

## Features

- **AI Angle Discovery**: Generates 4 unique creator angles using Google Gemini to ensure your content stands out.
- **Research & Verification**: Pulls verified academic papers and data points to back up your claims.
- **Automated Neural Voiceover**: Integrates seamlessly with ElevenLabs for high-quality, professional voice synthesis.
- **Fact-Checked Scripting**: Auto-structures your script into viral sections and flags any unverified claims for review.
- **Semantic B-Roll**: Matches footage semantically to every sentence in your script.
- **NLE Editing & Rendering**: Render your 1080x1920 60FPS master video automatically with YouTube/TikTok metadata.

## Architecture

- **Frontend**: React, Vite, TailwindCSS (for the landing page and dashboard).
- **Backend**: Self-hosted `n8n` orchestrated via Docker Compose.
- **Integrations**: Telegram Bot API, Gemini API, ElevenLabs API, YouTube Data API.
- **Tunneling**: Ngrok is used to expose the local n8n instance securely to the public web for webhook processing.

## Setup Instructions

### 1. Prerequisites
- Docker and Docker Compose
- Node.js and npm
- Ngrok
- API Keys: Telegram Bot Token, Google Gemini, ElevenLabs, and YouTube OAuth Client ID.

### 2. Backend (n8n & Workflow)
1. Navigate to the `backend/` folder.
2. Configure your `clipforge.env` file containing your keys (including your `N8N_EDITOR_BASE_URL`).
3. Ensure Ngrok is running and forwarding to port `5678`.
4. Run `docker compose up -d --build --force-recreate` to start the backend.
5. Import `ClipForge_AI.workflow.json` into your n8n instance and activate the webhooks.

### 3. Frontend (Web Studio)
1. Navigate to the root folder.
2. Configure your `.env` file with your Gemini/ElevenLabs keys to power the visual demo.
3. Install dependencies: `npm install`
4. Run the development server: `npm run dev`

Launch the app from the frontend and connect directly to your Telegram bot to start forging!
