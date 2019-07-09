import io
import zipfile

import pandas as pd
import requests


def load_zipped_csv_file_from_url(zip_file_url, header_row_number):
    r = requests.get(zip_file_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    with z.open(z.namelist()[0], 'r') as csvfile:
        df = pd.read_csv(csvfile, header=header_row_number)
    return df
