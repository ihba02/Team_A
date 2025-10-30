from flask import Flask, jsonify, abort
import os
import json
import csv
import time
import datetime
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

SRC_DIR = os.path.dirname(__file__)


def sanitize_table_name(name: str) -> str:
    # remove extension already removed before calling this, remove trailing (1) style suffixes
    name = re.sub(r"\s*\(\d+\)$", "", name)
    return name.replace(" ", "_")


def list_tables():
    files = []
    for fname in os.listdir(SRC_DIR):
        fpath = os.path.join(SRC_DIR, fname)
        if os.path.isfile(fpath):
            base, ext = os.path.splitext(fname)
            ext = ext.lower()
            if ext in ('.json', '.csv', '.xml'):
                tables_name = sanitize_table_name(base)
                files.append({'file_name': fname, 'table': tables_name, 'ext': ext})
    return files


def file_mtime_iso(path):
    ts = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(ts).isoformat()


def infer_schema_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        # single object — take its keys
        keys = list(data.keys())
        return {k: type(data[k]).__name__ for k in keys}
    elif isinstance(data, list):
        types = {}
        for row in data:
            if isinstance(row, dict):
                for k, v in row.items():
                    if k not in types:
                        types[k] = type(v).__name__
        return types
    else:
        return {}


def infer_schema_csv(path, sample_rows=50):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        types = {fn: None for fn in fieldnames}
        count = 0
        for row in reader:
            for fn in fieldnames:
                val = row.get(fn)
                if val is None or val == '':
                    continue
                # attempt simple type inference
                if types[fn] in (None, 'str'):
                    if val.isdigit():
                        types[fn] = 'int'
                    else:
                        try:
                            float(val)
                            types[fn] = 'float'
                        except Exception:
                            types[fn] = 'str'
            count += 1
            if count >= sample_rows:
                break
        # default to str if unknown
        for fn in fieldnames:
            if types[fn] is None:
                types[fn] = 'str'
        return types


def infer_schema_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    # try to find a representative child that contains fields
    if len(root) == 0:
        # root has no children; schema is the root tag attributes
        return {k: 'str' for k in root.attrib.keys()}
    # pick first child element that has children
    for child in root:
        if len(child) > 0:
            fields = {}
            for f in child:
                fields[f.tag] = 'str'
            return fields
    # fallback: use tags of first child
    first = root[0]
    return {c.tag: 'str' for c in first}


def table_row_count(path, ext):
    if ext == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return len(data)
        return 1
    elif ext == '.csv':
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # count rows excluding header
            cnt = -1
            for _ in reader:
                cnt += 1
            return max(cnt, 0)
    elif ext == '.xml':
        tree = ET.parse(path)
        root = tree.getroot()
        # assume each direct child is a record
        return len(root)
    return 0


@app.route('/tables', methods=['GET'])
def get_tables():
    files = list_tables()
    return jsonify([{'table': f['table'], 'file': f['file_name'], 'ext': f['ext']} for f in files])


@app.route('/tables/<table>/schema', methods=['GET'])
def get_table_schema(table):
    files = list_tables()
    match = None
    for f in files:
        if f['table'] == table:
            match = f
            break
    if not match:
        abort(404, f"table {table} not found")
    path = os.path.join(SRC_DIR, match['file_name'])
    if match['ext'] == '.json':
        schema = infer_schema_json(path)
    elif match['ext'] == '.csv':
        schema = infer_schema_csv(path)
    elif match['ext'] == '.xml':
        schema = infer_schema_xml(path)
    else:
        schema = {}
    return jsonify({'table': table, 'schema': schema})


@app.route('/tables/<table>/status', methods=['GET'])
def get_table_status(table):
    files = list_tables()
    match = None
    for f in files:
        if f['table'] == table:
            match = f
            break
    if not match:
        abort(404, f"table {table} not found")
    path = os.path.join(SRC_DIR, match['file_name'])
    present = os.path.exists(path)
    row_count = table_row_count(path, match['ext']) if present else 0
    size = os.path.getsize(path) if present else 0
    return jsonify({'table': table, 'present': present, 'row_count': row_count, 'size_bytes': size})


@app.route('/tables/<table>/last_updated', methods=['GET'])
def get_table_last_updated(table):
    files = list_tables()
    match = None
    for f in files:
        if f['table'] == table:
            match = f
            break
    if not match:
        abort(404, f"table {table} not found")
    path = os.path.join(SRC_DIR, match['file_name'])
    if not os.path.exists(path):
        abort(404, f"file for table {table} not found")
    return jsonify({'table': table, 'last_updated': file_mtime_iso(path)})


@app.route('/metadata/schemas', methods=['GET'])
def get_all_schemas():
    files = list_tables()
    out = {}
    for f in files:
        path = os.path.join(SRC_DIR, f['file_name'])
        try:
            if f['ext'] == '.json':
                schema = infer_schema_json(path)
            elif f['ext'] == '.csv':
                schema = infer_schema_csv(path)
            elif f['ext'] == '.xml':
                schema = infer_schema_xml(path)
            else:
                schema = {}
        except Exception:
            schema = {}
        out[f['table']] = schema
    return jsonify(out)


@app.route('/metadata/status', methods=['GET'])
def get_all_status():
    files = list_tables()
    out = {}
    for f in files:
        path = os.path.join(SRC_DIR, f['file_name'])
        present = os.path.exists(path)
        row_count = table_row_count(path, f['ext']) if present else 0
        size = os.path.getsize(path) if present else 0
        out[f['table']] = {'present': present, 'row_count': row_count, 'size_bytes': size}
    return jsonify(out)


@app.route('/metadata/last_updated', methods=['GET'])
def get_all_last_updated():
    files = list_tables()
    out = {}
    for f in files:
        path = os.path.join(SRC_DIR, f['file_name'])
        if os.path.exists(path):
            out[f['table']] = file_mtime_iso(path)
        else:
            out[f['table']] = None
    return jsonify(out)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
