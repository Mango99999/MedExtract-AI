# MedExtract AI

## Clinical Notes → Structured Medical Information

MedExtract AI is a Generative AI project that extracts explicitly stated medical information from unstructured clinical notes and converts it into a consistent, validated JSON format.

The project was developed as part of a GenAI internship group project and focuses on:

- Prompt Engineering
- Structured LLM Output
- JSON Validation
- Error Handling and Retry/Repair
- LLM Evaluation
- Hallucination Prevention

> **Important:** MedExtract AI is an information extraction system. It does not diagnose patients, prescribe treatment, or invent information that is not explicitly present in the input.

---

## 1. Project Objective

Clinical notes are often written as free-form text. Important information such as symptoms, diagnoses, medications, procedures, and follow-up instructions can therefore be difficult to process automatically.

MedExtract AI uses an LLM to transform a clinical note such as:

```text
Patient reports severe chest pain and shortness of breath.
History of hypertension. Currently taking aspirin 81 mg daily.
Follow up with cardiology next week.
```

into structured information:

```json
{
  "chief_complaint": "severe chest pain",
  "symptoms": [
    "severe chest pain",
    "shortness of breath"
  ],
  "diagnosis": [],
  "medical_history": [
    "hypertension"
  ],
  "medications": [
    {
      "name": "aspirin",
      "dose": "81 mg",
      "frequency": "daily",
      "duration": null
    }
  ],
  "procedures": [],
  "follow_up": "Follow up with cardiology next week.",
  "summary": "Patient reports severe chest pain and shortness of breath, with a history of hypertension and current aspirin use.",
  "risk_indicators": [],
  "urgency": null
}
```

---
## 2. Target Audience

MedExtract AI is designed for users and organizations that need to convert unstructured clinical notes into structured medical information while reducing unsupported AI-generated information.

### Primary Audience

**Healthcare professionals and healthcare organizations**

The system can support doctors, nurses, clinics, and hospitals by organizing information from free-form clinical notes into a consistent JSON structure.

The system is intended to assist with **information organization and extraction**, not clinical decision-making.

### Secondary Audience

**AI and GenAI developers**

MedExtract AI demonstrates how Large Language Models can be used for structured information extraction while combining:

* Prompt engineering
* Structured JSON output
* Pydantic validation
* Error handling and retry/repair
* Hallucination prevention
* LLM evaluation

### Academic / Internship Audience

The project is also designed for **instructors, internship evaluators, and students** who want to understand how a GenAI application can be developed and evaluated systematically.

The project demonstrates the complete development process:

```text
Data
  ↓
Prompt Engineering
  ↓
LLM
  ↓
Structured Output
  ↓
Validation
  ↓
Error Analysis
  ↓
Evaluation
  ↓
Improved Prompt
```

### Intended Use

MedExtract AI can be used to:

* Extract explicitly stated symptoms
* Identify explicitly stated diagnoses
* Extract medications and their stated details
* Extract medical history
* Extract procedures
* Extract follow-up instructions
* Generate a summary based only on the clinical note
* Identify explicitly supported risk or urgency indicators
* Convert unstructured notes into consistent JSON

### Not Intended For

MedExtract AI is **not intended to**:

* Diagnose patients
* Recommend treatments
* Prescribe medication
* Replace healthcare professionals
* Make independent clinical decisions
* Infer diseases that are not explicitly stated

The system should always treat the source clinical note as the basis for extraction and should not invent missing information.


## 3. Core Pipeline

The main system follows this pipeline:

```text
Clinical Note
     |
     v
Prompt Engineering
     |
     v
Local / API LLM
     |
     v
Structured JSON
     |
     v
Pydantic Validation
     |
     +---- Invalid ----> Retry / Repair
     |
     v
Validated Medical Extraction
     |
     v
Summary / Risk / Urgency
```

---

## 4. Project Requirements

The system must:

1. Extract only information explicitly stated in the note.
2. Never hallucinate medical information.
3. Never diagnose a condition that is not explicitly diagnosed in the note.
4. Correctly handle missing information.
5. Return exactly the required JSON structure.
6. Produce valid JSON.
7. Validate the output using Pydantic.
8. Detect malformed output and invalid fields/types.
9. Retry or repair invalid LLM output.
10. Evaluate prompt versions using the same fixed test set.

---

## 5. Required JSON Schema

Every extraction should follow this structure:

```json
{
  "chief_complaint": null,
  "symptoms": [],
  "diagnosis": [],
  "medical_history": [],
  "medications": [
    {
      "name": null,
      "dose": null,
      "frequency": null,
      "duration": null
    }
  ],
  "procedures": [],
  "follow_up": null,
  "summary": null,
  "risk_indicators": [],
  "urgency": null
}
```

### Missing information

Use:

- `null` for missing single values
- `[]` for missing lists
- Medication fields that are not stated should be `null`

Example:

```json
{
  "chief_complaint": null,
  "symptoms": ["headache"],
  "diagnosis": [],
  "medical_history": [],
  "medications": [],
  "procedures": [],
  "follow_up": null,
  "summary": "Patient reports a headache.",
  "risk_indicators": [],
  "urgency": null
}
```

---

## 6. Important Extraction Rules

### Explicit information only

The model must extract information that is actually present in the text.

Bad behavior:

```text
Patient feels tired.
```

Incorrect:

```json
"diagnosis": ["depression"]
```

The note does not explicitly diagnose depression.

Correct:

```json
"diagnosis": []
```

---

### Diagnosis vs symptoms

A statement such as:

```text
Patient demonstrated symptoms of depression.
```

should not automatically become:

```json
"diagnosis": ["depression"]
```

because the text describes symptoms rather than explicitly stating a diagnosis.

This distinction is one of the important cases used during prompt evaluation.

---

### No hallucination

The model must not invent:

- medications
- doses
- diagnoses
- medical history
- procedures
- dates
- symptoms
- test results
- patient information

If it is not in the note, it should not be added.

---

### Negation

The model should correctly understand statements such as:

```text
Patient denies headache.
```

The system should not report:

```json
"symptoms": ["headache"]
```

as if the patient had the symptom.

---

### Ambiguous statements

If the note is unclear, the model should avoid making unsupported assumptions.

---

## 7. Dataset

The project currently uses two CSV datasets:

```text
data/
├── clinical_notes.csv
└── patient_diaries.csv
```

Both datasets contain:

```text
timestamp
text
label
response_length
sentiment
interaction_depth
turn_taking_frequency
```

The primary field used by the extraction system is:

```text
text
```

The other metadata fields are not required for the LLM extraction task.

### Dataset observations

The datasets contain short and highly repetitive text.

The clinical notes dataset contains approximately:

- 1,000 rows
- 57 unique texts

The patient diaries dataset contains approximately:

- 1,000 rows
- 64 unique texts

Because of this repetition, the project uses a fixed test set containing unique examples instead of repeatedly testing duplicate rows.

---

## 8. Test Set

The fixed evaluation set is:

```text
data/test_set.csv
```

It contains:

- 20 clinical notes
- 10 patient diary entries
- 30 total test cases

The test set should remain fixed while comparing Prompt V1, V2, V3, and the final prompt.

This makes prompt evaluation more meaningful because every version is tested on the same inputs.

---

## 9. Patient Diaries as Robustness Tests

Patient diary entries are useful for testing whether the model hallucinates diagnoses.

For example:

```text
I felt confused today. I felt overwhelmed with sadness and isolation.
```

The system should not automatically produce:

```json
"diagnosis": ["depression"]
```

because the diary does not explicitly state that diagnosis.

These examples help evaluate whether the prompt follows the project's explicit-only extraction rule.

---

## 10. Prompt Engineering

The project uses an iterative prompt engineering process.

```text
Prompt V1
   |
   v
Run Test Set
   |
   v
Document Failures
   |
   v
Prompt V2
   |
   v
Run Test Set
   |
   v
Document Failures
   |
   v
Prompt V3
   |
   v
Run Test Set
   |
   v
Final Prompt
```

### Prompt V1

Current baseline prompt:

```text
You are a medical information extraction assistant.

Read the clinical note provided by the user and extract the medical information from it.

Return the information as JSON using exactly this structure:

{
  "chief_complaint": null,
  "symptoms": [],
  "diagnosis": [],
  "medical_history": [],
  "medications": [
    {
      "name": null,
      "dose": null,
      "frequency": null,
      "duration": null
    }
  ],
  "procedures": [],
  "follow_up": null,
  "summary": null,
  "risk_indicators": [],
  "urgency": null
}

Extract information that is mentioned in the note.

If information is not available, use null for single values and [] for lists.

Do not add information that is not present in the note.

Return valid JSON only.
```

Prompt V1 is intentionally simple because it serves as the baseline for measuring improvements.

### Expected Prompt V1 weaknesses

The baseline may need stronger handling of:

- Diagnosis vs symptoms
- Negation
- Ambiguity
- Risk indicators
- Urgency
- Medication details
- Strict JSON formatting
- Explicit-only extraction
- Diary/personal statements

These failures should be measured rather than assumed.

---

## 11. Pydantic Validation

The project uses Pydantic to validate the LLM output.

The main model is located in:

```text
src/models.py
```

It contains:

- `Medication`
- `MedicalExtraction`

The model rejects unexpected fields using:

```python
ConfigDict(extra="forbid")
```

This prevents the LLM from silently adding fields outside the required schema.

### Validation tests

Validation tests are located in:

```text
tests/test_models.py
```

The tests currently verify:

1. Valid JSON is accepted.
2. Incorrect data types are rejected.
3. Unexpected fields are rejected.

Example:

```text
TEST 1: Valid JSON
PASSED

TEST 2: Wrong type
PASSED - Invalid data was rejected

TEST 3: Extra field
PASSED - Extra field was rejected
```

Run the tests from the project root with:

```powershell
python -m tests.test_models
```

---

## 12. Project Structure

The current project is organized approximately as follows:

```text
1/
│
├── data/
│   ├── clinical_notes.csv
│   ├── patient_diaries.csv
│   └── test_set.csv
│
├── prompts/
│   └── prompt_v1.txt
│
├── src/
│   └── models.py
│
├── tests/
│   └── test_models.py
│
├── inspect_data.py
├── create_test_set.py
└── README.md
```

As development continues, additional files can be added for:

```text
src/
├── models.py
├── llm.py
├── extractor.py
├── validator.py
└── evaluator.py
```

and:

```text
prompts/
├── prompt_v1.txt
├── prompt_v2.txt
├── prompt_v3.txt
└── prompt_final.txt
```

---

## 13. Environment Setup

### Python

The project uses Python 3.

Check your version:

```powershell
python --version
```

Example:

```text
Python 3.14.6
```

### Pip

Check pip:

```powershell
python -m pip --version
```

### Install Pydantic

```powershell
python -m pip install pydantic
```

The current project uses Pydantic 2.x.

---

## 14. Local LLM

The project can use a local LLM so that an API key is not required.

One planned option is Ollama.

After installing Ollama, check it with:

```powershell
ollama --version
```

A local model can then be downloaded and used by the Python application.

The exact model should be selected based on the computer's available RAM/VRAM and performance.

> The LLM is interchangeable. The extraction schema, prompts, validation, and evaluation pipeline should remain independent from the specific model.

---

## 15. Running the Project

From the project root:

```powershell
cd "C:\Users\20112\OneDrive\Desktop\1"
```

### Inspect the datasets

```powershell
python inspect_data.py
```

This reports:

- Number of rows
- Columns
- Data types
- Missing values
- Duplicate rows
- Text lengths
- Example texts

### Create the fixed test set

```powershell
python create_test_set.py
```

### Run validation tests

```powershell
python -m tests.test_models
```

---

## 15. Evaluation

The project should evaluate both technical correctness and extraction quality.

### A. JSON validity

Check whether the LLM response is valid JSON.

Possible metric:

```text
JSON Validity Rate =
Valid JSON Outputs / Total Outputs
```

---

### B. Schema validity

Check whether the JSON:

- Contains all required fields
- Does not contain unexpected fields
- Uses the correct types
- Contains correctly structured medication objects

Pydantic handles this part.

---

### C. Extraction correctness

Check whether information in the note was extracted correctly.

Examples:

- Correct symptom extraction
- Correct diagnosis extraction
- Correct medication extraction
- Correct medical history
- Correct follow-up

---

### D. Hallucination rate

Check whether the model added information that was not present.

This is particularly important for medical extraction.

Example:

```text
Input:
Patient reports feeling tired.
```

If the output says:

```json
"diagnosis": ["depression"]
```

that is an unsupported inference and should count as an error.

---

### E. Negation accuracy

Test statements such as:

```text
Patient denies chest pain.
```

The system should preserve the meaning of the note rather than treating every medical term as a positive symptom.

---

### F. Prompt comparison

Every prompt version should be evaluated using the same test set.

A future evaluation table can look like:

| Metric | V1 | V2 | V3 | Final |
|---|---:|---:|---:|---:|
| JSON validity | - | - | - | - |
| Schema validity | - | - | - | - |
| Extraction correctness | - | - | - | - |
| Hallucination rate | - | - | - | - |
| Negation accuracy | - | - | - | - |

Do not fill these values until the tests have actually been run.

---

## 17. Error Handling

The LLM can sometimes return invalid JSON.

Example:

```text
Here is the extracted information:
{
  ...
}
```

The extra text can make strict JSON parsing fail.

The system should therefore use a validation and retry/repair process:

```text
LLM
 |
 v
Parse JSON
 |
 +---- Valid ----> Pydantic
 |
 +---- Invalid
          |
          v
     Repair / Retry
          |
          v
     Parse again
```

The system should log failures so that prompt weaknesses can be identified.

---

## 18. Safety and Scope

MedExtract AI is an extraction and summarization project.

It should:

- Extract explicitly stated information.
- Summarize information from the note.
- Identify risk/urgency indicators only when supported by the text.
- Preserve missing information as `null` or `[]`.

It should **not**:

- Diagnose patients.
- Recommend treatment.
- Prescribe medication.
- Invent medical history.
- Infer unsupported diseases.
- Replace a healthcare professional.
- Generate information not contained in the source note.

Only synthetic or public data should be used for development and testing.

---

## 19. Optional Voice Input (Speech-to-Text)

Voice input can be added to MedExtract AI as an input layer before the existing clinical information extraction pipeline.

The recommended Speech-to-Text (STT) solution is **Whisper**.

Whisper converts spoken audio into text. The resulting text is then processed by the same prompt engineering, LLM extraction, and Pydantic validation pipeline used for normal text input.

### Voice Architecture

The extended MedExtract AI architecture becomes:

```text
Microphone
    |
    v
Audio Recording
    |
    v
Whisper Speech-to-Text
    |
    v
Clinical Note Text
    |
    v
Prompt Engineering
    |
    v
Local / API LLM
    |
    v
Structured JSON
    |
    v
Pydantic Validation
    |
    +---- Invalid ----> Retry / Repair
    |
    v
Validated Medical Extraction
    |
    v
Summary / Risk / Urgency
```

### Why Whisper?

Whisper is a suitable choice for this project because:

* It is designed for speech recognition.
* It can run locally.
* It supports multiple languages, including English and Arabic.
* It converts speech into normal text before the medical extraction process.
* It keeps Speech-to-Text separate from the medical information extraction task.
* It does not need to replace the existing LLM or Pydantic validation system.

### Separation of Responsibilities

Each component should have a specific responsibility:

| Component      | Responsibility               |
| -------------- | ---------------------------- |
| Microphone     | Capture the user's voice     |
| Whisper        | Convert speech into text     |
| Prompt         | Define extraction rules      |
| LLM            | Extract medical information  |
| Pydantic       | Validate the JSON structure  |
| Retry / Repair | Handle invalid LLM responses |
| Evaluation     | Measure system performance   |

For example, if a user says:

```text
Patient reports severe headache and fatigue. The patient is taking aspirin 81 mg daily.
```

Whisper produces the clinical note text:

```text
Patient reports severe headache and fatigue. The patient is taking aspirin 81 mg daily.
```

The text is then passed to the existing extraction pipeline.

The LLM should produce structured information such as:

```json
{
  "chief_complaint": "severe headache",
  "symptoms": [
    "severe headache",
    "fatigue"
  ],
  "diagnosis": [],
  "medical_history": [],
  "medications": [
    {
      "name": "aspirin",
      "dose": "81 mg",
      "frequency": "daily",
      "duration": null
    }
  ],
  "procedures": [],
  "follow_up": null,
  "summary": "Patient reports severe headache and fatigue and is taking aspirin 81 mg daily.",
  "risk_indicators": [],
  "urgency": null
}
```

### Important Design Principle

Whisper should **only transcribe the audio**.

It should not be responsible for:

* Diagnosing the patient
* Extracting medical conditions
* Creating medical summaries
* Determining medication information
* Generating risk indicators

Those tasks remain part of the existing MedExtract AI extraction pipeline.

The responsibilities are therefore:

```text
Voice
  |
  v
Whisper
  |
  |  Speech → Text
  v
Clinical Note
  |
  v
LLM
  |
  |  Text → Structured Medical Information
  v
JSON
  |
  v
Pydantic
  |
  |  Validate
  v
Final Result
```

### Voice Input and Existing Text Input

The system should support both text and voice:

```text
                 +------------------+
                 |   User Input     |
                 +--------+---------+
                          |
                 +--------+--------+
                 |                 |
                 v                 v
              Text Input       Voice Input
                                   |
                                   v
                                Whisper
                                   |
                                   v
                              Text Output
                 |                 |
                 +--------+--------+
                          |
                          v
                    Prompt / LLM
                          |
                          v
                   Structured JSON
                          |
                          v
                   Pydantic Validation
                          |
                          v
                    Final Extraction
```

This means adding voice recognition does not require rebuilding the core extraction system.

### Recommended Implementation Order

Voice input should be implemented **after the text-based extraction pipeline is working reliably**.

Recommended order:

1. Complete Prompt V1.
2. Test Prompt V1.
3. Create Prompt V2.
4. Create Prompt V3.
5. Build the validation and retry system.
6. Evaluate the prompts.
7. Finalize the text extraction pipeline.
8. Add Whisper for voice input.
9. Test speech-to-text accuracy.
10. Test the complete Voice → Text → LLM → JSON pipeline.

This keeps the project modular and makes it easier to determine whether an error came from speech recognition or medical information extraction.

### Future Voice Improvements

Possible future improvements include:

* Real-time microphone input
* Arabic speech recognition
* English/Arabic language selection
* Automatic language detection
* Audio preprocessing
* Noise reduction
* Speech-to-text confidence tracking
* Voice transcription history
* Integration with a Streamlit interface
* Support for longer clinical conversations
* Testing transcription errors separately from LLM extraction errors

Voice input remains an **optional extension** of MedExtract AI and should not change the core extraction rules, JSON schema, validation system, or evaluation methodology.

## 20. Future Improvements

Possible improvements include:

- Stronger Prompt V2 and V3
- Few-shot examples
- Better negation handling
- Better ambiguity handling
- Automated evaluation
- Automatic retry/repair
- LLM-as-a-judge evaluation
- Web/API interface
- Streamlit interface
- Voice input
- ICD-10 lookup
- Logging and experiment tracking
- More diverse clinical test cases
- More difficult hallucination tests

---

## 21. Recommended Development Order

To avoid building everything at once, follow this order:

### Phase 1 — Data

- [x] Inspect datasets
- [x] Understand columns
- [x] Identify duplicates
- [x] Create fixed test set

### Phase 2 — Validation

- [x] Create Pydantic models
- [x] Test valid output
- [x] Test invalid types
- [x] Test unexpected fields

### Phase 3 — LLM

- [ ] Install local LLM
- [ ] Download a suitable model
- [ ] Connect Python to the model
- [ ] Send one test note
- [ ] Parse the response

### Phase 4 — Prompt Engineering

- [x] Create Prompt V1
- [ ] Test V1 on all 30 cases
- [ ] Document failures
- [ ] Create Prompt V2
- [ ] Test V2
- [ ] Create Prompt V3
- [ ] Test V3
- [ ] Select/finalize the best prompt

### Phase 5 — Validation and Error Handling

- [ ] Validate every LLM response
- [ ] Add retry/repair
- [ ] Log failures
- [ ] Re-test after repairs

### Phase 6 — Evaluation

- [ ] JSON validity
- [ ] Schema validity
- [ ] Extraction correctness
- [ ] Hallucination rate
- [ ] Negation accuracy
- [ ] Prompt comparison

### Phase 7 — Interface

- [ ] Command-line interface
- [ ] Optional web interface
- [ ] Optional voice input

---

## 22. Quick Start

After setup, the basic workflow is:

```powershell
cd "C:\Users\20112\OneDrive\Desktop\1"

python inspect_data.py

python create_test_set.py

python -m tests.test_models
```

Once the local LLM is installed:

```text
Run one clinical note
        ↓
Check JSON
        ↓
Validate with Pydantic
        ↓
Run all 30 test cases
        ↓
Analyze failures
        ↓
Improve prompt
        ↓
Repeat
```

---

## 23. Current Project Status

At the current stage:

- Dataset inspection is complete.
- The fixed 30-case test set has been created.
- Prompt V1 has been created.
- Pydantic schema validation has been implemented.
- Validation tests pass.
- The next major step is connecting a local LLM and testing Prompt V1 against the fixed test set.

---

## 24. License / Disclaimer

This project is an educational GenAI internship project.

It is not a medical diagnostic system and should not be used to make clinical decisions.

All development and testing should use synthetic or appropriately public/anonymized data.
