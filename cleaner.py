import pandas as pd
import os


def clean_dataset(input_file):

    # Read the dataset
    df = pd.read_csv(input_file)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    for column in df.columns:

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())

        # Text columns
        else:
            df[column] = df[column].fillna("Unknown")

    # Round all numeric columns to 2 decimal places
    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].round(2)

    # Create cleaned folder if it doesn't exist
    os.makedirs("cleaned", exist_ok=True)

    # Create cleaned filename
    filename = os.path.basename(input_file)
    name = os.path.splitext(filename)[0]

    output_file = os.path.join(
        "cleaned",
        f"{name}_cleaned.csv"
    )

    # Save cleaned dataset
    df.to_csv(output_file, index=False)

    return output_file

