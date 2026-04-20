import sys

try:
    import pypdf
except ImportError:
    print("pypdf not installed. Please pip install it first.")
    sys.exit(1)

def extract_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print("--- EXTRACTED TEXT ---")
        print(text)
    except Exception as e:
        print("Error reading PDF:", e)

if __name__ == "__main__":
    extract_text(r"d:\Projects\bureacuracy-automation-ui\public\Dropdown.pdf")
