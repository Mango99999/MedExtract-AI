from src.models import MedicalExtraction


# Test 1: Valid data
valid_data = {
    "chief_complaint": "headache",
    "symptoms": ["headache", "fatigue"],
    "diagnosis": [],
    "medical_history": [],
    "medications": [],
    "procedures": [],
    "follow_up": None,
    "summary": "Patient reports headache and fatigue.",
    "risk_indicators": [],
    "urgency": None
}

result = MedicalExtraction.model_validate(valid_data)

print("TEST 1: Valid JSON")
print("PASSED")
print(result.model_dump_json(indent=2))


# Test 2: Wrong type
invalid_data = {
    "chief_complaint": "headache",
    "symptoms": "headache"
}

try:
    MedicalExtraction.model_validate(invalid_data)
    print("TEST 2: FAILED - Invalid data was accepted")

except Exception:
    print("\nTEST 2: Wrong type")
    print("PASSED - Invalid data was rejected")


# Test 3: Unexpected field
extra_field_data = {
    "chief_complaint": "headache",
    "symptoms": [],
    "doctor_name": "Ahmed"
}

try:
    MedicalExtraction.model_validate(extra_field_data)
    print("TEST 3: FAILED - Extra field was accepted")

except Exception:
    print("\nTEST 3: Extra field")
    print("PASSED - Extra field was rejected")