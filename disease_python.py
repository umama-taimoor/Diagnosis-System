from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()
# Update this path to your Prolog file
prolog.consult(r"d:\FAST_NUCES\5th_Semester\Knowledge_Representation_and_Reasoning\Prolog_diagnosis\disease.pl")

# List of all symptoms
all_symptoms = [
    "facial_pain",
    "nasal_congestion",
    "thick_yellow_green_discharge",
    "fever",
    "reduced_smell",
    "sneezing",
    "runny_clear_discharge",
    "itchy_eyes",
    "itchy_nose",
    "seasonal_or_triggered_by_allergens",
    "nasal_blockage",
    "persistent_facial_pressure",
    "postnasal_drip",
    "loss_of_smell",
    "fatigue",
    "symptoms_longer_than_12_weeks",
    "nasal_obstruction_one_side",
    "recurrent_sinus_infections",
    "frequent_nosebleeds",
    "noisy_breathing_during_sleep",
    "headache"
]

def ask_symptoms():
    # Clear previous symptoms
    list(prolog.query("retractall(symptom(_))"))

    print("Please answer the following questions with yes/no (or y/n):\n")

    # Ask symptoms
    for symptom in all_symptoms:
        while True:
            answer = input(f"Do you have {symptom.replace('_',' ')}? (yes/no): ").strip().lower()
            if answer in ["yes", "y"]:
                prolog.assertz(f"symptom({symptom})")
                break
            elif answer in ["no", "n", ""]:
                break
            else:
                print("Invalid input. Please answer with yes, no, y, or n. Press Enter for no.")

    # Show all disease match counts
    all_matches = list(prolog.query("diagnose_all(S)"))
    if all_matches:
        S = all_matches[0]['S']
        print("\nAll disease match counts:")
        for item in S:
            try:
                pair = item
                # If item is single-element list, extract it
                if isinstance(item, list) and len(item) == 1:
                    pair = item[0]
                # If pair is string like "chronic_sinusitis-1"
                if isinstance(pair, str):
                    disease, count = pair.split("-")
                    count = int(count)
                # If pair is tuple (disease, count)
                elif isinstance(pair, tuple):
                    disease, count = pair
                # Otherwise, assume it's already a list of two items
                else:
                    disease, count = pair
                print(f"{disease}: {count} matched symptom(s)")
            except Exception:
                print(f"{item}: (matched symptom(s))")

    # Diagnose top disease
    diagnosis_query = list(prolog.query("diagnose(D)"))
    if diagnosis_query:
        D = diagnosis_query[0]['D']
        print(f"\nTop Diagnosis: {D}\n")
    else:
        D = "unknown"
        print("\nTop Diagnosis: unknown\n")

    # Show matched symptoms for top diagnosis
    print("Matched symptoms for top diagnosis:")
    list(prolog.query(f"explain({D})"))  # explain/1 prints directly in Prolog

if __name__ == "__main__":
    ask_symptoms()
