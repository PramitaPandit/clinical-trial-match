import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(
    page_title="Clinical Trial Match",
    page_icon="✛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = ""
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'studies' not in st.session_state:
    st.session_state.studies = None

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600;700;800&display=swap');
    
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    
    .stApp {
        background: #FAFAF7;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        color: #1A1A1A;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 4rem;
        max-width: 1100px;
    }
            
    /* 1. Eliminate the gap between Streamlit elements globally */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }

    /* 2. Target the specific container padding */
    .element-container {
        margin-bottom: -1rem !important; /* Pulls elements closer together */
    }

    /* 3. Reset all default margins on your custom classes */
    .hero-title, .section-title {
        font-family: 'Instrument Serif', serif;
        font-size: 3.2rem;
        line-height: 1.0 !important;
        margin-top: 0px !important;
        margin-bottom: 5px !important;
        display: block !important; /* Ensures it renders as a block */
    }

    .hero-eyebrow, .section-eyebrow {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }

    .hero-desc, .section-text {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }

    /* 1. This kills the gap between ANY two Streamlit elements */
    [data-testid="stVerticalBlock"] > div {
        flex-direction: column;
        display: flex;
        gap: 0rem !important;
    }

    /* 2. Target the heading tags specifically to override Streamlit's defaults */
    h1, h2, h3 {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* 3. The "Nuclear Option" for that Hero Title */
    .hero-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.2rem !important;
        line-height: 1 !important;
        margin-bottom: 1rem !important;
        display: block !important;
    }
    
    /* NAVBAR */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E8E4DC;
    }
    
    .logo-wrap {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .logo-text {
        font-family: 'Instrument Serif', serif;
        font-size: 1.4rem;
        color: #1A1A1A;
        line-height: 1;
    }
    
    .logo-tag {
        font-size: 0.65rem;
        color: #1A4D3F;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 600;
        margin-top: 2px;
    }
    
    /* HERO - tighter, fixed line breaks */
    .hero-grid {
        display: grid;
        grid-template-columns: 1.4fr 1fr;
        gap: 3rem;
        align-items: center;
        margin: 1rem 0 2.5rem 0;
    }
    
    .hero-eyebrow {
        font-size: 0.75rem;
        color: #1A4D3F;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-family: 'Instrument Serif', serif;
        font-size: 3.2rem;
        line-height: 1.1;
        color: #1A1A1A;
        margin-bottom: 1.25rem;
        letter-spacing: -0.02em;
        white-space: normal;
    }
    
    .hero-title em {
        color: #1A4D3F;
        font-style: italic;
        white-space: nowrap;
    }
    
    .hero-desc {
        font-size: 1.05rem;
        color: #5A5A5A;
        line-height: 1.6;
        max-width: 540px;
    }
    
    .hero-visual {
        background: linear-gradient(135deg, #1A4D3F 0%, #0F3A2E 100%);
        border-radius: 8px;
        padding: 2.5rem 2rem;
        color: white;
        position: relative;
        overflow: hidden;
        min-height: 240px;
    }
    
    .hero-visual::before {
        content: '';
        position: absolute;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    
    .visual-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        opacity: 0.7;
        margin-bottom: 1rem;
    }
    
    .visual-stat {
        font-family: 'Instrument Serif', serif;
        font-size: 4rem;
        line-height: 1;
        margin-bottom: 0.75rem;
    }
    
    .visual-text {
        font-size: 0.95rem;
        opacity: 0.9;
        line-height: 1.5;
        max-width: 280px;
    }
    
    /* STATS BAR */
    .stats-bar {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 8px;
        margin: 0 0 3rem 0;
        overflow: hidden;
    }
    
    .stats-bar-item {
        padding: 1.5rem 1.75rem;
        border-right: 1px solid #E8E4DC;
    }
    
    .stats-bar-item:last-child {
        border-right: none;
    }
    
    .sb-num {
        font-family: 'Instrument Serif', serif;
        font-size: 2.25rem;
        color: #1A4D3F;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    
    .sb-label {
        font-size: 0.85rem;
        color: #5A5A5A;
        line-height: 1.4;
    }
    
    /* SECTION - tighter spacing */
    .section {
        margin: 2.5rem 0;
    }
    
    .section-eyebrow {
        font-size: 0.7rem;
        font-weight: 600;
        color: #1A4D3F;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.4rem;
    }
    
    .section-title {
        font-family: 'Instrument Serif', serif;
        font-size: 2.25rem;
        color: #1A1A1A;
        margin-bottom: 0.85rem;
        line-height: 1.15;
        letter-spacing: -0.01em;
    }
    
    .section-title em {
        color: #1A4D3F;
        font-style: italic;
    }
    
    .section-text {
        font-size: 0.98rem;
        color: #5A5A5A;
        line-height: 1.7;
        margin-bottom: 0.75rem;
        max-width: 740px;
    }
    
    .section-text strong {
        color: #1A1A1A;
        font-weight: 600;
    }
    
    /* INFO GRID */
    .info-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .info-card {
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 6px;
        padding: 1.5rem 1.25rem;
        position: relative;
        transition: all 0.2s;
    }
    
    .info-card:hover {
        border-color: #1A4D3F;
        transform: translateY(-2px);
    }
    
    .info-card-num {
        font-family: 'Instrument Serif', serif;
        font-size: 1.85rem;
        color: #1A4D3F;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .info-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 0.4rem;
    }
    
    .info-card-text {
        font-size: 0.85rem;
        color: #5A5A5A;
        line-height: 1.55;
    }
    
    /* CTA */
    .cta-block {
        background: #1A4D3F;
        border-radius: 8px;
        padding: 2.5rem;
        margin: 2.5rem 0 1rem 0;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .cta-block::before {
        content: '';
        position: absolute;
        top: -100px;
        right: -100px;
        width: 300px;
        height: 300px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    
    .cta-block h2 {
        font-family: 'Instrument Serif', serif;
        font-size: 2rem;
        margin-bottom: 0.75rem;
        color: white;
        line-height: 1.2;
    }
    
    .cta-block h2 em {
        font-style: italic;
        opacity: 0.85;
    }
    
    .cta-block p {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.85);
        line-height: 1.55;
        margin: 0;
        max-width: 500px;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: #1A4D3F !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.85rem 1.75rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #0F3A2E !important;
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="primary"] {
        font-size: 0.95rem !important;
        padding: 1rem 2rem !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #1A4D3F !important;
        border: 1px solid #D4CEC0 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #F5F2EC !important;
    }
    
    /* TEXTAREA */
    .stTextArea textarea {
        background: white !important;
        border: 1px solid #D4CEC0 !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #1A1A1A !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #1A4D3F !important;
        box-shadow: 0 0 0 1px #1A4D3F !important;
    }
    

    /* RADIO - FIXED VISIBILITY */
    div[role="radiogroup"] {
        display: flex !important;
        gap: 0.75rem !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 1rem !important;
    }

    div[role="radiogroup"] > label {
        flex: 1 !important;
        background: white !important;
        border: 1.5px solid #D4CEC0 !important;
        border-radius: 6px !important;
        padding: 1rem 1.5rem !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.6rem !important;
    }

    div[role="radiogroup"] > label > div {
        color: #1A1A1A !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    div[role="radiogroup"] > label > div > p {
        color: #1A1A1A !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
        opacity: 1 !important;
    }

    div[role="radiogroup"] > label:hover {
        border-color: #1A4D3F !important;
        background: #F5F2EC !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] {
        border-color: #1A4D3F !important;
        background: #F0EDE5 !important;
        border-width: 2px !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] > div > p {
        color: #1A4D3F !important;
        font-weight: 600 !important;
    }
    
    /* FILE UPLOADER */
    [data-testid="stFileUploader"] {
        background: white;
        border: 1px dashed #D4CEC0;
        border-radius: 6px;
        padding: 1.5rem;
    }
    
    /* TRIAL CARD */
    .trial-card {
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 6px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .trial-card:hover {
        border-color: #1A4D3F;
    }
    
    .trial-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .trial-info-block {
        flex: 1;
    }
    
    .trial-id {
        font-size: 0.7rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .trial-name {
        font-size: 1rem;
        font-weight: 600;
        color: #1A1A1A;
        line-height: 1.4;
        margin-bottom: 0.5rem;
    }
    
    .trial-rationale {
        font-size: 0.85rem;
        color: #5A5A5A;
        line-height: 1.5;
        margin-top: 0.75rem;
    }
    
    .score-block {
        text-align: right;
        flex-shrink: 0;
        min-width: 100px;
    }
    
    .score-percent {
        font-family: 'Instrument Serif', serif;
        font-size: 2.5rem;
        line-height: 1;
    }
    
    .score-status {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.4rem;
    }
    
    .strong { color: #1A4D3F; }
    .moderate { color: #B8860B; }
    .weak { color: #888; }
    
    /* PROFILE BLOCKS */
    .profile-section {
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 6px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .profile-section h4 {
        font-family: 'Instrument Serif', serif;
        font-size: 1.3rem;
        color: #1A1A1A;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #F0EDE5;
    }
    
    .profile-line {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        font-size: 0.9rem;
        border-bottom: 1px solid #F5F2EC;
    }
    
    .profile-line:last-child {
        border-bottom: none;
    }
    
    .profile-line-key {
        color: #888;
    }
    
    .profile-line-val {
        color: #1A1A1A;
        font-weight: 500;
    }
    
    /* LOADING */
    .loading-card {
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 8px;
        padding: 4rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .loading-icon {
        font-family: 'Instrument Serif', serif;
        font-size: 3rem;
        color: #1A4D3F;
        margin-bottom: 1rem;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    
    .loading-title {
        font-family: 'Instrument Serif', serif;
        font-size: 1.5rem;
        color: #1A1A1A;
        margin-bottom: 0.5rem;
    }
    
    .loading-text {
        color: #5A5A5A;
        font-size: 0.9rem;
    }
    
    /* FOOTER */
    .site-footer {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid #E8E4DC;
        text-align: center;
        font-size: 0.85rem;
        color: #888;
    }
    
    .site-footer .made-by {
        font-family: 'Instrument Serif', serif;
        font-size: 1rem;
        color: #1A1A1A;
        margin-bottom: 0.5rem;
    }
            
    /* LINK BUTTONS - FIXED OVERLAP */
    .stLinkButton {
        margin-bottom: 0.5rem !important;
    }

    .stLinkButton > a {
        background: white !important;
        border: 1px solid #1A4D3F !important;
        color: #1A4D3F !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border-radius: 4px !important;
        padding: 0.6rem 1rem !important;
        text-align: center !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 42px !important;
        line-height: 1.2 !important;
    }

    .stLinkButton > a:hover {
        background: #1A4D3F !important;
        color: white !important;
    }

    /* Trial card spacing fix */
    .trial-card {
        margin-bottom: 1.5rem !important;
    }

    /* Add spacing after trial action buttons row */
    .element-container:has(.stLinkButton) {
        margin-bottom: 1rem !important;
    }

    /* Fix expander overlap */
    [data-testid="stExpander"] {
        margin-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# NAVBAR
st.markdown("""
<div class="navbar">
    <div class="logo-wrap">
        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <rect width="36" height="36" rx="4" fill="#1A4D3F"/>
            <path d="M18 9 L18 27 M9 18 L27 18" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="18" cy="18" r="3" fill="white"/>
        </svg>
        <div>
            <div class="logo-text">Clinical Trial Match</div>
            <div class="logo-tag">AI · Healthcare</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== PAGE 1: LANDING =====
if st.session_state.page == 'landing':
    
    # HERO - new headline
    st.markdown("""
    <div class="hero-grid">
        <div>
            <div class="hero-eyebrow">AI · Patient · Trial Matching</div>
            <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            Stop searching.<br>Start <em style="color: #1A4D3F; font-style: italic;">treating.</em>
            </h1>
            <p class="hero-desc">An intelligent platform that matches patients to active clinical trials in seconds — closing the gap between people who need treatment and the research that could save them.</p>
        </div>
        <div class="hero-visual">
            <div class="visual-label">Real-time access</div>
            <div class="visual-stat">400K+</div>
            <div class="visual-text">Active recruiting clinical trials, searchable in seconds with AI eligibility analysis.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # STATS BAR
    st.markdown("""
    <div class="stats-bar">
        <div class="stats-bar-item">
            <div class="sb-num">76%</div>
            <div class="sb-label">of trials fail enrollment targets</div>
        </div>
        <div class="stats-bar-item">
            <div class="sb-num">$100M+</div>
            <div class="sb-label">wasted annually on recruitment</div>
        </div>
        <div class="stats-bar-item">
            <div class="sb-num">2 min</div>
            <div class="sb-label">average match time vs. 6+ months</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # THE GAP
    st.markdown("""
    <div class="section">
        <div class="section-eyebrow">The opportunity</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            A solvable <br>multi-billion dollar <em style="color: #1A4D3F; font-style: italic;">problem.</em>
        </h1>
        <p class="section-text"><strong>The data exists. The matching logic is straightforward. The only thing missing is the connection.</strong> Clinical Trial Match closes that gap with AI that reads medical records the way a research coordinator would, then surfaces the right trials in seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # WHY IT MATTERS - 4 cards
    st.markdown("""
    <div class="section">
        <div class="section-eyebrow">Why it matters</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            The hidden cost of <br>broken <em style="color: #1A4D3F; font-style: italic;">matching.</em>
        </h1>
    </div>
    
    <div class="info-grid-4">
        <div class="info-card">
            <div class="info-card-num">$100M+</div>
            <div class="info-card-title">Burned each year</div>
            <div class="info-card-text">Failed enrollments cost pharma companies hundreds of millions in delays and write-offs.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">6 mo.</div>
            <div class="info-card-title">Lost in the search</div>
            <div class="info-card-text">Average time patients spend navigating fragmented databases without expert help.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">85%</div>
            <div class="info-card-title">Trials that stall</div>
            <div class="info-card-text">Most studies hit major enrollment delays, postponing patient access to new therapies.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">3%</div>
            <div class="info-card-title">Patients who know</div>
            <div class="info-card-text">Only a tiny fraction ever learn about trials they qualify for. The rest never enroll.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # HOW IT WORKS - rendered as components.html to avoid escaping
    st.markdown("""
    <div class="section">
        <div class="section-eyebrow">How it works</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            Three steps.<br>Two minutes. <em style="color: #1A4D3F; font-style: italic;">One match that matters.</em>
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Use components.html to render the flow cards properly
    components.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        body { margin: 0; padding: 0; background: #FAFAF7; }
        
        /* 1. Reduce space between all Streamlit elements */
        [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
        }

        /* 2. Target your specific custom classes to remove bottom margins */
        .hero-title, .section-title {
            margin-bottom: 0.2rem !important; /* Tighten gap to the text below */
        }

        .hero-eyebrow, .section-eyebrow {
            margin-bottom: 0rem !important;
        }

        /* 3. Remove default padding Streamlit adds to markdown blocks */
        .stMarkdown div p {
            margin-bottom: 0.5rem !important;
        }
                    
        .flow-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
        }
        
        .flow-card {
            background: white;
            border: 1px solid #E8E4DC;
            border-radius: 6px;
            padding: 1.75rem 1.5rem;
            position: relative;
            transition: all 0.2s;
        }
        
        .flow-card:hover {
            border-color: #1A4D3F;
            transform: translateY(-2px);
        }
        
        .flow-num {
            position: absolute;
            top: 1rem;
            right: 1.5rem;
            font-family: 'Instrument Serif', serif;
            font-size: 3rem;
            color: #E8E4DC;
            line-height: 1;
        }
        
        .flow-icon {
            width: 40px;
            height: 40px;
            background: #1A4D3F;
            border-radius: 6px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .flow-card h4 {
            font-size: 1.05rem;
            font-weight: 600;
            color: #1A1A1A;
            margin: 0 0 0.5rem 0;
            line-height: 1.3;
        }
        
        .flow-card p {
            font-size: 0.85rem;
            color: #5A5A5A;
            line-height: 1.55;
            margin: 0;
        }
    </style>
    
    <div class="flow-grid">
        <div class="flow-card">
            <div class="flow-num">01</div>
            <div class="flow-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="white" stroke-width="2"/>
                    <polyline points="14 2 14 8 20 8" stroke="white" stroke-width="2" fill="none"/>
                </svg>
            </div>
            <h4>Drop in the patient data</h4>
            <p>Type clinical info or upload medical records. The AI reads unstructured notes, EMR exports, and PDFs.</p>
        </div>
        
        <div class="flow-card">
            <div class="flow-num">02</div>
            <div class="flow-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
                    <path d="M12 6v6l4 2" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
            <h4>Let the AI do the reading</h4>
            <p>Medical NLP extracts diagnoses, demographics, and meds — then queries 400K+ trials in real-time.</p>
        </div>
        
        <div class="flow-card">
            <div class="flow-num">03</div>
            <div class="flow-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <polyline points="20 6 9 17 4 12" stroke="white" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                </svg>
            </div>
            <h4>Review the matches that fit</h4>
            <p>Each trial gets an eligibility score with rationale. Direct links to study protocols and coordinators.</p>
        </div>
    </div>
    """, height=240)
    
    # AFTER MATCH
    st.markdown("""
    <div class="section">
        <div class="section-eyebrow">After the match</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            From <br>discovery <em style="color: #1A4D3F; font-style: italic;">to enrollment.</em>
        </h1>
        <p class="section-text">Finding a trial is just the first step. Here's the path forward — clear, structured, and grounded in the real-world process of getting into a study.</p>
    </div>
    
    <div class="info-grid-4">
        <div class="info-card">
            <div class="info-card-num">①</div>
            <div class="info-card-title">Read the protocol</div>
            <div class="info-card-text">Click through to the official ClinicalTrials.gov listing for full eligibility criteria and study details.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">②</div>
            <div class="info-card-title">Reach the team</div>
            <div class="info-card-text">Each listing has direct contacts for study coordinators. Get in touch to confirm fit.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">③</div>
            <div class="info-card-title">Talk to your doctor</div>
            <div class="info-card-text">Trial enrollment requires medical oversight. Bring the protocol to your next visit.</div>
        </div>
        <div class="info-card">
            <div class="info-card-num">④</div>
            <div class="info-card-title">Complete screening</div>
            <div class="info-card-text">Most trials require an in-person screening visit before final enrollment is confirmed.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div class="cta-block">
        <h2>Find a trial in <em>two minutes</em>.</h2>
        <p>Enter patient information and let AI surface the most relevant active trials in seconds. No more six-month searches.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("→ Start Trial Search", type="primary", use_container_width=True):
            st.session_state.page = 'input'
            st.rerun()


# ===== PAGE 2: INPUT =====
elif st.session_state.page == 'input':
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to home", type="secondary"):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown("""
    <div class="section" style="margin-top: 2rem;">
        <div class="section-eyebrow">Patient data</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            Tell us <br>who <em style="color: #1A4D3F; font-style: italic;">we're looking for.</em>
        </h1>
        <p class="section-text">The more specific the input, the sharper the match. Include diagnoses, current medications, age, and location for the most accurate trial recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_method = st.radio(
        "Input method:",
        ["Type Manually", "Upload Document"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    patient_info = ""
    
    if input_method == "Type Manually":
        patient_info = st.text_area(
            "Patient data:",
            value=st.session_state.patient_info,
            placeholder="Age: 52\nGender: Male\nLocation: Philadelphia, PA\n\nDiagnoses:\n- Type 2 Diabetes Mellitus\n- Essential Hypertension\n\nMedications:\n- Metformin 1000mg BID\n- Lisinopril 10mg QD",
            height=280,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Load sample"):
                st.session_state.patient_info = """Age: 52
Gender: Male
Location: Philadelphia, PA

Diagnoses:
- Type 2 Diabetes Mellitus (HbA1c 8.9%)
- Obesity (BMI 34.2)
- Essential Hypertension

Medications:
- Metformin 1000mg BID
- Insulin Glargine 20 units QHS
- Lisinopril 10mg QD"""
                st.rerun()
    
    else:
        uploaded_file = st.file_uploader(
            "Upload PDF or TXT document",
            type=['pdf', 'txt'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    from PyPDF2 import PdfReader
                    pdf = PdfReader(uploaded_file)
                    patient_info = "\n".join([p.extract_text() for p in pdf.pages])
                else:
                    patient_info = uploaded_file.read().decode('utf-8')
                st.success(f"✓ Loaded {len(patient_info)} characters from {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("→ Find Matching Trials", type="primary", use_container_width=True):
            if patient_info.strip():
                st.session_state.patient_info = patient_info
                st.session_state.extracted_data = None
                st.session_state.studies = None
                st.session_state.page = 'results'
                st.rerun()
            else:
                st.error("Please provide patient information")


# ===== PAGE 3: RESULTS =====
elif st.session_state.page == 'results':
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← New search", type="secondary"):
            st.session_state.page = 'input'
            st.session_state.extracted_data = None
            st.session_state.studies = None
            st.rerun()
    
    if st.session_state.extracted_data is None:
        st.markdown("""
        <div class="loading-card">
            <div class="loading-icon">✛</div>
            <div class="loading-title">Reading the chart</div>
            <div class="loading-text">Extracting clinical entities and querying<br>the ClinicalTrials.gov registry...</div>
        </div>
        """, unsafe_allow_html=True)
        
        prompt = f"""Extract from this patient record. Return ONLY valid JSON:

{st.session_state.patient_info}

Format:
{{
    "age": "number or 'not specified'",
    "gender": "Male/Female/Other or 'not specified'",
    "location": "city, state or 'not specified'",
    "conditions": ["diagnosis 1"],
    "medications": ["med 1"]
}}"""
        
        try:
            resp = model.generate_content(prompt)
            text = resp.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            st.session_state.extracted_data = json.loads(text.strip())
        except Exception as e:
            st.error(f"Extraction error: {e}")
            st.stop()
        
        conds = st.session_state.extracted_data.get('conditions', [])
        if conds:
            params = {
                "query.cond": " OR ".join(conds),
                "filter.overallStatus": "RECRUITING",
                "pageSize": 10,
                "format": "json"
            }
            
            loc = st.session_state.extracted_data.get('location', '')
            if 'philadelphia' in loc.lower() or 'PA' in loc:
                params["filter.geo"] = "distance(39.9526,-75.1652,100mi)"
            
            try:
                r = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params, timeout=15)
                st.session_state.studies = r.json().get('studies', [])
            except Exception as e:
                st.error(f"Search error: {e}")
                st.session_state.studies = []
        
        st.rerun()
    
    data = st.session_state.extracted_data
    studies = st.session_state.studies
    
    st.markdown("""
    <div class="section" style="margin-top: 1.5rem;">
        <div class="section-eyebrow">Patient profile</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            Let's see <br>What the AI <em style="color: #1A4D3F; font-style: italic;">found.</em>
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="profile-section">
            <h4>Demographics</h4>
            <div class="profile-line">
                <span class="profile-line-key">Age</span>
                <span class="profile-line-val">{data.get('age', 'N/A')}</span>
            </div>
            <div class="profile-line">
                <span class="profile-line-key">Gender</span>
                <span class="profile-line-val">{data.get('gender', 'N/A')}</span>
            </div>
            <div class="profile-line">
                <span class="profile-line-key">Location</span>
                <span class="profile-line-val">{data.get('location', 'N/A')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        conds = data.get('conditions', [])
        meds = data.get('medications', [])
        cond_html = "".join([f'<div class="profile-line"><span class="profile-line-val">{c}</span></div>' for c in conds])
        med_html = "".join([f'<div class="profile-line"><span class="profile-line-val">{m}</span></div>' for m in meds])
        
        st.markdown(f"""
        <div class="profile-section">
            <h4>Clinical summary</h4>
            <div style="font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; font-weight: 600;">Diagnoses</div>
            {cond_html}
            <div style="font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; margin: 1rem 0 0.5rem 0; font-weight: 600;">Medications</div>
            {med_html}
        </div>
        """, unsafe_allow_html=True)
    
    show_count = min(10, len(studies)) if studies else 0
    
    st.markdown(f"""
    <div class="section">
        <div class="section-eyebrow">Matched trials</div>
        <h1 style="font-family: 'Instrument Serif', serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 1rem; color: #1A1A1A;">
            Your <br>best <em style="color: #1A4D3F; font-style: italic;">fits.</em>
        </h1>
        <p class="section-text">Found <strong>{len(studies) if studies else 0}</strong> active recruiting trials matching the patient's profile. Each one analyzed individually for eligibility fit.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not studies:
        st.warning("No matching trials found.")
    else:
        for idx, study in enumerate(studies[:10], 1):
            p = study.get('protocolSection', {})
            ident = p.get('identificationModule', {})
            desc = p.get('descriptionModule', {})
            elig = p.get('eligibilityModule', {})
            
            title = ident.get('officialTitle', ident.get('briefTitle', 'No title'))
            nct = ident.get('nctId', 'N/A')
            summ = desc.get('briefSummary', 'N/A')
            crit = elig.get('eligibilityCriteria', 'N/A')
            
            match_prompt = f"""Analyze patient-trial match:

Patient: {data.get('age')}yo {data.get('gender')}, conditions: {', '.join(data.get('conditions', []))}

Trial: {title}
Summary: {summ[:300]}
Criteria: {crit[:400]}

Return ONLY:
SCORE: [0-100]
RATIONALE: [1-2 sentences explaining the match]"""
            
            with st.spinner(f"Analyzing trial {idx} of {show_count}..."):
                try:
                    m_resp = model.generate_content(match_prompt)
                    analysis = m_resp.text
                    score_line = [l for l in analysis.split('\n') if 'SCORE' in l.upper()][0]
                    score = int(''.join(filter(str.isdigit, score_line.split(':')[-1])))
                    
                    if 'RATIONALE' in analysis.upper():
                        rationale = analysis.split('RATIONALE:')[-1].strip()
                    else:
                        rationale = analysis
                except:
                    rationale = "Analysis unavailable"
                    score = 0
            
            if score >= 70:
                score_class = "strong"
                score_text = "Strong match"
            elif score >= 50:
                score_class = "moderate"
                score_text = "Moderate match"
            else:
                score_class = "weak"
                score_text = "Weak match"
            
            st.markdown(f"""
            <div class="trial-card">
                <div class="trial-header">
                    <div class="trial-info-block">
                        <div class="trial-id">Trial {idx:02d} · {nct}</div>
                        <div class="trial-name">{title[:160]}{'...' if len(title) > 160 else ''}</div>
                        <div class="trial-rationale">{rationale[:280]}{'...' if len(rationale) > 280 else ''}</div>
                    </div>
                    <div class="score-block">
                        <div class="score-percent {score_class}">{score}%</div>
                        <div class="score-status {score_class}">{score_text}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.link_button(
                    "→ View on ClinicalTrials.gov",
                    f"https://clinicaltrials.gov/study/{nct}",
                    use_container_width=True
                )
            with col2:
                st.link_button(
                    "→ Contact Coordinators",
                    f"https://clinicaltrials.gov/study/{nct}#contacts",
                    use_container_width=True
                )
            with col3:
                with st.expander("Details"):
                    st.write(f"**Summary:** {summ[:400]}...")
                    st.write(f"**Eligibility:** {crit[:300]}...")


# FOOTER
st.markdown("""
<div class="site-footer">
    <div class="made-by">Made by <em>Pramita</em> · April 2026</div>
    <p>Powered by Google Gemini & ClinicalTrials.gov · For research purposes only</p>
</div>
""", unsafe_allow_html=True)