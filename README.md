# A4Uniforms
Maintain Uniforms Division Data Det 520

# Purpose
A4Uniforms is designed to streamline and modernize the management of uniform inventories for cadet units. The app helps with:
- Convert legacy Google Sheets into a standardized “Teams-style” spreadsheet format
- Centralized inventory management
- Accountability (who has what, when it was issued, condition)
- Easy access for cadets + cadre
- Auditability

# Features
- Import cadet and supply data from Excel/CSV files.
- View and manage cadet and inventory records.
- Approve uniform requests directly through the app.
- Maintain a searchable, centralized database of all uniforms and associated information.

# Usage
- Clone the repository: git clone https://github.com/RitikaRoy72/A4Uniforms.git
- Install dependencies: pip install -r requirements.txt
- Run the Flask App: python flaskApp.py

# Stack
Frontend: HTML + CSS 
Backend: Python (Flask)
Database: SQLite → PostgreSQL
Auth: Flask-Login
Deployment: Render / Railway

# Architecture
Browser → Route → Importer → Models → Database

* Project Tree * <br>
A4Uniforms/ <br>
│ <br>
├── excel_parsers.py <br>
├── flaskApp.py <br>
├── models.py <br>
├── README.md <br>
│ <br>
├── importers/ <br>
│   ├── cadet_import.py <br>
│   └── supply_import.py <br>
│ <br>
├── data/ <br>
│   ├── AllInventoryData.xlxs <br>
│   ├── det520.png <br>
│   └── uniform_requests.csv <br>
│ <br>
├── templates/ <br>
│   ├── home.html <br>
│   ├── upload.html <br>
│   ├── cadets.html <br>
│   ├── inventory.html <br>
│   ├── approve.html <br>
│   └── requests.html <br>
│
├── static/ <br>
│   ├── styles.css <br>
│   └── images <br>
│        └── det520.png <br>

# Contributing
Contributions are welcome! Feel free to submit pull requests for bug fixes, enhancements, or additional features.
