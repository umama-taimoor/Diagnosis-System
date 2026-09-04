:- dynamic symptom/1.

% -----------------------------
% Diseases and their symptoms
% -----------------------------
disease(acute_sinusitis).
disease(rhinitis).
disease(chronic_sinusitis).
disease(deviated_nasal_septum).

disease_symptom(acute_sinusitis, facial_pain).
disease_symptom(acute_sinusitis, nasal_congestion).
disease_symptom(acute_sinusitis, thick_yellow_green_discharge).
disease_symptom(acute_sinusitis, fever).
disease_symptom(acute_sinusitis, reduced_smell).

disease_symptom(rhinitis, nasal_congestion).
disease_symptom(rhinitis, sneezing).
disease_symptom(rhinitis, runny_clear_discharge).
disease_symptom(rhinitis, itchy_eyes).
disease_symptom(rhinitis, itchy_nose).
disease_symptom(rhinitis, seasonal_or_triggered_by_allergens).

disease_symptom(chronic_sinusitis, nasal_blockage).
disease_symptom(chronic_sinusitis, persistent_facial_pressure).
disease_symptom(chronic_sinusitis, postnasal_drip).
disease_symptom(chronic_sinusitis, loss_of_smell).
disease_symptom(chronic_sinusitis, fatigue).
disease_symptom(chronic_sinusitis, symptoms_longer_than_12_weeks).

disease_symptom(deviated_nasal_septum, nasal_obstruction_one_side).
disease_symptom(deviated_nasal_septum, recurrent_sinus_infections).
disease_symptom(deviated_nasal_septum, frequent_nosebleeds).
disease_symptom(deviated_nasal_septum, noisy_breathing_during_sleep).
disease_symptom(deviated_nasal_septum, headache).

% -----------------------------
% Matching logic
% -----------------------------
matched_symptom(Disease, Symptom) :-
    disease_symptom(Disease, Symptom),
    symptom(Symptom).

count_matches(Disease, Count) :-
    findall(S, matched_symptom(Disease, S), L),
    length(L, Count).

% -----------------------------
% Diagnose all diseases
% -----------------------------
diagnose_all(Sorted) :-
    findall(D-Count, (disease(D), count_matches(D, Count)), Scores),
    sort(2, @>=, Scores, Sorted).  % sort descending by Count

% -----------------------------
% Diagnose best match
% -----------------------------
diagnose(Disease) :-
    diagnose_all([Disease-Count | _]),
    Count > 0, !.

diagnose(unknown) :-
    \+ symptom(_).


% Explain which symptoms matched for a disease
explain(Disease) :-
    diagnose(Disease),
    Disease \= unknown,
    findall(S, matched_symptom(Disease, S), Matched),
    format('Diagnosis: ~w~n', [Disease]),
    format('Matched symptoms: ~w~n', [Matched]).
    
% Optional: fallback for unknown
explain(unknown) :-
    format('No matching symptoms found. Diagnosis: unknown~n').
