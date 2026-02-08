import streamlit as st

# ----------------------------
# Page settings
# ----------------------------
st.set_page_config(
    page_title="Monofer Dose Calculator",
    page_icon="💉",
    layout="centered",
)
col1, col2 = st.columns([1,5])

with col1:
    st.image("monofer_logo.png", width=80)

with col2:
    st.title("Monofer Dose Calculator")
st.image("monofer_logo.png.jpg", width=180)

# ----------------------------
# Custom CSS (design only)
# ----------------------------
st.markdown(
    """
    <style>
      /* App background */
      .stApp {
        background: linear-gradient(180deg, #F6FAFF 0%, #FFFFFF 50%, #F6FAFF 100%);
      }

      /* Remove extra top padding */
      .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }

      /* Card style */
      .card {
        background: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 10px 25px rgba(2, 8, 23, 0.06);
        margin-bottom: 14px;
      }

      /* Header row */
      .header-wrap{
        display:flex;
        align-items:center;
        gap:14px;
        margin-bottom:10px;
      }
      .brand-title{
        font-size: 34px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin:0;
      }
      .brand-subtitle{
        font-size: 14px;
        color: rgba(15, 23, 42, 0.65);
        margin-top: 2px;
      }

      /* Section titles */
      .section-title{
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin: 0 0 10px 0;
      }

      /* Result styles */
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
        font-size: 13px;
        color: rgba(15, 23, 42, 0.70);
        margin:0;
      }
      .result-value{
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        margin: 2px 0 0 0;
      }

      /* Small footer note */
      .note{
        font-size: 12px;
        color: rgba(15, 23, 42, 0.55);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Header with logo
# ----------------------------
col_logo, col_text = st.columns([1, 5], vertical_alignment="center")

with col_logo:
    # Put monofer_logo.png in the repo root
    try:
        st.image("monofer_logo.png", width=70)
    except Exception:
        # If logo isn't uploaded yet, app still works
        st.write("")

with col_text:
    st.markdown(
        """
        <div class="header-wrap">
          <div>
            <p class="brand-title">Monofer Dose Calculator</p>
            <div class="brand-subtitle">IV Iron dosing support • simple & fast</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------
# Inputs (same logic)
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Patient Inputs</p>', unsafe_allow_html=True)

weight = st.number_input("Body weight (kg)", min_value=50.0, max_value=250.0, value=70.0, step=0.5)

hb_category = st.radio(
    "Hemoglobin Category",
    ["Hb < 10 g/dL", "Hb ≥ 10 g/dL"],
    horizontal=False
)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Calculation (same as yours)
# ----------------------------
def total_iron(weight, hb_category):
    if hb_category == "Hb ≥ 10 g/dL":
        return 1000 if weight < 70 else 1500
    else:
        return 1500 if weight < 70 else 2000

total = total_iron(weight, hb_category)
first_dose = min(weight * 20, total)
second_dose = total - first_dose

# ----------------------------
# Results (styled)
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Results</p>', unsafe_allow_html=True)

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
    <br/>
    <div class="note">Note: Design preview only. Validate dosing with local protocol / prescribing information.</div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
