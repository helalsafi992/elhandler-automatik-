import boto3
import pandas as pd
from datetime import datetime

# AWS S3 settings
AWS_ACCESS_KEY = "AKIASVVAGJVE4D537KVL"
AWS_SECRET_KEY = "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"
BUCKET_NAME = "elhandler"
REGION = "eu-north-1"
LOCAL_FILENAME = "05-08-2025.xlsx"

def get_forecast():
    # Forbind til S3 og hent nyeste fil
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION
    )

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    objects = response.get("Contents", [])
    if not objects:
        raise Exception("Ingen filer i bucket.")

    # Find nyeste fil
    nyeste = max(objects, key=lambda x: x["LastModified"])
    s3.download_file(BUCKET_NAME, nyeste["Key"], LOCAL_FILENAME)

    # Læs filen som dataframe
    df = pd.read_excel(LOCAL_FILENAME)
    return df

def find_best_trade(df):
    best = {"spread": 0, "buy_hour": None, "sell_hour": None}

    for buy_hour in range(24):
        for sell_hour in range(buy_hour + 1, 24):
            spread = df.loc[sell_hour, "ResidualLoad"] - df.loc[buy_hour, "ResidualLoad"]

            if spread > best["spread"]:
                best["spread"] = round(spread, 2)
                best["buy_hour"] = int(buy_hour)
                best["sell_hour"] = int(sell_hour)

    if best["spread"] >= 50:
        return best
    return None

def run_model():
    df = get_forecast()
    result = find_best_trade(df)
    return result
