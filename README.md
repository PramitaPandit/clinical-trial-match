# Clinical Trial Match

**AI-powered platform connecting patients to life-saving clinical trials in seconds.**

[Live Demo](https://your-app-name.streamlit.app) · [Codex Creator Challenge 2025](https://codex.com)

---

## The Problem

76% of clinical trials fail to meet enrollment targets, costing the pharmaceutical industry $100M+ annually. Meanwhile, patients with conditions matching open trials spend an average of 6+ months searching for treatments — most never find them.

The data exists. The matching logic is straightforward. What's missing is the connection.

## The Solution

Clinical Trial Match closes that gap. It reads unstructured medical records (typed notes, EMR exports, or PDFs), extracts clinical entities using AI, and queries 400,000+ active trials in real-time — surfacing matches with eligibility scores and clinical rationale.

A 6-month manual search becomes a 2-minute automated process.

## Features

- **Medical NLP extraction** — Pulls diagnoses, demographics, and medications from unstructured records
- **Real-time trial search** — Queries the official ClinicalTrials.gov registry (400K+ studies)
- **AI eligibility scoring** — Each trial scored 0-100% with clinical rationale
- **Direct enrollment paths** — Links to study protocols and trial coordinators
- **Multi-page workflow** — Landing → Input → Results with persistent session state
- **PDF & text upload** — Handles unstructured medical documents

## Tech Stack

- **Frontend:** Streamlit + custom CSS (Instrument Serif + Inter typography)
- **AI:** Google Gemini 2.5 Flash
- **Data:** ClinicalTrials.gov API v2
- **Language:** Python 3.10+
- **Document parsing:** PyPDF2

## Setup

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API key ([get one free here](https://aistudio.google.com/))

### Installation

```bash
# Clone the repo
git clone https://github.com/pramitapandit/clinical-trial-match.git
cd clinical-trial-match

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GOOGLE_API_KEY=your-key-here" > .env

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## How It Works

1. **Enter patient data** — Type clinical info or upload medical documents
2. **AI extraction** — Gemini parses unstructured text into structured medical entities
3. **Trial search** — Queries ClinicalTrials.gov filtered by condition and location
4. **Eligibility analysis** — Each trial scored against patient profile with rationale
5. **Direct action** — Click through to official trial pages and contact coordinators

## Architecture

User Input (text/PDF)
↓
Gemini 2.5 Flash (extraction)
↓
Structured patient profile
↓
ClinicalTrials.gov API
↓
Top 10 matching trials
↓
Gemini (per-trial eligibility scoring)
↓
Ranked results with rationale

## Project Structure
clinical-trial-match/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # API keys (not committed)
├── .gitignore         # Git exclusions
└── README.md          # This file

## Roadmap

- [ ] Add support for more EMR formats (HL7 FHIR, CCD)
- [ ] Multi-language support for international trials
- [ ] Saved searches and patient profiles
- [ ] Integration with telehealth platforms
- [ ] Detailed eligibility breakdown (inclusion/exclusion criteria matching)

## About

Built by **Pramita Pandit** — a Clinical Systems Analyst with 6+ years bridging clinical trial operations and healthcare AI. Former Solutions Designer at Calyx (IRT/RTSM systems for 15+ pharmaceutical trials). Published 2 IEEE papers on ML optimization. Dual MS in Computer Science and Business Analytics.

This project emerged from witnessing the trial recruitment crisis firsthand at Calyx — pharmaceutical sponsors writing off failed studies while eligible patients had no way to discover trials they qualified for.

## Disclaimer

This tool is for informational and research purposes only. It does not constitute medical advice, diagnosis, or treatment. All clinical decisions regarding trial enrollment should be made in consultation with qualified healthcare professionals.

## License

MIT License — see LICENSE file for details.

## Acknowledgments

- ClinicalTrials.gov for the open trials registry API
- Google Gemini team for the AI infrastructure
- Streamlit for the rapid prototyping framework
- Codex Creator Challenge 2025 for the catalyst to build this

---

**Connect:** 
[LinkedIn](https://linkedin.com/in/pramita-pandit) · [GitHub](https://github.com/pramitapandit) · p4pandit7@gmail.com