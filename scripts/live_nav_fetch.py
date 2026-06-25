import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

schemes = {
    "hdfc_top100":125497,
    "sbi_bluechip":119551,
    "icici_bluechip":120503,
    "nippon_largecap":118632,
    "axis_bluechip":119092,
    "kotak_bluechip":120841
}

for name, code in schemes.items():

    print(f"Downloading {name}")

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        file_path = f"data/raw/{name}.csv"

        nav_df.to_csv(file_path, index=False)

        print(f"Saved {file_path}")

    else:
        print(f"Failed for {name}")