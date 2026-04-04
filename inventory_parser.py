import openpyxl

def load_inventory(filepath):
    """
    Parse AllInventoryData.xlsx into a structured format:
    [
      {
        "section": "PTGs",
        "items": [
          {
            "name": "Shirt",
            "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "rows": [
              { "length": None, "quantities": { "XS": 7, "S": 0, ... } }
            ]
          },
          {
            "name": "Jacket",
            "sizes": ["XS", "S", "M", "L", "XL"],
            "rows": [
              { "length": "Short",   "quantities": { "XS": 0, ... } },
              { "length": "Regular", "quantities": { "XS": 0, ... } },
              { "length": "Long",    "quantities": { "XS": 0, ... } },
            ]
          },
          ...
        ]
      },
      ...
    ]
    """
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    sections = []
    current_section = None
    current_item = None

    for row in ws.iter_rows(values_only=True):
        # Skip fully empty rows
        if not any(row):
            continue

        col_b = row[1]   # section headers live in col B (index 1)
        col_c = row[2]   # item names live in col C (index 2)
        col_d = row[3]   # length sub-rows or first size value (index 3)

        # Section header: col B has value, nothing else
        if col_b and not col_c and not any(row[2:]):
            current_section = {"section": str(col_b), "entries": []}
            sections.append(current_section)
            current_item = None
            continue

        if current_section is None:
            continue

        # Item header: col C has name, col D onward has sizes
        if col_c and any(v for v in row[3:] if isinstance(v, str)):
            sizes = [str(v) for v in row[3:] if isinstance(v, str) and v]
            current_item = {"name": str(col_c), "sizes": sizes, "rows": []}
            current_section["entries"].append(current_item)
            continue

        # Simple item (no length): col C has name, col D onward has numbers
        if col_c and any(v for v in row[3:] if isinstance(v, (int, float))):
            sizes = []
            quantities = {}
            # sizes come from row[3:] positions with numbers — but we need
            # to re-read the header row. For simple items, sizes ARE the
            # header row values at those positions.
            # We handle this by treating col_c row as both name + qty row
            current_item = {"name": str(col_c), "sizes": [], "rows": []}
            current_section["entries"].append(current_item)
            # sizes discovered inline from previous header already set above
            # Fall through to quantity parsing below

        # Quantity row: col D might be a length string or a number
        if current_item is not None and not col_c:
            if isinstance(col_d, str) and not col_b:
                # Length sub-row: "Short", "Regular", "Long", etc.
                qtys = {}
                for i, size in enumerate(current_item["sizes"]):
                    val = row[4 + i] if (4 + i) < len(row) else None
                    qtys[size] = val if isinstance(val, (int, float)) else 0
                current_item["rows"].append({"length": col_d, "quantities": qtys})
            elif isinstance(col_d, (int, float)) or any(isinstance(v, (int, float)) for v in row[3:]):
                # Simple qty row (no length)
                qtys = {}
                for i, size in enumerate(current_item["sizes"]):
                    val = row[3 + i] if (3 + i) < len(row) else None
                    qtys[size] = val if isinstance(val, (int, float)) else 0
                current_item["rows"].append({"length": None, "quantities": qtys})

        # Handle simple items where col_c and numbers are on the same row
        if col_c and current_item and current_item["name"] == str(col_c) and not current_item["rows"]:
            # Already created item above, now add its qty row
            qtys = {}
            for i, size in enumerate(current_item["sizes"]):
                val = row[3 + i] if (3 + i) < len(row) else None
                qtys[size] = val if isinstance(val, (int, float)) else 0
            if qtys:
                current_item["rows"].append({"length": None, "quantities": qtys})

    return sections