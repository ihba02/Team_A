import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine(f"sqlite:///staging")
file_name = "asset_performance.csv"
# Get the directory where the script is located



def log_stg_ingestion(file_name, table_name, row_count, status, message):
    """Logs the ingestion details to the log table."""
    log_data = pd.DataFrame([{
        "file_name": file_name,
        "table_name": table_name,
        "row_count": row_count,
        "status": status,
        "message": message,
        "load_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    # Append log to log table
    log_data.to_sql("staging.ingestion_log", con=engine, if_exists="append", index=False)

def read_file(file_name):
       current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to the data file relative to the script location
       file_path = os.path.join(current_dir, "..", "src", file_name)
       if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
       ext = os.path.splitext(file_path)[1].lower()
       try:
           if ext == '.csv':
            df = pd.read_csv(file_path)
            table_name = 'staging.Asset_performance'
            
           elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Convert JSON data to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
                table_name = 'staging.Asset_Metadata'
                
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
                table_name = 'staging.Asset_Metadata'
                
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
            table_name = 'staging.Plant_hierarchy'
            
           else:
            raise ValueError(f"Unsupported file format: {ext}")
           
           df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        # Log success
           log_stg_ingestion(file_name, table_name, len(df), "SUCCESS", "Data loaded successfully")

           print(f"✅ {file_name} loaded to {table_name} ({len(df)} records).")
        
          
       except Exception as e:
        raise RuntimeError(f"Error reading {file_path}: {e}")

read_file(file_name)