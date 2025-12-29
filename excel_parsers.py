import openpyxl
import re

def clean_uniform_name(header):
    # Remove gender notes and "- Size"
    name = re.sub(r"\s*-\s*Size.*$", "", header)
    name = re.sub(r"\(.*?\)", "", name)
    return name.strip()

def load_cadet_excel(filepath):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    headers = [cell.value for cell in ws[1]]
    uniform_headers = headers[3::2]
    uniform_names = [clean_uniform_name(h) for h in uniform_headers]

    rows = []

    for row in ws.iter_rows(min_row=2, values_only=True):

        # Stop at first empty cadet row
        if not any(row[0:3]):
            break

        cadet = {
            "name": row[0],
            "status": row[1],
            "gender": row[2],
        }

        sizes = []
        for i in range(3, len(row), 2):
            sizes.append(row[i])

        rows.append({
            "cadet": cadet,
            "sizes": sizes
        })

    return {
        "uniform_types": uniform_names,
        "rows": rows
    }
