# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Export data into a certain format.
"""

import os


def export_data(df, file_name, file_types="txt"):
    """
    Exports the data into a file with a given format(s).

    Parameters
    ----------
    df : pandas DataFrame
        A dataframe containing the necessary data to export.
    file_name : str
        The name of the file / path to the file to which the data
            will be exported.
    file_types : str, optional
        The extension of the file to export the data into.
        The available extensions: "txt","csv", "xlsx", "tsv". 
        The default is "txt".
        To export data into more than one file type, use | to separate
           extensions.
        Example: "txt|xlsx".

    Raises
    ------
    Exception
        If the requested file type is not supported by the function.

    Returns
    -------
    None.

    """
    # Create the folder for the data if it does not exist yet
    split_path = file_name.split("/")
    directory = "/".join(split_path[:-1])
        
    dir_level = 1
        
    while not os.path.exists(directory) and directory:
        dir_level += 1
        directory = "/".join(split_path[:-dir_level])
        
    while dir_level > 1:
        dir_level -= 1
        directory = "/".join(split_path[:-dir_level])
        os.mkdir(directory)
    
    # Create the file(s) with the required extension
    for file_type in file_types.split("|"):
        curr_file_name = f"{file_name}.{file_type}"
        
        if file_type == "txt" or file_type == "tsv":
            df.to_csv(curr_file_name, sep='\t', index=False,
                      encoding="utf-8")
        
        elif file_type == "csv":
            df.to_csv(curr_file_name, sep=',', index=False,
                      encoding="utf-8")
        
        elif file_type == "xlsx":
            # Maximum size possible for excel: 1,048,576 rows, 16,384 cols
            max_rows = 1048576
            df[:max_rows].to_excel(curr_file_name, index=False)
            
            # Also create a readable version restricted to 100,000 entries
            # if the full file is too big
            cut_entries = 100000
            if cut_entries < df.shape[0]:
                curr_file_name = f"{".".join(curr_file_name.split(".")[:-1])}.{cut_entries}.xlsx"
                df[:cut_entries].to_excel(curr_file_name, index=False)
        
        else:
            raise Exception(f"Unsupported file type {file_type}.")
    
