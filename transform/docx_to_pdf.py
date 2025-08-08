import sys
import subprocess
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from xhtml2pdf import pisa

# Install these dependencies if missing:
# pandoc from https://pandoc.org/installing.html
# wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
# If on MacOS, you can use Homebrew:
# `brew install pandoc`
# The wkhtmltopdf cask has been deprecated, so this script uses xhtml2pdf instead.

def docx_to_pdf(docx_path, pdf_path):
    """
    Convert a DOCX file to PDF using Pandoc and wkhtmltopdf.
    Requires: pandoc and wkhtmltopdf installed and available in PATH.

    Usage: python docx_to_pdf.py input.docx output.pdf
    If output is a directory, the PDF will be saved with the same name as the DOCX.
    If input is a directory, all DOCX files in that directory will be converted to PDF.
    """
    input_path = Path(docx_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {docx_path}")

    if pdf_path is None:
        output_path = input_path.with_suffix(".pdf")
    else:
        output_path = Path(pdf_path)
        if not output_path.exists():
            raise FileNotFoundError(f"Output path does not exist: {pdf_path}")
        elif output_path.suffix.lower() != ".pdf":
            output_path = output_path.with_suffix(".pdf")

    # Create a temporary directory to hold the intermediate HTML file
    # with TemporaryDirectory() as temp_dir:
    #     html_path = Path(temp_dir) / f"{input_path.stem}.html"
    html_path = input_path.with_suffix(".html")

    # Convert DOCX to HTML
    subprocess.run(["pandoc", str(input_path), "-o", str(html_path)], check=True)

    # Convert HTML to PDF
    with open(html_path, "rb") as html_file:
        html_content = html_file.read()

    pdf_output = BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_output, encoding="utf-8")

    with open(output_path, "wb") as pdf_file:
        pdf_file.write(pdf_output.getvalue())

    # if html_path.is_file():
    #     html_path.unlink(missing_ok=True)

    print(f"Converted: {input_path.name} -> {output_path.name}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert DOCX to PDF.")
    parser.add_argument("docx", help="Path to the DOCX file or directory.")
    parser.add_argument("-o", "--output", help="Path to the output PDF file.", default=None)
    parser.add_argument("-d", "--directory", help="Flag to convert all the DOCX files in the specified directory. The PDFs will be saved in the same directory with the same name.", type=bool)

    args = parser.parse_args()

    if args.directory:
        docx_path = Path(args.docx)
        if not docx_path.is_dir():
            print(f"Error: {docx_path} is not a directory.")
            sys.exit(1)

        for docx_file in docx_path.glob("*.docx"):
            pdf_file = docx_file.with_suffix(".pdf")
            docx_to_pdf(docx_file, pdf_file)
    else:
        if not args.docx:
            print("Error: No DOCX file specified.")
            sys.exit(1)

        docx_to_pdf(args.docx, args.output if args.output else None)

if __name__ == "__main__":
    main()
