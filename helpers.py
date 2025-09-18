import os.path

import pandas as pd


def parse_uploaded_file(file):
    """
    Recieves an uploaded file from Streamlit (st.file_updater)
    and returns a Dataframe if the file was processed.
    In any other case, it will return None
    :param file:
    :return:
    """
    filename = file.name
    extension = os.path.splitext(filename)[1].lower()

    try:
         if extension == ".csv":
             try:
                 df = pd.read_csv(file, sep=None, engine="python")
                 return df, None
             except Exception:
                 return None, f"Couldn't match the separator automatically"

         elif extension in [".xls", ".xlsx"]:
                df = pd.read_excel(file)
                return df, None
         else:
             return None, f"{extension} is currently unsupported."
    except Exception as e:
        return None, f"Sorry, your file contains some feature that is currently unsupported."

