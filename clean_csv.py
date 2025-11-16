import pandas as pd

def clean_csv_file(df):
    df = df.copy()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert numeric columns safely
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # DO NOT drop rows with missing close immediately — be gentle
    if "Close" in df.columns:
        df = df[df["Close"].notna()]

    df.reset_index(drop=True, inplace=True)

    return df
