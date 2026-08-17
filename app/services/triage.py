TRIAGE_ROUTINE = "routine"
TRIAGE_URGENT = "urgent"
TRIAGE_EMERGENCY = "emergency"
EMERGENCY_WARNING_SIGNS = [
    "difficulty breathing",
    "severe chest pain",
    "loss of consciousness",
    "uncontrolled bleeding",
    "severe allergic reaction",
    "seizure",
    "sudden weakness",
    "sudden confusion",
    "severe difficulty speaking",
]
def contains_emergency_warning_signs(text: str) -> bool:
    normalized_text = text.lower()

    return any(
        warning_sign in normalized_text
        for warning_sign in EMERGENCY_WARNING_SIGNS
    )
def determine_triage(text: str) -> str:
    if contains_emergency_warning_signs(text):
        return TRIAGE_EMERGENCY

    return TRIAGE_ROUTINE
def triage_case(
    symptoms: str,
    extracted_information: str = "",
) -> str:
    combined_text = f"{symptoms} {extracted_information}"

    return determine_triage(combined_text)
def requires_doctor_alert(triage_result: str) -> bool:
    return triage_result == TRIAGE_EMERGENCY