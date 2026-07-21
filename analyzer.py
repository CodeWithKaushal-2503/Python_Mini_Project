import pandas as pd


def analyze_dataset(file_path):

    # Read CSV
    df = pd.read_csv(file_path)

    # Basic Information
    rows = df.shape[0]
    columns = df.shape[1]

    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())
    memory = round(df.memory_usage(deep=True).sum() / 1024, 2)

    # ---------------- Health Score ---------------- #

    score = 100

    score -= missing * 5
    score -= duplicates * 10

    if score < 0:
        score = 0

    if score >= 90:
        status = "Excellent"
    elif score >= 70:
        status = "Good"
    elif score >= 50:
        status = "Average"
    else:
        status = "Poor"

    # ---------------- Missing Values by Column ---------------- #

    missing_by_column = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_by_column.columns = [
        "Column",
        "Missing"
    ]

    missing_by_column = missing_by_column[
        missing_by_column["Missing"] > 0
    ]

    # ---------------- Summary Statistics ---------------- #

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:

        average_values = numeric_df.mean().round(2).to_dict()
        minimum_values = numeric_df.min().to_dict()
        maximum_values = numeric_df.max().to_dict()

    else:

        average_values = {}
        minimum_values = {}
        maximum_values = {}

    # ---------------- Report ---------------- #

    report = {

        # Basic Information
        "rows": rows,
        "columns": columns,
        "column_names": list(df.columns),

        # Data Quality
        "missing_values": missing,
        "duplicate_rows": duplicates,
        "memory_usage": memory,

        # Health Score
        "health_score": score,
        "status": status,

        # Preview
        "preview_columns": list(df.columns),
        "preview_data": df.head().values.tolist(),

        # Missing Value Analysis
        "missing_columns": missing_by_column["Column"].tolist(),
        "missing_count": missing_by_column["Missing"].tolist(),

        # Summary Statistics
        "average_values": average_values,
        "minimum_values": minimum_values,
        "maximum_values": maximum_values

    }

    return report