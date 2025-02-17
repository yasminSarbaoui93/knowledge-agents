import requests
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

input_folder = "../../data/"

authorization = os.environ["KM_SERVICE_AUTHORIZATION"]
km_service_url = os.environ["KM_SERVICE_URL"]

file_metadata = [
    {
        "file1": "MDr_br141011_SR 0643_2.pdf",
        "subject": "Determination of the Tensile Behaviour and Poissons Ratio of Terophon HDF 6170 V524.",
        "tags": ["type:report", "year:2011"]
    },
    {
        "file2": "CMMT256.pdf",
        "subject": "Committee Draft for an ISO Guide to the Acquisition and Presentation of Design Data for Plastics",
        "tags": ["type:report", "year:2000"]
    },
    {
        "file3": "D412-16(2021).pdf",
        "subject": "Standard Test Methods for Vulcanized Rubber and Thermoplastic Elastomers—Tension",
        "tags": ["type:report", "year:2021"]
    },
    {
        "file4": "D638-22.pdf",
        "subject": "Standard Test Method for Tensile Properties of Plastics",
        "tags": ["type:report", "year:2022"]
    },
    {
        "file5": "DEPC_MPR7.pdf",
        "subject": "Determination of Material Properties and Parameters Required for the Simulation of Impact Performance of Plastics Using Finite Element Analysis",
        "tags": ["type:report", "year:2004"]
    },
    {
        "file6": "DIN EN ISO 472_2013.pdf",
        "subject": "Kunststoffe-Fachwörterverzeichnis (ISO 472:2013); Dreisprachige Fassung EN ISO 472:2013",
        "tags": ["type:DIN", "year:2019"]
    },
    {
        "file7": "DIN EN ISO 527-3.pdf",
        "subject": "DEUTSCHE NORM Kunststoffe Bestimmung der Zugeigenschaften Teil 3: Prüfbedingungen für Folien und Tafeln (ISO 527-3:1995 + Corr 1:1998 + Corr 2:2001)",
        "tags": ["type:DIN", "year:2003"]
    },
    {
        "file8": "Iso 37.pdf",
        "subject": "Rubber, vulcanized or thermoplastic — Determination of tensile stress-strain properties",
        "tags": ["type:ISO", "year:2005"]
    },
    {
        "file9": "ISO 527-1_2012-02.pdf",
        "subject": "Plastics — Determination of tensile properties — Part 1: General principles",
        "tags": ["type:ISO", "year:2012"]
    },
    {
        "file10": "ISO 527-2_2012-02.pdf",
        "subject": "Plastics — Determination of tensile properties — Part 2: Test conditions for moulding and extrusion plastics",
        "tags": ["type:ISO", "year:2012"]
    },
]


index = 0
max_index = len(file_metadata) - 1

for index in range(max_index):
    file_id = "file" + str(index + 1)
    files = {
        file_id: (file_metadata[index][file_id], open(input_folder + file_metadata[index][file_id], "rb")),
    }

    # Tags to apply, used by queries to filter memory
    data = { "documentId": file_metadata[index][file_id],
             "tags": file_metadata[index]["tags"],
              "subject": file_metadata[index]["subject"],
           }

    headers = {'Authorization': authorization}

    print ("Posting file: " + file_metadata[index][file_id])
    response = requests.post(f"{km_service_url}/upload", files=files, data=data, headers=headers)
    print(response.status_code)
    print(response)
    time.sleep(20)
