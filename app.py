import time
import streamlit as st


# ----------------------------
# Page settings
# ----------------------------
st.set_page_config(
    page_title="Monofer Dose Calculator",
    page_icon="💉",
    layout="centered",
)


# ----------------------------
# Custom CSS (Pharma look + colors + loader)
# ----------------------------
st.markdown(
    """
    <style>
      /* Background */
      .stApp {
        background: radial-gradient(circle at 20% 10%, rgba(75, 156, 221, 0.18), transparent 35%),
                    radial-gradient(circle at 85% 35%, rgba(134, 206, 245, 0.22), transparent 40%),
                    linear-gradient(180deg, #F6FAFF 0%, #FFFFFF 55%, #F6FAFF 100%);
      }

      /* Reduce top padding */
      .block-container { padding-top: 1.1rem; padding-bottom: 2.5rem; max-width: 720px; }

      /* Pharma card */
      .card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 16px 16px 12px 16px;
        box-shadow: 0 14px 32px rgba(2, 8, 23, 0.10);
        margin-bottom: 14px;
        backdrop-filter: blur(6px);
      }

      /* Header */
      .header-card{
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15, 23, 42, 0.06);
        border-radius: 18px;
        padding: 14px 16px;
        box-shadow: 0 14px 32px rgba(2, 8, 23, 0.10);
        margin-bottom: 14px;
      }
      .header-wrap{
        display:flex;
        align-items:center;
        gap:14px;
      }
      .brand-title{
        font-size: 30px;
        font-weight: 850;
        color: #0F172A;
        line-height: 1.1;
        margin:0;
      }
      .brand-subtitle{
        font-size: 13px;
        color: rgba(15, 23, 42, 0.62);
        margin-top: 3px;
        margin-bottom: 0;
      }

      /* Section title */
      .section-title{
        font-size: 16px;
        font-weight: 750;
        color: #0F172A;
        margin: 0 0 10px 0;
        display:flex;
        gap:8px;
        align-items:center;
      }
      .pill{
        display:inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        background: rgba(59,130,246,0.10);
        border: 1px solid rgba(59,130,246,0.18);
        color: rgba(15,23,42,0.75);
        font-size: 12px;
        font-weight: 650;
      }

      /* Results */
      .result-grid{
        display:grid;
        grid-template-columns: 1fr;
        gap:10px;
        margin-top: 4px;
      }
      .result-item{
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.18);
      }
      .result-label{
        font-size: 12px;
        color: rgba(15, 23, 42, 0.70);
        margin:0;
      }
      .result-value{
        font-size: 22px;
        font-weight: 850;
        color: #0F172A;
        margin: 2px 0 0 0;
      }

      /* Footer note */
      .note{
        font-size: 12px;
        color: rgba(15, 23, 42, 0.55);
        margin-top: 10px;
      }

      /* Small loader (animation) */
      .loader-wrap{ display:flex; align-items:center; gap:10px; margin: 6px 0 6px 0; }
      .dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: rgba(59,130,246,0.75);
        animation: bounce 1.1s infinite ease-in-out;
      }
      .dot:nth-child(2){ animation-delay: 0.15s; opacity: 0.8; }
      .dot:nth-child(3){ animation-delay: 0.30s; opacity: 0.65; }
      @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-7px); }
      }
      .loading-text{ font-size: 12px; color: rgba(15,23,42,0.55); }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Header with logo beside title (small)
# ----------------------------
st.markdown('<div class="header-card">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    # Logo file must be in repo root with this exact name:
    # monofer_logo.png.jpg
    st.image("monofer_logo.png.jpg", width=56)

with col2:
    st.markdown(
        """
        <div class="header-wrap">
          <div>
            <p class="brand-title">Monofer Dose Calculator</p>
            <p class="brand-subtitle">IV Iron dosing support • simple & fast</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Inputs
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧾 Patient Inputs <span class="pill">Quick Entry</span></div>', unsafe_allow_html=True)

weight = st.number_input(
    "Body weight (kg)",
    min_value=30.0,
    max_value=250.0,
    value=70.0,
    step=0.5
)

hb_category = st.radio(
    "Hemoglobin Category",
    ["Hb < 10 g/dL", "Hb ≥ 10 g/dL"],
    horizontal=False
)

st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Calculation (same logic you used)
# ----------------------------
def total_iron(weight_kg: float, hb_cat: str) -> int:
    if hb_cat == "Hb ≥ 10 g/dL":
        return 1000 if weight_kg < 70 else 1500
    else:
        return 1500 if weight_kg < 70 else 2000


# Loading animation (pharma feel)
st.markdown(
    """
    <div class="loader-wrap">
      <div class="dot"></div><div class="dot"></div><div class="dot"></div>
      <div class="loading-text">Calculating dose…</div>
    </div>
    """,
    unsafe_allow_html=True,
)
time.sleep(0.35)

total = total_iron(weight, hb_category)
first_dose = min(weight * 20, total)   # 20 mg/kg, max total
second_dose = total - first_dose


# ----------------------------
# Results
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Results <span class="pill">mg</span></div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="result-grid">
      <div class="result-item">
        <p class="result-label">Total Iron Need</p>
        <p class="result-value">{int(total)} mg</p>
      </div>
      <div class="result-item">
        <p class="result-label">First Dose</p>
        <p class="result-value">{first_dose:.1f} mg</p>
      </div>
      <div class="result-item">
        <p class="result-label">Second Dose</p>
        <p class="result-value">{second_dose:.1f} mg</p>
      </div>
    </div>
    <div class="note">
      Note: Validate dosing with local protocol / prescribing information.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
