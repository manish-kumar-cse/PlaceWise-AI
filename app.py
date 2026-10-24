import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="PlaceWise AI | Placement Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

model = joblib.load("placement_model.pkl")
features = joblib.load("placement_features.pkl")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #111a30 55%, #101426 100%);
    color: #f1f5f9;
}

.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    padding: 32px;
    border-radius: 24px;
    background: linear-gradient(120deg, #182b4a, #20204a 65%, #292052);
    border: 1px solid #344567;
    margin-bottom: 26px;
}

.eyebrow {
    color: #8fe3d0;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 47px);
    font-weight: 800;
    line-height: 1.15;
    margin: 12px 0;
    color: #ffffff;
}

.hero p {
    color: #c0cbe0;
    font-size: 15px;
    margin-bottom: 0;
}

.section-title {
    font-size: 21px;
    font-weight: 750;
    color: #f8fafc;
    margin: 12px 0 4px;
}

.section-subtitle {
    color: #9baac3;
    font-size: 13px;
    margin-bottom: 20px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #2b3a55;
    border-radius: 18px;
    background: rgba(21, 31, 52, 0.76);
}

label, .stMarkdown, p {
    color: #e2e8f0;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: #172238;
    border-color: #354661;
    border-radius: 10px;
}

.stSlider [data-baseweb="slider"] {
    padding-top: 5px;
}

.stButton > button,
.stFormSubmitButton > button {
    width: 100%;
    min-height: 49px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(100deg, #14b8a6, #6366f1);
    color: white;
    font-weight: 750;
    font-size: 16px;
    transition: 0.2s ease;
}

.stFormSubmitButton > button:hover {
    border: none;
    color: white;
    filter: brightness(1.12);
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: #17243b;
    border: 1px solid #344765;
    border-radius: 14px;
    padding: 18px;
}

div[data-testid="stMetricLabel"] {
    color: #aabbd3;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
}

.result-card {
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #344765;
    background: linear-gradient(135deg, #17243b, #202747);
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #8292ad;
    font-size: 12px;
    padding-top: 28px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ AI-Powered Career Insights</div>
    <h1>Find Your Path to<br>Placement Success.</h1>
    <p>PlaceWise AI analyzes student academic performance, skills and preparation
    to estimate placement outcomes.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">🎯 Student Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Enter your details below to generate a personalized prediction.</div>', unsafe_allow_html=True)

with st.form("placement_form"):
    st.markdown("#### 📚 Academic Performance")

    c1, c2 = st.columns(2)

    with c1:
        cgpa = st.slider("CGPA", 0.0, 10.0, 8.0, 0.1)
        ssc = st.slider("SSC Marks (%)", 0, 100, 85)
        hsc = st.slider("HSC Marks (%)", 0, 100, 80)

    with c2:
        aptitude = st.slider("Aptitude Test Score", 0, 100, 80)
        soft_skills = st.slider("Soft Skills Rating", 0.0, 5.0, 4.0, 0.1)

    st.divider()
    st.markdown("#### 💼 Experience & Preparation")

    c3, c4 = st.columns(2)

    with c3:
        internships = st.number_input("Internships Completed", 0, 10, 2)
        projects = st.number_input("Projects Completed", 0, 20, 3)
        workshops = st.number_input("Workshops / Certifications", 0, 20, 2)

    with c4:
        extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"])
        training = st.selectbox("Placement Training", ["Yes", "No"])

    st.markdown("")
    submitted = st.form_submit_button("✨  Predict My Placement", use_container_width=True)

if submitted:
    student = pd.DataFrame([{
        "CGPA": cgpa,
        "Internships": internships,
        "Projects": projects,
        "Workshops/Certifications": workshops,
        "AptitudeTestScore": aptitude,
        "SoftSkillsRating": soft_skills,
        "ExtracurricularActivities": 1 if extracurricular == "Yes" else 0,
        "PlacementTraining": 1 if training == "Yes" else 0,
        "SSC_Marks": ssc,
        "HSC_Marks": hsc
    }], columns=features)

    prediction = model.predict(student)[0]
    probabilities = model.predict_proba(student)[0]
    placed_probability = float(probabilities[1]) * 100
    not_placed_probability = float(probabilities[0]) * 100

    st.markdown('<div class="section-title">📊 Your Prediction</div>', unsafe_allow_html=True)

    if prediction == 1:
        st.success("🎉 Model prediction: Placed")
    else:
        st.warning("Model prediction: Not Placed")

    m1, m2 = st.columns(2)

    with m1:
        st.metric("Estimated Placement Probability", f"{placed_probability:.1f}%")

    with m2:
        st.metric("Estimated Non-Placement Probability", f"{not_placed_probability:.1f}%")

    st.markdown("**Placement Probability**")
    st.progress(int(round(placed_probability)))
    st.caption("These probabilities are model estimates, not guarantees of actual placement.")

    st.markdown("**Profile Summary**")
    st.write(
        f"CGPA: **{cgpa:.1f}** · Aptitude: **{aptitude}/100** · "
        f"Internships: **{internships}** · Projects: **{projects}**"
    )

st.markdown("""
<div class="footer">
    PLACEWISE AI · STUDENT PLACEMENT PREDICTION<br>
    Built with Streamlit & Machine Learning · For educational purposes
</div>
""", unsafe_allow_html=True)

st.divider()

st.header("🎓 Chandigarh University Placement Statistics")
st.caption("Officially reported figures • Batch 2024–25")

col1, col2 = st.columns(2)

with col1:
    st.metric("Placement Offers", "10,000+")

with col2:
    st.metric("Companies Visited", "1,300+")

col3, col4 = st.columns(2)

with col3:
    st.metric("Highest National Package", "₹59.9 LPA")

with col4:
    st.metric("Highest International Package", "₹1.7 Crore")

st.caption(
    "Source: Chandigarh University official placement website"
)

st.markdown(
    "[View Official Placement Details](https://www.cuchd.in/placements/)"
)
