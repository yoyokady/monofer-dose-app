import streamlit as st

st.title("Monofer Dose Calculator")

weight = st.number_input("Body weight (kg)", min_value=50.0, max_value=250.0, value=70.0)

hb_category = st.radio(
    "Hemoglobin Category",
    ["Hb < 10 g/dL", "Hb ≥ 10 g/dL"]
)

def total_iron(weight, hb_category):
    if hb_category == "Hb ≥ 10 g/dL":
        return 1000 if weight < 70 else 1500
    else:
        return 1500 if weight < 70 else 2000

total = total_iron(weight, hb_category)

first_dose = min(weight * 20, total)
second_dose = total - first_dose

st.write("### Results")
st.write(f"Total Iron Need: {total} mg")
st.write(f"First Dose: {first_dose:.1f} mg")
st.write(f"Second Dose: {second_dose:.1f} mg")
