from openpyxl import load_workbook
import json
import sys
from fastapi import UploadFile
import pandas as pd
from io import BytesIO


async def read_xlsx_file(excel_data):
    try:
        # Read with pandas using openpyxl engine
        df = pd.read_excel(BytesIO(excel_data), engine="openpyxl")

        # Convert DataFrame to list of dictionaries
        records = df.to_dict(orient="records")

        return {"data": records}

    except Exception as e:
        return {"error": f"Failed to read Excel file: {str(e)}"}
