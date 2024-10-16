import pandas as pd

# Load the Excel file
file_path = 'Frequency List.xlsx'
sheet_name = 'The List - Frequency List'

# Read the specified sheet into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract the 'Lemma' column
lemma_column = df["Frequency List"]

print([i for i in lemma_column])

# Export the 'Lemma' column to a text file
with open('lemmas.txt', 'w', encoding='utf-8') as f:
    for lemma in lemma_column[1:-1]:
        ll = lemma.find("|")
        lemma = lemma[:ll].strip()
        f.write(f"{lemma}\n")

print("Export completed successfully.")
