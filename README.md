# A4Uniforms
Maintain Uniforms Division Data Det 520

# Purpose
- Convert legacy Google Sheets into a standardized “Teams-style” spreadsheet format
- Centralized inventory management
- Accountability (who has what, when it was issued, condition)
- Easy access for cadets + cadre
- Auditability

# Timeline
- Debug the request uniform items

# Stack
Frontend: HTML + CSS 
Backend: Python (Flask)
Database: SQLite → PostgreSQL
Auth: Flask-Login
Deployment: Render / Railway

# Architecture
Browser → Route → Importer → Models → Database

* Project Tree * 
A4Uniforms/
│
├── excel_parsers.py
├── flaskApp.py
├── models.py
├── README.md
│
├── importers/
│   ├── cadet_import.py
│   └── supply_import.py
│
├── data/
│   ├── AllInventoryData.xlxs
│   ├── det520.png
│   └── uniform_requests.csv
│
├── templates/
│   ├── home.html
│   ├── upload.html
│   ├── cadets.html
│   ├── inventory.html
│   ├── approve.html
│   └── requests.html
│
├── static/
│   ├── styles.css
│   └── images
│        └── det520.png