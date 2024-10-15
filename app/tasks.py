import os

import pandas as pd
import requests

from celery import shared_task


def rename(data: str):
    """rename to camelCase"""
    names = data.lower().split(" ")
    # print("------------------------")
    # print(names)
    if len(names) > 1:
        name = names[0] + "".join([x[0].upper() + x[1:] for x in names[1:]])
        return validate_column(name)
    return names[0]


def validate_column(column: str):
    if "organizationName" in column or "companyName" in column:
        return "company"
    return column


# @shared_task
def read_file(file_path: str):
    _, ext = os.path.splitext(file_path)
    if ext not in [".csv", ".xlsx"]:
        return {"message": "File must be Spreadsheet readable", "status": False}

    df = None
    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)
    if file_path.lower().endswith(".xls"):
        df = pd.read_excel(file_path)
    if file_path.lower().endswith(".xlsx"):
        df = pd.read_excel(file_path, engine="xlrd")

    if df is not None:
        columns = [rename(column) for column in df.columns]
        df.columns = columns
        # check for names
        if "fullName" in df.columns or "name" in df.columns:
            df[["firstName", "lastName"]] = df["fullName"].apply(
                lambda x: pd.Series(x.split(" ", 1))
            )
            df = df.drop("fullName", axis=1)

        # check for index column
        if "unnamed:0" in df.columns:
            df = df.drop(columns=["unnamed:0"])

        l = []

        for m in df.to_dict(orient="records"):
            l.append(get_practitioner(m))
        return l

    return {"message": "No data in the file", "status": False}


def get_practitioner(hco):
    practitionals = []
    d = {}
    for p in list(hco.keys()):
        if "practitioner" in p:
            a = p.replace("practitioner", "")
            a = a[0].lower() + a[1:]
            d[a] = hco[p]
            hco.pop(p)

    practitionals.append(d)
    hco["practitioners"] = practitionals
    return hco


@shared_task
def on_board_hco(templateUrl, companyId, managerId):
    data = {}
    # 1. read or download the file from url

    xlsx_file = requests.get(templateUrl)
    from pathlib import Path

    with open("excel_file.xlsx", "wb") as f:
        f.write(xlsx_file.content)

    # save for reading
    # xlsx_file.save(file_path)

    result = read_file(f"/app/excel_file.xlsx")
    # clean up

    os.remove("/app/excel_file.xlsx")

    data["companyId"] = companyId
    data["managerId"] = managerId
    data["data"] = result

    print("My data::::::::::", data)
    return data
    # import json

    # with open("new.json", "w") as f:
    #     json.dump(data, f, indent=4)

    # 2. load it to memory
    # 3. process the data
    # 4. send the response to the backend webhook


# on_board_hco("hco.xlsx", "12345", "67890")
