from pypdf import PdfReader


def extract_resume_text(pdf_path):
    """
    Extract text from a resume PDF.
    """

    reader = PdfReader(pdf_path)

    extracted_text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text


if __name__ == "__main__":
    resume_path = "resume.pdf"

    text = extract_resume_text(resume_path)

    print("\nRESUME TEXT:\n")
    print(text)