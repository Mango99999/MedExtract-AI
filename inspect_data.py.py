import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

CLINICAL_FILE = "data/clinical_notes.csv"
DIARY_FILE = "data/patient_diaries.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_dataset(file_path, dataset_name):
    """Load a CSV file and give a clear error if something is wrong."""

    print("=" * 70)
    print(f"LOADING: {dataset_name}")
    print("=" * 70)

    if not os.path.exists(file_path):
        print(f"ERROR: File not found:")
        print(f"      {file_path}")
        print()
        print("Make sure your folder structure is:")
        print("MedExtract-AI/")
        print("├── data/")
        print("│   ├── clinical_notes.csv")
        print("│   └── patient_diaries.csv")
        print("└── inspect_data.py")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded: {file_path}")
        return df

    except Exception as e:
        print(f"ERROR while reading {file_path}")
        print(e)
        return None


def inspect_dataset(df, dataset_name):
    """Print useful information about a dataset."""

    if df is None:
        return

    print("\n" + "=" * 70)
    print(f"{dataset_name} - BASIC INFORMATION")
    print("=" * 70)

    # Shape
    rows, columns = df.shape
    print(f"Number of rows    : {rows}")
    print(f"Number of columns : {columns}")

    # Columns
    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    # Data types
    print("\nData types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing values:")
    missing = df.isnull().sum()

    for column, count in missing.items():
        print(f"  {column}: {count}")

    # Duplicate rows
    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    # Text column
    if "text" not in df.columns:
        print("\nWARNING: 'text' column was not found!")
        return

    print("\n" + "=" * 70)
    print(f"{dataset_name} - TEXT INFORMATION")
    print("=" * 70)

    # Convert to string so we don't crash on unexpected values
    text_data = df["text"].dropna().astype(str)

    print(f"Total text entries : {len(text_data)}")
    print(f"Unique text entries: {text_data.nunique()}")
    print(f"Duplicate texts    : {len(text_data) - text_data.nunique()}")

    # Text length
    text_lengths = text_data.str.len()

    print(f"\nText length:")
    print(f"  Minimum : {text_lengths.min()}")
    print(f"  Maximum : {text_lengths.max()}")
    print(f"  Average : {text_lengths.mean():.2f}")

    # First examples
    print("\n" + "=" * 70)
    print(f"{dataset_name} - FIRST 10 EXAMPLES")
    print("=" * 70)

    for i, text in enumerate(text_data.head(10), start=1):
        print(f"\n{i}. {text}")

    # Unique examples
    unique_texts = text_data.drop_duplicates()

    print("\n" + "=" * 70)
    print(f"{dataset_name} - FIRST 30 UNIQUE TEXTS")
    print("=" * 70)

    for i, text in enumerate(unique_texts.head(30), start=1):
        print(f"\n{i}. {text}")


def compare_datasets(clinical_notes, patient_diaries):
    """Compare the two datasets."""

    if clinical_notes is None or patient_diaries is None:
        return

    print("\n" + "=" * 70)
    print("DATASET COMPARISON")
    print("=" * 70)

    print(f"\nClinical notes:")
    print(f"  Rows: {len(clinical_notes)}")

    print(f"\nPatient diaries:")
    print(f"  Rows: {len(patient_diaries)}")

    if "text" in clinical_notes.columns and "text" in patient_diaries.columns:

        clinical_unique = clinical_notes["text"].dropna().nunique()
        diary_unique = patient_diaries["text"].dropna().nunique()

        print("\nUnique texts:")
        print(f"  Clinical notes : {clinical_unique}")
        print(f"  Patient diaries: {diary_unique}")

    # Check whether both datasets have the same columns
    clinical_columns = set(clinical_notes.columns)
    diary_columns = set(patient_diaries.columns)

    print("\nSame columns:", clinical_columns == diary_columns)

    if clinical_columns != diary_columns:
        print("\nColumns only in clinical notes:")
        print(clinical_columns - diary_columns)

        print("\nColumns only in patient diaries:")
        print(diary_columns - clinical_columns)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("*" * 70)
    print("              MedExtract AI - DATA INSPECTION")
    print("*" * 70)
    print()

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    clinical_notes = load_dataset(
        CLINICAL_FILE,
        "Clinical Notes"
    )

    patient_diaries = load_dataset(
        DIARY_FILE,
        "Patient Diaries"
    )

    # --------------------------------------------------------
    # Inspect clinical notes
    # --------------------------------------------------------

    inspect_dataset(
        clinical_notes,
        "CLINICAL NOTES"
    )

    # --------------------------------------------------------
    # Inspect patient diaries
    # --------------------------------------------------------

    inspect_dataset(
        patient_diaries,
        "PATIENT DIARIES"
    )

    # --------------------------------------------------------
    # Compare datasets
    # --------------------------------------------------------

    compare_datasets(
        clinical_notes,
        patient_diaries
    )

    # --------------------------------------------------------
    # Finish
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATA INSPECTION COMPLETE")
    print("=" * 70)
    print()


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()