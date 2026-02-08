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
# Pharma UI CSS + small loader
# ----------------------------
st.markdown(
    """
    <style>
      /* App background */
      .stApp {
        background: linear-gradient(180deg, #F3F8FF 0%, #FFFFFF 55%, #F3F8FF 100%);
      }

      /* Page spacing */
      .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; max-width: 720px; }

      /* Card */
      .card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 14px 32px rgba(2, 8, 23, 0.08);
        margin-bottom: 14px;
        backdrop-filter: blur(6px);
      }

      /* Header */
      .header-row { display:flex; align-items:center; gap:14px; }
      .brand-title{
        font-size: 34px; font-weight: 900; color:#0F172A;
        margin:0; line-height: 1.05;
      }
      .brand-subtitle{
        font-size: 14px; color: rgba(15,23,42,0.65);
        margin-top: 4px;
      }

      /* Section title */
      .section-title{
        font-size: 18px; font-weight: 800; color:#0F172A;
        margin: 0 0 10px 0;
        display:flex; align-items:center; gap:10px;
      }
      .badge{
        display:inline-flex;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(0, 122, 255, 0.10);
        border: 1px solid rgba(0, 122, 255, 0.18);
        color: rgba(15,23,42,0.75);
      }

      /* Result blocks */
      .result-grid{ display:grid; grid-template-columns: 1fr; gap:10px; margin-top: 6px; }
      .result-item{
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(0, 122, 255, 0.08);
        border: 1px solid rgba(0, 122, 255, 0.18);
        display:flex; align-items:center; justify-content:space-between;
      }
      .result-left{ display:flex; align-items:center; gap:10px; }
      .chip{
        width: 24px; height: 24px;
        border-radius: 8px;
        background: rgba(0, 122, 255, 0.18);
        display:flex; align-items:center; justify-content:center;
        font-weight: 900;
        color: rgba(15,23,42,0.75);
      }
      .result-label{ font-size: 14px; color: rgba(15,23,42,0.78); margin:0; font-weight: 700; }
      .result-value{ font-size: 22px; font-weight: 900; color:#0F172A; margin:0; }

      /* Note */
      .note{
        font-size: 12px;
        color: rgba(15,23,42,0.55);
        margin-top: 10px;
      }

      /* Optional tiny top loader bar */
      .top-loader {
        height: 4px;
        width: 100%;
        border-radius: 999px;
        background: rgba(0, 122, 255, 0.10);
        overflow: hidden;
        margin-bottom: 12px;
      }
      .top-loader > div {
        height: 100%;
        width: 35%;
        background: rgba(0, 122, 255, 0.55);
        border-radius: 999px;
        animation: slide 1.2s infinite ease-in-out;
      }
      @keyframes slide {
        0% { transform: translateX(-60%); }
        50% { transform: translateX(180%); }
        100% { transform: translateX(-60%); }
      }

      /* Make Streamlit button look more "pharma" */
      div.stButton > button {
        width: 100%;
        border-radius: 14px;
        padding: 10px 14px;
        font-weight: 800;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Header card with logo beside title
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col_logo, col_text = st.columns([1, 6], vertical_alignment="center")

with col_logo:
    # IMPORTANT: exact filename + exact capitalization
    try:
        st.image("Monofer_logo.png.jpg", width=55)
    except Exception:
        st.write("")

with col_text:
    st.markdown(
        """
        <div class="header-row">
          <div>
            <p class="brand-title">Monofer Dose Calculator</p>
            <div class="brand-subtitle">IV Iron dosing support • simple & fast</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Inputs card
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Patient Inputs <span class="badge">Clinical tool</span></div>', unsafe_allow_html=True)

weight = st.number_input(
    "Body weight (kg)",
    min_value=50.0,
    max_value=250.0,
    value=70.0,
    step=0.5
)

hb_category = st.radio(
    "Hemoglobin Category",
    ["Hb < 10 g/dL", "Hb ≥ 10 g/dL"],
    horizontal=False
)

calculate = st.button("Calculate dose")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Calculation logic (same as yours)
# ----------------------------
def total_iron(weight_val: float, hb_cat: str) -> int:
    if hb_cat == "Hb ≥ 10 g/dL":
        return 1000 if weight_val < 70 else 1500
    return 1500 if weight_val < 70 else 2000

# Keep results stable between reruns
if "results" not in st.session_state:
    st.session_state.results = None

if calculate:
    # Loading animation (spinner + top moving bar)
    st.markdown('<div class="top-loader"><div></div></div>', unsafe_allow_html=True)
    with st.spinner("Calculating…"):
        time.sleep(0.6)

    total = total_iron(weight, hb_category)
    first_dose = min(weight * 20, total)
    second_dose = total - first_dose

    st.session_state.results = (total, first_dose, second_dose)

# ----------------------------
# Results card
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Results <span class="badge">mg</span></div>', unsafe_allow_html=True)

if st.session_state.results is None:
    st.info("Enter patient details and press **Calculate dose**.")
else:
    total, first_dose, second_dose = st.session_state.results

    st.markdown(
        f"""
        <div class="result-grid">
          <div class="result-item">
            <div class="result-left">
              <div class="chip">Σ</div>
              <p class="result-label">Total Iron Need</p>
            </div>
            <p class="result-value">{int(total)} <span style="font-size:16px;font-weight:800;color:rgba(15,23,42,0.70)">mg</span></p>
          </div>

          <div class="result-item">
            <div class="result-left">
              <div class="chip">1</div>
              <p class="result-label">First Dose</p>
            </div>
            <p class="result-value">{first_dose:.1f} <span style="font-size:16px;font-weight:800;color:rgba(15,23,42,0.70)">mg</span></p>
          </div>

          <div class="result-item">
            <div class="result-left">
              <div class="chip">2</div>
              <p class="result-label">Second Dose</p>
            </div>
            <p class="result-value">{second_dose:.1f} <span style="font-size:16px;font-weight:800;color:rgba(15,23,42,0.70)">mg</span></p>
          </div>
        </div>

        <div class="note">
          Note: Validate dosing with local protocol / prescribing information.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)
