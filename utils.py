import calendar
import datetime
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


def yymm2yymmdd_lastdayofmonth(yymm):
    yymm = str(yymm)
    year_ = int(yymm[:4])
    month_ = int(yymm[4:6])
    date_ = calendar.monthrange(year_, month_)[1]
    return datetime.datetime(year_, month_, date_)


def process_ff5_df(df):
    ff5 = df.copy()
    ff5.rename(columns={'Unnamed: 0': 'YYMM'}, inplace=True)
    yymm = str(ff5['YYMM'].iloc[0])
    if len(yymm) == 6:
        ff5['YYMM'] = ff5['YYMM'].apply(yymm2yymmdd_lastdayofmonth)

    elif len(str(ff5['YYMM'].iloc[0])) == 8:
        ff5['YYMM'] = pd.to_datetime(ff5['YYMM'], yearfirst=True,
                                     format='%Y%m%d')

    ff5.index = ff5['YYMM']
    if 'RF' in df.columns:
        ff5 = ff5.drop('RF', axis=1)

    if '<= 0' in df.columns:
        ff5 = ff5.drop('<= 0', axis=1)

    ff5 = ff5.drop('YYMM', axis=1)
    return ff5
