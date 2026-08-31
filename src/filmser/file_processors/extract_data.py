# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva
"""Extract text lines from a gzipped file."""

import gzip
from pathlib import Path
from typing import List, Union


def extract_from_gz(gz_file: Union[str, Path]) -> List[str]:
    """
    Read all lines from a .gz text file using UTF-8 decoding.

    Parameters
    ----------
    gz_file : str or Path
        Path to the gzipped text file.

    Returns
    -------
    list[str]
        Lines from the file (newline characters preserved).
    """
    gz_path = Path(gz_file)
    if not gz_path.exists():
        raise FileNotFoundError(f"File not found: {gz_path}")

    with gzip.open(gz_path, mode="rt", encoding="utf-8", errors="strict") as f:
        return f.readlines()
