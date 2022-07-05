"""
Author: Greta Heng and Sheetal Prasad
Created On: 3 June 2022
Subject: Data Preparation for Open Refine with Qnum and LC data.
"""

import pandas as pd
import requests
import numpy as np


def change_name_LC(name):
    namel = name.strip().split(" ")

    if len(namel) == 1:
        rn = name
    elif len(namel) == 2:
        rn = namel[1].strip() + ", " + namel[0].strip()
    else:
        rnpre = [i.strip() for i in namel]
        rnpre2 = (" ").join(rnpre[1:-1])
        rn = rnpre[-1] + ", " + rnpre[0] + " " + rnpre2
    return rn


def dataPrep(basePath, filename, collegeQnum, fieldQnum, departmentQnum, websiteBaseUrl, allOnePage):
    filepath = basePath + filename
    file_name = filepath

    filename = filename[:len(filename) - 4]

    # df = pd.read_csv(file_name,encoding='latin-1')
    df = pd.read_csv(file_name)
    print("Total records in original file: ", len(df))

    df = df.drop(columns=['Unnamed: 0', 'research.interests', 'title'])
    df["FacultyNameForLC"] = np.nan
    df["LCnum"] = np.nan
    df["web"] = np.nan

    # CHANGE COLLEGE QNUM
    df["Qcol"] = collegeQnum  # CAL

    df["FieldQnum"] = fieldQnum

    df["Qdept"] = departmentQnum

    df = df.rename({'faculty.name': 'FacultyNameForWiki'}, axis=1)

    df["FacultyNameForLC"] = df["FacultyNameForLC"].astype(str)
    df["LCnum"] = df["LCnum"].astype(str)
    df["web"] = df["web"].astype(str)


    df1 = df.copy()
    for i, r in df.iterrows():
        namelc = change_name_LC(r["FacultyNameForWiki"])
        if r["LCnum"] == "nan":
            df1.at[i, "FacultyNameForLC"] = str(namelc)
            response = requests.get("https://id.loc.gov/authorities/names/suggest/?q=" + namelc)
            data = response.json()
            if len(data[-1]) > 0:
                df1.at[i, "LCnum"] = data[-1]
            else:
                df1.at[i, "LCnum"] = np.nan

        # some departments have only 1 page with all faculty bios
        if allOnePage:
            df1.at[i, "web"] = websiteBaseUrl
        else:
            if 'tenure' in file_name:
                website = websiteBaseUrl + namelc.split(",")[0].strip()
                response = requests.get(website)
                status = response.status_code
                if status == 200:
                    df1.at[i, "web"] = website

        # When no school is present, bot does not add degree to wikidata. Overload for open refine. Hence removed
        if df1.at[i, "education.school"] == '':
            df1.at[i, "education.degree"] = ''

    # CHANGE FILEPATH AND FILENAME
    df1.to_csv(basePath + filename + "_ready4or.csv", encoding="utf8")

    print("Total records in new file: ", len(df1))

def runDataPrepForForm(basePath, filename, collegeQnum, fieldQnum, departmentQnum, websiteBaseUrl, allOnePage):
    response = ''

    try:
        dataPrep(basePath, filename, collegeQnum, fieldQnum, departmentQnum, websiteBaseUrl, allOnePage)
    except BaseException as error:
        response = 'FAIL: An error occurred: {}'.format(error)

    if response == '':
        response = 'SUCCESS: Data preparation completed. New csv file \"ready4or\" ready for refining .'

    return response
