import json
import importlib
import pandas as pd
from phone_api import validate_phone


def load_phone_numbers_csv(file_path: str, phone_number: str = 'phone_number') -> list:
    """
    Loads phone numbers from a CSV file, extracting the 'phone_numbers' column.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of phone numbers.
    """
    try:
        df = pd.read_csv(file_path)
        if phone_number not in df.columns:
            raise ValueError(f"CSV file must contain a {phone_number} column.")
        # Ensure no NaN values and convert to string
        df = df[df[phone_number].notna()]
        df = df.drop_duplicates()
        df['phone_number_str'] = df[phone_number].astype(int).astype(str)
        # return df[phone_number].dropna().astype(str).tolist()
        df = df[['phone_number_str', phone_number]]
        return (df)
    except Exception as e:
        print(f"Error loading phone numbers: {e}")
        return []


def save_results_to_csv(data: list, file_path: str, original_data: pd.DataFrame) -> None:
    """
    Converts results to a Pandas DataFrame and saves to CSV.

    Args:
        data (list): List of API responses.
        file_path (str): Path to save the CSV file.
        original_data (pd.DataFrame): original dataframe that includes original phone number var
    """
    df = pd.DataFrame(data)  # Convert to DataFrame
    # Merge back with original dataframe
    phone_numbers_merged = pd.merge(df, original_data, how='outer',
                                    left_on='phone_number_input_api', right_on='phone_number_str')
    phone_numbers_merged.drop('phone_number_str', axis=1, inplace=True)
    phone_numbers_merged.to_csv(file_path, index=False)  # Save to CSV


def process_phone_numbers(input_file: str, phone_number: str = 'phone_number', output_file: str = 'results'):
    """
    Processes phone numbers by validating them and saving results.

    Args:
        phone_numbers_file (str): Path to the phone numbers file.
    """
    phone_numbers_df = load_phone_numbers_csv(input_file, phone_number)
    phone_numbers = phone_numbers_df['phone_number_str'].unique()
    phone_numbers = [number for number in phone_numbers]
    results = [validate_phone(number) for number in phone_numbers]
    # print(results)

    output_filepath = "output/" + output_file + ".csv"

    save_results_to_csv(results, output_filepath, phone_numbers_df)

    print("Results saved to " + output_filepath)
