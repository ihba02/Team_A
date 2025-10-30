import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
#engine = create_engine('sqlite:///staging')
#df = pd.read_sql_table('staging.ingestion_log', con=engine)

file_path  = r"C:\Users\aayus\Downloads\Py_project\Team_A\src\plant_hierarchy (1).xml"

tree = ET.parse(file_path)
root = tree.getroot()
rows = []
for parent in root:
    # Start with parent attributes (like Plant name="PlantA")
    record = {}
    # Add parent attributes as columns
    for attr_key, attr_value in parent.attrib.items():
        record[f"{parent.tag}_{attr_key}"] = attr_value

    # Add child elements as columns
    for elem in parent:
        record[elem.tag] = elem.text

    rows.append(record)
df = pd.DataFrame(rows)
table_name = 'staging.Plant_hierarchy'

print(df)

