
import pypdf
import os

pdf_files = ["projet_final_UCO.pdf", "grasp.pdf"]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f"\n--- EXTRACTED TEXT FROM {pdf_file} ---\n")
        try:
            reader = pypdf.PdfReader(pdf_file)
            for page in reader.pages:
                print(page.extract_text())
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    else:
        print(f"File not found: {pdf_file}")
