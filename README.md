# A4Uniforms
Maintain Uniforms Division Data Det 520

# Purpose
- Convert legacy Google Sheets into a standardized “Teams-style” spreadsheet format
- Centralized inventory management
- Accountability (who has what, when it was issued, condition)
- Easy access for cadets + cadre
- Auditability

# Timeline
- 22 Dec: Git Repo and Planning
- 23 Dec: Project details
- 26 Dec: PT1 Core
  - Flask app
  - Database models
  - Inventory CRUD
  - Issue / return logic
- 31 Dec: PT2
  - CSV upload
  - Mapping UI
  - Validation
- 5 Jan: PT3 Debugging and Polish
  - Permissions
  - UI cleanup
  - Deployment

# Stack
Frontend: HTML + CSS + JavaScript
Backend: Python (Flask)
Database: SQLite → PostgreSQL
Auth: Flask-Login
Deployment: Render / Railway

# Architecture
Browser (Web App)
   |
   | HTTP Requests
   v
Flask Backend (API)
   |
   | ORM (SQLAlchemy)
   v
PostgreSQL Database

# Program Structure
A4Uniforms/
│
├── flaskApp.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── inventory.html
│
├── static/
│   ├── hello.js
│   └── styles.css
│
└── myenv/

# Table
* Cadets *
first_name
last_name
class_year
rank
email

* Uniforms *
type: PTG, OCP, BLUE
item_type (ex. OCP Pants, Boots)
size
serial_number
condition (New / Good / Worn / Damaged)
status (In Stock / Issued / Lost)

* Issuance Log *
cadet rank
cadet first name
cadet last name
cadet email
uniform_item_id 
issued_date
returned_date
issued_by
condition_out
condition_in

* Legacy Imports *
id (PK)
source_file
import_date
rows_imported
status

* Old Sheet Column → New Field *
"Cadet Name"     → cadet_name
"Uniform Size"   → size
"Item Type"      → item_type

# A4Uniforms
Maintain Uniforms Division Data Det 520

# Purpose
- Convert legacy Google Sheets into a standardized “Teams-style” spreadsheet format
- Centralized inventory management
- Accountability (who has what, when it was issued, condition)
- Easy access for cadets + cadre
- Auditability

# Timeline
- 22 Dec: Git Repo and Planning
- 23 Dec: Project details
- 26 Dec: PT1 Core
  - Flask app
  - Database models
  - Inventory CRUD
  - Issue / return logic
- 31 Dec: PT2
  - CSV upload
  - Mapping UI
  - Validation
- 5 Jan: PT3 Debugging and Polish
  - Permissions
  - UI cleanup
  - Deployment

# Stack
Frontend: HTML + CSS + JavaScript
Backend: Python (Flask)
Database: SQLite → PostgreSQL
Auth: Flask-Login
Deployment: Render / Railway

# Architecture
Browser (Web App)
   |
   | HTTP Requests
   v
Flask Backend (API)
   |
   | ORM (SQLAlchemy)
   v
PostgreSQL Database

# Table
* Cadets *
first_name
last_name
class_year
rank
email

* Uniforms *
type: PTG, OCP, BLUE
item_type (ex. OCP Pants, Boots)
size
serial_number
condition (New / Good / Worn / Damaged)
status (In Stock / Issued / Lost)

* Issuance Log *
cadet rank
cadet first name
cadet last name
cadet email
uniform_item_id 
issued_date
returned_date
issued_by
condition_out
condition_in

* Legacy Imports *
id (PK)
source_file
import_date
rows_imported
status

* Old Sheet Column → New Field *
"Cadet Name"     → cadet_name
"Uniform Size"   → size
"Item Type"      → item_type
