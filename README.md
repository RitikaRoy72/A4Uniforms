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

# Project Updates Log: 
https://docs.google.com/document/d/1XySOlcomjNhRcHuvFETMcPWZkMtwsbMxRUwVOSrEWCE/edit?tab=t.0
### Dec 29
*Estimated Total Time: 3 hours*
* Goal 1: Updated README.md
    * Added a bug section
    * Fixed project tree display
    * Added a deployment section
* Goal 2: Reading documentation
    * Determine a software for deploying the app:
    * Render: https://render.com/
    * Railway: https://railway.com/enterprise?gad_source=1&gad_campaignid=23229512525&gbraid=0AAAABBOsx_otSKo3KEMz-vIqqZtXSKteG&gclid=Cj0KCQiA6sjKBhCSARIsAJvYcpNx5RKGO_hkBoyQpsEY0Y347O5uXYgrXOadMXINQ66Uqwebp-dpY2UaAlodEALw_wcB
    * Heroku: https://devcenter.heroku.com/categories/deployment

### Dec 28
*Estimated Total Time: 10 hours*
* Goal 1: Finish user interface
    * Wrote html user interaction
* Goal 2: Create back end routers
    * Used flask.App to route every pipeline from user interaction to python process
* Goal 3: Correct data base handling
* Goal 4: Start debugging
* ToDo: Fix error in Uniform requests

### Dec 24
*Estimated Total Time: 8 hours*
* Goal 1: Implement FLASK
    * Used the following resources:
        * https://www.geeksforgeeks.org/installation-guide/how-to-install-flask-in-windows/
        * https://python-adv-web-apps.readthedocs.io/en/latest/flask.html
        * https://www.python.org/downloads/release/python-3142/
        * https://www.geeksforgeeks.org/python/python-pip/
* Goal 2: Create basic working architecture of program
    * Created flaskAPP.py backend in python
    * Created index.html front end for
    * Created css and js for handling of user interface interactions

### Dec 23
*Estimated Total Time: 4 hour*
* Goal 1: Program Architecture
    * Designed a program architecture
    * Created Project outline
    * Share project outline
* Goal 2: Develop Read Me Doc
    * All documents uploaded to gitHub: https://github.com/RitikaRoy72/A4Uniforms



# Contributing
Contributions are welcome! Feel free to submit pull requests for bug fixes, enhancements, or additional features.

# Bugs
* Uniforms requests and displays
* Adding a reset button to the display tab
* testing and validation of file upload
