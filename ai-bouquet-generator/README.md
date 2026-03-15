# 🌸 AI Bouquet Generator — Floragenix

A multimodal AI web application that generates beautiful floral bouquet designs using **Google's Gemini API**. Describe your vision, pick your colors, and let AI craft bespoke floral arrangements with poetic descriptions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![Gemini API](https://img.shields.io/badge/Gemini_API-1.5_Flash-orange?logo=google)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-Ready-4285F4?logo=googlecloud)

---

## ✨ Features

- 🌺 **AI-Powered Bouquet Design** — Gemini 1.5 Flash generates detailed bouquet descriptions
- 🖼️ **Image Generation** — Gemini 2.0 Flash Experimental for visual generation (requires billing-enabled GCP project)
- 🎨 **Custom Color Palette** — Pick from 10 color chips
- 💐 **Occasion & Style Selector** — Wedding, Birthday, Anniversary, 7 style modes
- 🌿 **Care Tips & Symbolism** — Every bouquet comes with florist-level detail
- 📱 **Responsive Design** — Works beautifully on mobile and desktop

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-bouquet-generator.git
cd ai-bouquet-generator
```

### 2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
cp .env.example .env
```
Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```
Get your key at: https://aistudio.google.com/app/apikey

### 4. Run the app
```bash
python app.py
```
Open http://localhost:5000 in your browser.

---

## 🌐 Deploy to Railway / Render / Fly.io

### Railway (recommended — free tier)
1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add `GEMINI_API_KEY` as an environment variable
4. Deploy! 🚀

### Render
1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add `GEMINI_API_KEY` in Environment Variables

---

## 🏗️ Project Structure

```
ai-bouquet-generator/
├── app.py                  # Flask backend + Gemini API logic
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment config
├── .env.example           # Environment variables template
├── templates/
│   └── index.html         # Main UI template
└── static/
    ├── css/style.css      # Elegant floral styling
    └── js/main.js         # Frontend interactivity
```

---

## 🔑 API Usage

| API | Usage | Model |
|-----|-------|-------|
| Gemini API | Bouquet description generation | `gemini-1.5-flash` |
| Gemini API | Image generation (optional) | `gemini-2.0-flash-exp` |
| Vertex AI | Alternative deployment path | Configurable |

---

## 📸 Screenshots

> Add screenshots here after deployment

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Gunicorn
- **AI**: Google Gemini API (`google-generativeai`)
- **Frontend**: Vanilla HTML/CSS/JS, Cormorant Garamond + Jost fonts
- **Deployment**: Railway / Render / Heroku compatible

---

## 📄 License

MIT License — feel free to use and modify.

---

*Built with 🌸 and Google Gemini*
