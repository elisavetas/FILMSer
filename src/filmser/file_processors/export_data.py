# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Export a DataFrame to one or more file formats."""

import os
from pathlib import Path
from typing import Union, List

import pandas as pd

from src.filmser.config import VALID_OUTPUT_FORMATS


def export_data(df: pd.DataFrame, file_name: str, 
                file_types: Union[str, List[str]] = "tsv") -> None:
    """
    Exports the data into a file with a given format(s).

    Parameters
    ----------
    df : pandas DataFrame
        A dataframe containing the necessary data to export.
    file_name : str
        The name of the file / path to the file to which the data
            will be exported.
    file_types : str or list of str, optional
        The extension(s) of the file to export the data into.
        The available extensions: "txt", "csv", "xlsx", "tsv", "json". 
        The default is "tsv".
        Can be a single string, a list of strings, or a pipe-separated string.
        Examples: "tsv", ["tsv", "xlsx"], or "tsv|xlsx".

    Raises
    ------
    Exception
        If the requested file type is not supported by the function.

    Returns
    -------
    None.

    """
    # Normalize and validate requested file types
    # Convert to list if needed
    if isinstance(file_types, str):
        requested_types = [ft.strip().lower() for ft in file_types.split("|") if ft.strip()]
    elif isinstance(file_types, list):
        requested_types = [ft.strip().lower() for ft in file_types if isinstance(ft, str) and ft.strip()]
    else:
        # Try to iterate over it
        try:
            requested_types = [ft.strip().lower() for ft in file_types if isinstance(ft, str) and ft.strip()]
        except TypeError:
            print(f"Warning: file_types must be a string or list of strings, got {type(file_types).__name__}. Defaulting to 'tsv'.")
            requested_types = ["tsv"]

    # Remove unknown file types and warn the user
    unknown = set(requested_types) - VALID_OUTPUT_FORMATS
    if unknown:
        print(f"Warning: Unsupported file type(s): {', '.join(sorted(unknown))}")
        requested_types = [ft for ft in requested_types if ft in VALID_OUTPUT_FORMATS]
    if not requested_types:
        print("No supported file types specified to export. Defaulting to .tsv")
        requested_types = ["tsv"]

    # Convert list/dict to DataFrame if needed
    if not isinstance(df, pd.DataFrame):
        if isinstance(df, list):
            df = pd.DataFrame(df)
        elif isinstance(df, dict):
            # Handle both column-oriented {col: [vals]} and single record {key: val}
            try:
                df = pd.DataFrame(df)
            except (ValueError, TypeError) as e:
                # Try wrapping as single record only if it looks like a dict record
                try:
                    df = pd.DataFrame([df])
                except (ValueError, TypeError):
                    raise TypeError(f"Could not convert dict to DataFrame: {e}")
        else:
            raise TypeError("df must be a pandas DataFrame, list, or dict")
    
    if df.empty:
        # Avoid writing empty files
        raise ValueError("Cannot export empty DataFrame")

    # Create the folder for the data if it does not exist yet
    directory = Path(file_name).parent
    if directory and str(directory) != ".":
        directory.mkdir(parents=True, exist_ok=True)

    # Dispatch writers per file type
    for file_type in requested_types:
        curr_file_name = f"{file_name}.{file_type}"

        if file_type in {"txt", "tsv"}:
            df.to_csv(curr_file_name, sep="\t", index=False, encoding="utf-8")
        elif file_type == "csv":
            df.to_csv(curr_file_name, sep=",", index=False, encoding="utf-8")
        elif file_type == "json":
            df.to_json(curr_file_name, orient="records", lines=True, force_ascii=False)
        elif file_type == "xlsx":
            # Maximum size possible for excel: 1,048,576 rows, 16,384 cols
            max_rows = 1_048_576 - 1  # -1 for the header
            df.iloc[:max_rows].to_excel(curr_file_name, index=False)

            # Also create a readable version restricted to 100,000 entries if the full file is too big
            cut_entries = 100_000
            if cut_entries < df.shape[0]:
                base_name = os.path.splitext(curr_file_name)[0]
                trimmed_name = f"{base_name}.{cut_entries}.xlsx"
                df.iloc[:cut_entries].to_excel(trimmed_name, index=False)

