import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

engine = create_engine(f"sqlite:///staging")

file_path =r"C:\Users\aayus\Downloads\Py_project\Team_A\src\asset_performance.csv"

def read_file(file_path):
       if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
       ext = os.path.splitext(file_path)[1].lower()
       try:
           if ext == '.csv':
            df = pd.read_csv(file_path)
            df.to_sql('staging.Asset_performance', con=engine, if_exists='replace', index=False)
       except Exception as e:
        raise RuntimeError(f"Error reading {file_path}: {e}")

read_file(file_path)