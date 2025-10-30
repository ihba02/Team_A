import os
import pandas as pd
import json
import xml.etree.ElementTree as ET

file_path =""

if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    