from flask import Flask, render_template, request, redirect, url_for
from models import db, Cadet, IssuedUniform, SupplyInventory, UniformRequest, UniformType
from importers.cadet_import import import_cadet_sheet
from importers.supply_import import import_supply_sheet
import os
import csv
from datetime import datetime
from excel_parsers import load_cadet_excel, clean_uniform_name
import shutil
from datetime import datetime
import openpyxl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///uniforms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")


UPLOAD_TARGETS = {
    "cadets_blues": "cadet_data/CadetData_Blues.xlsx",
    "cadets_ocp": "cadet_data/CadetData_OCP.xlsx",
    "cadets_ptg": "cadet_data/CadetData_PTG.xlsx",
    "inventory": "data/AllInventoryData.xlsx",
}
from werkzeug.utils import secure_filename

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        target_key = request.form.get("target")

        if not file or not target_key:
            return "Missing file or target", 400

        if target_key not in UPLOAD_TARGETS:
            return "Invalid target", 400

        target_path = UPLOAD_TARGETS[target_key]

        # Ensure folders exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        filename = secure_filename(file.filename)

        # Optional: enforce Excel only
        if not filename.lower().endswith((".xlsx", ".xls")):
            return "Only Excel files allowed", 400

        target_path = UPLOAD_TARGETS[target_key]

        # Overwrite the target file
        file.save(target_path)

        return render_template(
            "upload.html",
            message="File uploaded successfully."
        )

    return render_template("upload.html")




@app.route("/cadets")
def cadet():
    cadet_data = {}

    for filename in os.listdir("cadet_data"):
        if not filename.endswith(".xlsx"):
            continue

        category = filename.replace("CadetData_", "").replace(".xlsx", "")
        filepath = os.path.join("cadet_data", filename)

        cadet_data[category] = load_cadet_excel(filepath)

    return render_template("cadets.html", cadet_data=cadet_data)



@app.route("/inventory")
def inventory():
    inventory_data = load_inventory_excel("data/AllInventoryData.xlsx")
    return render_template("inventory.html", inventory_data=inventory_data)

def load_inventory_excel(filepath):
    wb = openpyxl.load_workbook(filepath)
    data = {}

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = []

        empty_streak = 0
        MAX_EMPTY = 4

        for row in ws.iter_rows(values_only=True):

            # Completely empty row
            if not any(row):
                empty_streak += 1

                if empty_streak >= MAX_EMPTY:
                    break   # STOP reading this sheet

                rows.append({"type": "break"})
                continue

            empty_streak = 0

            # Column B header
            if row[1] and not any(row[2:]):
                rows.append({
                    "type": "section",
                    "title": row[1]
                })
            else:
                rows.append({
                    "type": "data",
                    "cells": list(row)
                })

        data[sheet_name] = rows

    return data


REQUESTS_FILE = "data/uniform_requests.csv"
os.makedirs(os.path.dirname(REQUESTS_FILE), exist_ok=True)
@app.route("/requests", methods=["GET", "POST"])
def requests_page():
    if request.method == "POST":
        os.makedirs(os.path.dirname(REQUESTS_FILE), exist_ok=True)

        row = {
            "timestamp": datetime.now().isoformat(),
            "first_name": request.form.get("first_name", ""),
            "last_name": request.form.get("last_name", ""),
            "rank": request.form.get("rank", ""),
            "uniform_type": request.form.get("uniform_type", ""),
            "uniform_item": request.form.get("uniform_item", ""),
            "size": request.form.get("size", ""),
            "reason": request.form.get("reason", ""),
            "status": "PENDING"
        }

        file_exists = os.path.exists(REQUESTS_FILE)

        with open(REQUESTS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        return redirect(url_for("requests_page"))

    return render_template("requests.html")

CSV_FILE = "data/uniform_requests.csv"
@app.route("/approve", methods=["GET", "POST"])
def approve_requests():

    if request.method == "POST":
        if request.form.get("reset") == "reset":
            with open(CSV_FILE, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)

            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

            return redirect(url_for("approve_requests"))

    with open(CSV_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        requests = list(reader)

    return render_template("approve.html", requests=requests)


if __name__ == "__main__":
    app.run(debug=True)
