import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

CLINICAL_FILE = "data/clinical_notes.csv"
DIARY_FILE = "data/patient_diaries.csv"

OUTPUT_FILE = "data/test_set.csv"

NUMBER_OF_CLINICAL_NOTES = 20
NUMBER_OF_DIARY_NOTES = 10


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Could not find: {file_path}\n"
            "Check that the file exists inside the data folder."
        )

    return pd.read_csv(file_path)


# ============================================================
# SELECT UNIQUE TEXTS
# ============================================================

def get_unique_texts(df, number_of_texts):
    if "text" not in df.columns:
        raise ValueError("The dataset does not contain a 'text' column.")

    # Remove missing values
    texts = df["text"].dropna().astype(str)

    # Remove duplicate texts
    texts = texts.drop_duplicates()

    # Take the requested number
    return texts.head(number_of_texts).tolist()


# ============================================================
# CREATE TEST SET
# ============================================================

def create_test_set():

    print("=" * 70)
    print("MedExtract AI - Creating Test Set")
    print("=" * 70)

    # Load datasets
    clinical_notes = load_data(CLINICAL_FILE)
    patient_diaries = load_data(DIARY_FILE)

    # Get unique texts
    clinical_texts = get_unique_texts(
        clinical_notes,
        NUMBER_OF_CLINICAL_NOTES
    )

    diary_texts = get_unique_texts(
        patient_diaries,
        NUMBER_OF_DIARY_NOTES
    )

    # Create records
    records = []

    # Clinical notes
    for text in clinical_texts:
        records.append({
            "source": "clinical_note",
            "text": text
        })

    # Patient diaries
    for text in diary_texts:
        records.append({
            "source": "patient_diary",
            "text": text
        })

    # Create DataFrame
    test_set = pd.DataFrame(records)

    # Add an ID
    test_set.insert(
        0,
        "test_id",
        range(1, len(test_set) + 1)
    )

    # Save
    test_set.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print("\nTest set created successfully!")

    print(f"\nClinical notes selected : {len(clinical_texts)}")
    print(f"Patient diaries selected: {len(diary_texts)}")
    print(f"Total test cases        : {len(test_set)}")

    print(f"\nSaved to:")
    print(f"  {OUTPUT_FILE}")

    print("\n" + "=" * 70)
    print("TEST SET")
    print("=" * 70)

    for _, row in test_set.iterrows():
        print(
            f"\n[{row['test_id']}] "
            f"{row['source']}"
        )
        print(row["text"])

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    create_test_set()