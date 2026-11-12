# 🩺 MediCare AI — Clinical Medical Agentic Chatbot

> 🚀 **Application URL:** [http://localhost:3000](http://localhost:3000)  
> 🌐 **Local Host:** `http://localhost:3000` (Port: `3000`)  
> ⚡ **Inference Engine:** Groq High-Speed Medical AI Core  

---

## 📌 Overview
**MediCare AI** is a professional, clinical-grade medical intelligence assistant built with **FastAPI**, **LangGraph**, and **Groq**. It provides autonomous symptom triage, red-flag emergency detection, BMI & hydration calculations, and evidence-based self-care guidance.

---

## ✨ Features
* 🩺 **Clinical Symptom Triage:** Structured assessments with possible etiologies and recovery guidelines.
* 🚨 **Red-Flag Emergency Detector:** Alerts users when symptoms indicate acute medical emergencies (chest pain, stroke signs, breathing distress).
* ⚖️ **BMI & Dosage Calculator:** Accurately computes Body Mass Index, target weight ranges, and daily hydration goals.
* ⚡ **Sub-Second Groq Inference:** Powered by Groq for instantaneous answers.
* 💻 **Modern Professional Web UI:** Responsive dark-mode interface with clinical intake prompt cards.

---

## 🚀 Quick Start (Localhost:3000)

### 1. Clone & Setup
```bash
git clone https://github.com/2303A52440/agentic-ai_project.git
cd agentic-ai_project
```

### 2. Configure Environment (`.env`)
```env
GROQ_API_KEY=your_groq_api_key_here
PORT=3000
```

### 3. Install & Run
```bash
pip install -r requirements.txt
python app.py
```
Open **`http://localhost:3000`** in your browser.

---

## 🐳 Docker Deployment
```bash
docker build -t medicare-ai .
docker run -d -p 3000:3000 --env-file .env medicare-ai
```

---

## ⚠️ Medical Disclaimer
*MediCare AI is designed for informational and educational triage purposes only. It does not provide formal medical diagnosis, physical examinations, or prescriptions. In a medical emergency, call 911 (US/CA), 112 (EU), or your local emergency dispatch immediately.*
