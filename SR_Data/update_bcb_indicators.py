import csv
import shutil
from pathlib import Path

def update_bcb_indicators():
    # New indicators to add
    new_indicators = [
        ("SELIC", "432", "1"),
        ("CDI", "4389", "1"),
        ("IPCA", "433", "1"),
        ("IPCA_12M", "433", "1"),
        ("IPCA_ANO", "433", "1"),
        ("IPCA_ANUAL", "433", "1"),
        ("IGP-M", "189", "1"),
        ("IGP-M_12M", "189", "1"),
        ("IGP-M_ANO", "189", "1"),
        ("IGP-M_ANUAL", "189", "1"),
        ("CAMBIO_USD", "1", "1"),
        ("IBC-BR", "24363", "1"),
        ("IBC-BR_12M", "24363", "1"),
        ("IBC-BR_ANO", "24363", "1")
    ]

    # Backup existing file
    bcb_file = Path("data/config/BCB_SGS.csv")
    backup_file = Path("data/config/BCB_SGS.csv.bak")
    shutil.copy(bcb_file, backup_file)

    # Read existing indicators
    existing_indicators = set()
    with open(bcb_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                existing_indicators.add(row[0])  # Add indicator name to set

    # Write updated file
    with open(bcb_file, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        for name, code, mult in new_indicators:
            if name not in existing_indicators:
                writer.writerow([name, code, mult])

    print("BCB indicators updated successfully!")

if __name__ == "__main__":
    update_bcb_indicators()
