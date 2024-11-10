import pandas as pd
import re


def load_data(path):
    return pd.read_excel(path)


def clean_data(df):
    df.replace('', pd.NA, inplace=True)
    df.replace(0, pd.NA, inplace=True)
    return df


def fill_from_date(row):
    from_date = row["pay_from_date"]
    draft_date = row["draft_date"]
    if pd.isna(from_date):
        return draft_date
    return from_date


def fill_id(row):
    id_original = row["id_original"]
    id_rent = row["id_rent"]
    if pd.isna(id_rent):
        return id_original
    return id_rent


def fill_owner(row):
    owner_name_original = row["owner_name_original"]
    owner_name_rent = row["owner_name_rent"]
    if pd.isna(owner_name_rent):
        return owner_name_original
    return owner_name_rent


def to_date(timestamp):
    if pd.isna(timestamp):
        return pd.NA
    return timestamp.date()

def clean_license(license):
    s = str(license)
    digits = re.search(r"[0-9]+", s)
    if digits:
        return int(digits.group())
    else:
        return pd.NA


def orgenize_cols(df, cols_index, cols_translate):
    columns = {}
    for i, col in enumerate(df.columns):
        if (i + 1) in cols_index.values():
            columns[col] = i + 1
    reverse_cols_index = {v: k for k, v in cols_index.items()}
    index_to_name = {}
    for k, v in reverse_cols_index.items():
        index_to_name[k] = cols_translate[v]
    tranlate = {}
    for k, v in columns.items():
        tranlate[k] = index_to_name[v]
    df = df[columns.keys()]
    df = df.rename(columns=tranlate)
    return df


def prepare_data(df, cols_index, cols_translate):
    df = orgenize_cols(df, cols_index, cols_translate)
    
    df = df[df["misgeret"] == 'יצא']
    df = clean_data(df)

    df["license"] = df["license"].apply(clean_license)

    date_columns = [col for col in df.columns if "date" in col]
    for c in date_columns:
        df[c] = df[c].apply(to_date)
    df["pay_from_date"] = df.apply(fill_from_date, axis=1)
    df["id"] = df.apply(fill_id, axis=1)

    df["owner_name"] = df.apply(fill_owner, axis=1)

    return df