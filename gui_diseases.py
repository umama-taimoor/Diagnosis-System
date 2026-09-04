import streamlit as st
from pyswip import Prolog

prolog = Prolog()
prolog.consult(r"D:\FAST_NUCES\5th_Semester\Knowledge_Representation_and_Reasoning\Prolog_diagnosis\disease.pl")

#Diseases with hierarchy priority
disease_priority = {
    "chronic_sinusitis": 1,
    "acute_sinusitis": 2,
    "deviated_nasal_septum": 3,
    "rhinitis": 4
}
diseases = list(disease_priority.keys())

#All symptoms
all_symptoms = [
    "facial_pain","nasal_congestion","thick_yellow_green_discharge",
    "fever","reduced_smell","sneezing","runny_clear_discharge",
    "itchy_eyes","itchy_nose","seasonal_or_triggered_by_allergens",
    "nasal_blockage","persistent_facial_pressure","postnasal_drip",
    "loss_of_smell","fatigue","symptoms_longer_than_12_weeks",
    "nasal_obstruction_one_side","recurrent_sinus_infections",
    "frequent_nosebleeds","noisy_breathing_during_sleep","headache"
]

st.title("Diagnosis Tool")

#session states for name and age
if "name" not in st.session_state:
    st.session_state.name = ""
if "age" not in st.session_state:
    st.session_state.age = 0

name = st.text_input("Enter your Name", value=st.session_state.name, key="name")
age = st.number_input("Enter your Age", min_value=0, max_value=100, step=1, key="age")

st.write("Select the symptoms you have:")

#session states becz of the checkboxes
for s in all_symptoms:
    if s not in st.session_state:
        st.session_state[s] = False

#used to un-check every checkbox
def reset_all():
    st.session_state.name = ""
    st.session_state.age = 0
    for s in all_symptoms:
        st.session_state[s] = False

#symptoms and they are mapped to their keys
for i in range(0,len(all_symptoms),3):
    cols = st.columns(3)
    for j in range(3):
        idx = i+j
        if idx<len(all_symptoms):
            symptom = all_symptoms[idx]
            with cols[j]:
                st.checkbox(symptom.replace("_"," "), key=symptom)

#buttons , 1 for diagnose,2 for reset
col1,col2 = st.columns([1,1])
with col1:
    diagnose_btn = st.button("Diagnose")
with col2:
    st.button("Reset", on_click=reset_all)

#list of selected checkboxes = symptoms
selected_symptoms = [s for s in all_symptoms if st.session_state.get(s)]

#diagnosis logic
if diagnose_btn:
    if not selected_symptoms:
        st.success("✅ You are perfectly healthy!")
    else:
        list(prolog.query("retractall(symptom(_))"))
        for s in selected_symptoms:
            prolog.assertz(f"symptom({s})")

        results = []
        for d in diseases:
            disease_symptoms = list(prolog.query(f"disease_symptom({d}, S)"))
            total = len(disease_symptoms)
            matched = list(prolog.query(f"matched_symptom({d}, S)"))
            count = len(matched)
            percent = round((count/total)*100,1) if total>0 else 0
            results.append((d,count,total,percent))

        #simple sort-key
        def sort_key(result):
            disease,count,total,percent = result
            return (percent,-disease_priority[disease])

        results.sort(key=sort_key, reverse=True)

        #basically the top = diagnosed
        best = results[0]
        st.subheader("Final Diagnosis")
        st.markdown(
            f"""
            <div style="padding:15px; margin:10px 0; border-radius:12px;
            border:2px solid #1976d2; background:#e3f2fd;">
            <h4 style="margin:0; color:#0d47a1;">Patient: {name if name else "Unknown"}, Age: {age}</h4>
            <h3 style="margin:5px 0; color:#0d47a1;">{best[0].replace('_',' ').title()}</h3>
            <p style="margin:0; color:#000;"><b>Confidence:</b> {best[3]}% 
            ({best[1]}/{best[2]} symptoms matched)</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        #details about the whole diagnosis
        st.subheader("Full Results")
        for d,c,t,p in results:
            st.markdown(
                f"""
                <div style="padding:10px; margin:6px 0; border-radius:8px; border:1px solid #ccc;">
                    <b>Disease:</b> {d.replace('_',' ').title()}<br>
                    <b>Confidence:</b> {p}% ({c}/{t} symptoms matched)
                </div>
                """,
                unsafe_allow_html=True
            )
