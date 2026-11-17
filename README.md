# 🏥 Medical AI Chatbot

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=2303A52440/agentic-ai_project&branch=main&mainModule=app.py)
[![GitHub stars](https://img.shields.io/github/stars/2303A52440/agentic-ai_project?style=social)](https://github.com/2303A52440/agentic-ai_project)

> 💻 **Local Address:** `http://localhost:8501` *(Opens in browser when running locally on your PC)*  
> 🌐 **Default Port:** `8501`  
> ⚡ **Hardware Acceleration:** Groq LPU Inference Core (`qwen/qwen3.8-27b`)  
> 🩺 **Clinical Architecture:** Decision Support, SOAP Generation, Specialty Routing & Physiological Calculators  

---

## 📌 Overview

**Medical AI Chatbot** is a professional medical information and clinical decision-support application built with **Streamlit** and **Groq LPU acceleration**. It provides real-time clinical consultations across 10 medical specialties, automated SOAP encounter note generation, physiological calculators (BMI, MAP), and emergency triage red-flag detection.

---

## 🚀 How to Run and Open `http://localhost:8501`

> ⚠️ **Note:** `localhost:8501` is a local address on your personal computer. It requires running the application locally on your machine following these 4 steps:

### 1. Clone Repository
```bash
git clone https://github.com/2303A52440/agentic-ai_project.git
cd agentic-ai_project
```

### 2. Configure Environment (`.env`)
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Add your free Groq API key from [console.groq.com/keys](https://console.groq.com/keys):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
PORT=8501
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Application
Run:
```bash
python run.py
```
*or directly with Streamlit:*
```bash
python -m streamlit run app.py
```

Your browser will automatically open and connect to:  
👉 **`http://localhost:8501`**

---

## 🌐 Free 1-Click Cloud Deployment (Public Link)

Want a live public link anyone can access online? Deploy it for free on **Streamlit Community Cloud**:

1. Click the button below:  
   [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=2303A52440/agentic-ai_project&branch=main&mainModule=app.py)
2. Sign in with GitHub and select repository **`2303A52440/agentic-ai_project`**.
3. Under **Advanced Settings > Secrets**, paste your Groq API key:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```
4. Click **Deploy!** You will get a permanent public URL (e.g. `https://agentic-ai-project.streamlit.app`).

---

## ✨ Clinical Capabilities & Features

| Capability | Technical Details |
|---|---|
| ⚡ **Sub-Second Groq Inference** | Powered by Groq LPUs running high-speed clinical models at ~350+ tokens/sec. |
| 🔬 **10 Specialty Departments** | General Medicine, Cardiology, Neurology, Orthopedics, Pediatrics, Dermatology, Pulmonology, Pharmacology, Nutrition, Psychiatry. |
| 🎭 **3 Clinical Personas** | Switch between **Patient-Friendly**, **Clinical/Physician (SOAP & Differential)**, and **Pharmacology Deep-Dive**. |
| 📋 **Automated SOAP Notes** | 1-Click synthesis of full patient encounters into structured SOAP notes (Subjective, Objective, Assessment, Plan). |
| ⚖️ **Clinical Calculators** | Real-time Body Mass Index (BMI) WHO stratification and Mean Arterial Pressure (MAP) organ perfusion estimator. |
| 🚨 **Emergency Triage Matrix** | Rapid-reference protocol for Acute Coronary Syndrome, BE-FAST Acute Stroke, Sepsis, and Respiratory Distress. |
| 📥 **Transcript Export** | Download encrypted-session consultation transcripts as Markdown (`.md`). |

---

## 📁 Repository Structure

```
agentic-ai_project/
├── .streamlit/
│   └── config.toml      # Server configuration locking port 8501
├── app.py               # Main Clinical Intelligence application interface
├── run.py               # Direct one-command entry point for localhost:8501
├── config.py            # Clinical specialties, prompts, and inference parameters
├── llm_client.py        # Groq LPU API client and SOAP note generator
├── styles.py            # Clinical slate-teal custom styling and responsive UI
├── requirements.txt     # Python dependency specifications
├── .env.example         # Template for environment variables
├── .gitignore           # Ignores sensitive keys (.env) and byte-caches
└── README.md            # Comprehensive project documentation
```

---

## 📄 License
This project is licensed under the MIT License.
