import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

engine = create_engine(f"sqlite:///staging")

file_path =r"C:\Users\aayus\Downloads\Py_project\Team_A\src\plant_hierarchy (1).xml"

def read_file(file_path):
       if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
       ext = os.path.splitext(file_path)[1].lower()
       try:
           if ext == '.csv':
            df = pd.read_csv(file_path)
            df.to_sql('staging.Asset_performance', con=engine, if_exists='replace', index=False)
           elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Convert JSON data to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
                df.to_sql('staging.Asset_Metadata', con=engine, if_exists='replace', index=False)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
                df.to_sql('staging.Asset_Metadata', con=engine, if_exists='replace', index=False)
            else:
                raise ValueError("Unsupported JSON structure")
           elif ext == '.xml':
            tree = ET.parse(file_path)
            root = tree.getroot()
            rows = []
            for child in root:
                record = {elem.tag: elem.text for elem in child}
                rows.append(record)
            df = pd.DataFrame(rows)
            df.to_sql('staging.Plant_hierarchy', con=engine, if_exists='replace', index=False)
        
           else:
            raise ValueError(f"Unsupported file format: {ext}")
        
          
       except Exception as e:
        raise RuntimeError(f"Error reading {file_path}: {e}")

read_file(file_path)