import streamlit as st
import json
import base64

st.markdown("""
    <style>
        .stApp {
            background-color: white !important;
        }
        
        .stApp h1 {
            color: red !important;
        }

        .stHeader, .stSubheader, .stMarkdown, .stText {
            color: #00008B !important;  
        }

        label[data-baseweb="label"], .stCheckbox label, .stRadio label {
            color: #00008B !important;
        }

        .stCheckbox input[type="checkbox"] + div, .stRadio input[type="radio"] + div {
            color: #00008B !important;
        }

        .stDataFrame, .stTable {
            color: black !important;
            background-color: white !important;
            border: 2px solid black !important;
        }
        .stTable th, .stTable td {
            color: black !important;
            border: 1px solid black !important;
        }

        .stMarkdown h3 {
            color: black !important;
        }

        input#age_input {
            background-color: #E0F7FF !important;  
            color: white !important;               
            border: 1px solid #00008B !important;  
            border-radius: 5px;
            padding: 5px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

with open(r"D:\FAST_NUCES\5th_Semester\Knowledge_Representation_and_Reasoning\Rule_based_diagnosis\Disease_rule_based.json") as f:
    data = json.load(f)

decision_table = data["nodes"][1]["content"]
rules = decision_table["rules"]
symptoms = decision_table["inputs"]
disease_info = decision_table["outputs"]

input_id = {i["id"]: i["field"] for i in symptoms}   
output_field = disease_info[0]["id"]

def process_val(val):
    if isinstance(val, str):
        s = val.strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        ls = s.lower()
        if ls == "true":
            return True
        if ls == "false":
            return False
        if s == "":
            return None
        return s
    return val

def best_match(user_input):
    selected_symptoms = [k for k, v in user_input.items()
                         if k.lower() not in ("age", "gender") and v is True]
    if not selected_symptoms:
        return "Other", [], []

    full_info = []  
    for rule in rules:
        disease = rule.get(output_field, "Other").strip('"')
        matches = 0
        total = 0
        for in_id, expected_val in rule.items():
            if in_id not in input_id:
                continue
            expected = process_val(expected_val)
            if expected is None:
                continue

            field = input_id[in_id]
            user_val = user_input.get(field, None)

            if expected is True:
                total += 1
                if user_val is True:
                    matches += 1
            elif isinstance(expected, str):
                total += 1
                if isinstance(user_val, str) and user_val.strip().lower() == expected.strip().lower():
                    matches += 1

        if total > 0:
            percent = round((matches / total) * 100, 1)
            full_info.append((disease, matches, total, percent))

    if not full_info:
        return "Other", [], []

    max_matches = max(m for (_, m, _, _) in full_info)
    if max_matches == 0:
        return "Other", [], full_info

    candidates = [(d, m, t, p) for (d, m, t, p) in full_info if m == max_matches]

    if len(candidates) > 1:
        candidates_sorted = sorted(candidates, key=lambda x: x[0].lower())
        names_with_perc = [f"{d} ({p}%)" for (d, _, _, p) in candidates_sorted]
        result_text = "Could be: " + " OR ".join(names_with_perc)
        return result_text, candidates_sorted, full_info

    d, m, t, p = candidates[0]
    return f"{d} ({p}% match)", [(d, m, t, p)], full_info

def add_bg_from_url(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    img_base64 = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: scroll;  
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url(r"D:/FAST_NUCES/5th_Semester/Knowledge_Representation_and_Reasoning/Rule_based_diagnosis/background_pic.jpg")  

st.title("Dr. AI")
st.write("Answer the following to get your diagnosis:")
st.write("*Check all symptoms that match\n*If symptoms are similar, check the one that is more exact.*")

user_input = {}
for inp in symptoms:
    field = inp["field"]
    name = inp["name"]

    if field.lower() == "age":
        st.markdown(f"<label for='age_input' style='color:#00008B; font-weight:bold;'>{name}</label>", unsafe_allow_html=True)
        age_str = st.text_input(label="", value="0", key="age_input")  
        try:
            val = int(age_str)
        except:
            val = 0
    elif field.lower() == "gender":
        val = st.radio(name, ["Male", "Female"])
    else:
        val = st.checkbox(name)
    user_input[field] = val

show_match_table = st.checkbox("Show match table")

if st.button("Get Diagnosis"):
    result, candidates, all_info = best_match(user_input)

    st.markdown(f"""
        <div style='background-color:#d4edda; color:red; padding:10px; border-radius:5px; margin-bottom:10px;'>
            <strong>Result:</strong> {result}
        </div>
    """, unsafe_allow_html=True)

    if candidates:
        st.markdown(f"""
            <div style='background-color:#d4edda; color:red; padding:5px 10px; border-radius:5px; margin-bottom:5px;'>
                <strong>Top candidate(s):</strong>
            </div>
        """, unsafe_allow_html=True)
        for d, m, t, p in candidates:
            st.markdown(f"""
                <div style='background-color:#d4edda; color:red; padding:5px 10px; border-radius:5px; margin-bottom:2px;'>
                    - {d}: {m}/{t} matching conditions — {p}%
                </div>
            """, unsafe_allow_html=True)

    if show_match_table:
        if not all_info:
            st.info("No informative rule conditions found in the decision table.")
        else:
            st.markdown("### Full match table")
            all_info_sorted = sorted(all_info, key=lambda x: (-x[1], -x[3], x[0].lower()))
            st.table([{"Disease": d, "Matches": m, "Total": t, "Percent": f"{p}%"} 
                      for (d, m, t, p) in all_info_sorted])
