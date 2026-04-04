# A4Uniforms
Maintain Uniforms Division Data — Det 520

## Purpose
A4Uniforms is designed to streamline and modernize the management of uniform inventories for cadet units. The app helps with:

- Convert legacy Google Sheets into a standardized spreadsheet format
- Centralized inventory management
- Accountability (who has what, when it was issued, condition)
- Easy access for cadets + cadre
- Auditability

## Features
- Import cadet and supply data from Excel files (Blues, OCP, PTG)
- Full admin master roster with inline editable fields — status, gender, sizing, and qty all editable directly in the table
- Cadet login portal — cadets can view and update their own uniform data
- Admin controls: add cadet, delete cadet, resolve uniform requests
- Approve uniform requests directly through the app
- Download current Excel data files (Blues, OCP, PTG, All Supply Data) directly from the admin panel
- Maintain a searchable, centralized database of all uniforms
- Password reset via email (flask-mail)
- First-time registration flow for new cadets

## Usage
1. Clone the repository: `git clone https://github.com/RitikaRoy72/A4Uniforms.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables (see below)
4. Run the Flask app: `python flaskApp.py`

## Environment Variables
| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask session secret | `dev-secret-change-in-prod` |
| `ADMIN_USERNAME` | Admin login username | `admin` |
| `ADMIN_PASSWORD` | Admin login password | `` |

> **Note:** Always set `ADMIN_PASSWORD` via environment variable before deploying to production.

## Stack
- **Frontend:** HTML + CSS + Vanilla JS
- **Backend:** Python (Flask)
- **Database:** SQLite (→ PostgreSQL planned)
- **Auth:** Session-based with bcrypt password hashing
- **Excel I/O:** openpyxl
- **Email:** Flask-Mail
- **Deployment:** Render / Railway (planned)

## Architecture
```
Browser → Flask Route → Excel Parser / Auth → Models → SQLite DB
                     ↘ CSV (uniform requests)
```

## Project Tree
```
A4Uniforms/
│
├── flaskApp.py              # Main Flask app and all routes
├── excel_parsers.py         # Parses cadet Excel files into structured data
├── inventory_parser.py      # Parses AllInventoryData.xlsx
├── models.py                # SQLAlchemy models
├── auth.py                  # Registration, login, password reset
├── mailer.py                # Flask-Mail integration
├── README.md
│
├── cadet_data/
│   ├── CadetData_Blues.xlsx
│   ├── CadetData_OCP.xlsx
│   └── CadetData_PTG.xlsx
│
├── data/
│   ├── AllInventoryData.xlsx
│   └── uniform_requests.csv
│
├── templates/
│   ├── cadets.html          # Main portal (login, cadet view, admin view)
│   ├── upload.html
│   ├── inventory.html
│   ├── approve.html
│   ├── requests.html
│   ├── register.html
│   ├── forgot.html
│   └── reset.html
│
└── static/
    └── images/
        └── det520.png
```

## Future Plans
- Cadet sizing profiles — store each cadet's measurements and automatically match them to available uniform sizes in inventory
- PostgreSQL migration for production deployment
- Email notifications to cadets for semester uniform updates
- Inventory editing directly in inventory.html

---

## Project Updates Log
Full log: https://docs.google.com/document/d/1XySOlcomjNhRcHuvFETMcPWZkMtwsbMxRUwVOSrEWCE/edit?tab=t.0

### March 28 - Apr 3, 2026
Estimated Total Time: 4 hours

**Goal 1: Complete UI redesign**
- Replaced all static displays with a dark tactical UI (IBM Plex Mono/Sans, Bebas Neue)
- Admin master roster now fully inline-editable — status, gender, size, and qty all editable directly in the table without navigating away
- Cadet portal shows personal uniform data with editable size/qty fields
- Tab-based navigation for Blues / OCP / PTG / Supply Room / Requests
- Toast notifications for all save/error/delete actions

**Goal 2: Bug fixes — Flask routes**
- Fixed `CSV_FILE` used before assignment in `approve_requests()` (caused crash on reset)
- Fixed missing file existence check in `upload()` download action (crashed on missing file)
- Fixed null file guard in `upload()` upload action
- Added `os.path.isdir` guard on `cadet_data/` directory in `cadet()` route
- Fixed name parsing inconsistency in `cadet_request()` for single-word names
- Fixed `approve_requests()` crashing when no CSV exists yet

**Goal 3: Excel file corruption fix**
- Identified root cause: openpyxl cannot round-trip `.xlsx` files containing Excel comments, drawings, or `docProps` metadata — calling `wb.save()` on such files destroys their internal zip structure
- Changed all `load_workbook()` calls to use `data_only=True` throughout
- Rewrote `save_cadet_edits` to read into memory and write a fresh workbook instead of mutating and saving in place
- Implemented atomic writes: all Excel saves now write to a temp file first, then `shutil.move()` into place — prevents Windows file-locking from producing truncated/corrupt files
- Removed backup system (was backing up corrupt files and making things worse)

**Goal 4: Admin file management**
- Added download buttons for Blues, OCP, PTG, and All Supply Data directly in the admin panel
- Backend `/upload` route already supported downloads — added frontend forms to expose this

### Jan 7, 2026
Estimated Total Time: 1 hour

- Fixed bug in table display in `approve.html`
- Fixed column heading issue and timestamping
- Added download button in `upload.html`
- Rewrote `flaskApp.py` router to support download feature

### Jan 5, 2026
Estimated Total Time: 2 hours

- Fixed bug in requests tab router
- Standardized requests tab formatting
- Fixed cadet data display (every other column skipping)
- Rewrote Excel parser for data display
- Standardized column headings
- Added RESET REQUESTS button in `approve.html`

### Dec 29, 2025
Estimated Total Time: 3 hours

- Updated README
- Researched deployment options: Render, Railway, Heroku

### Dec 28, 2025
Estimated Total Time: 10 hours

- Finished user interface HTML/CSS
- Created Flask backend routes for all pipelines
- Corrected database handling
- Started debugging uniform requests

### Dec 24, 2025
Estimated Total Time: 8 hours

- Implemented Flask
- Created `flaskApp.py` backend
- Created `index.html` frontend with CSS/JS

### Dec 23, 2025
Estimated Total Time: 4 hours

- Designed program architecture
- Created project outline
- Wrote initial README

---

## Bugs / Known Issues
- Inventory edit method in `inventory.html` not yet implemented
- Email system for semester uniform updates not yet implemented

## Contributing
Contributions are welcome! Feel free to submit pull requests for bug fixes, enhancements, or additional features.
