
import re
from pathlib import Path

from resume_parser import extract_resume_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESUME_PATH = PROJECT_ROOT / "resume.pdf"

# Map different resume headings to internal categories.
SECTION_ALIASES = {
    "Summary": [
        "professional summary", "summary", "profile",
        "about me", "career summary", "executive summary",
        "career objective", "objective", "personal profile"
    ],
    "Skills": [
        "core skills", "technical skills", "skills",
        "key skills", "technical expertise",
        "areas of expertise", "key competencies",
        "competencies", "technology stack",
        "technical proficiencies"
    ],
    "Experience": [
        "professional experience", "work experience",
        "employment history", "work history",
        "career history", "experience"
    ],
    "Projects": [
        "projects", "selected projects",
        "key projects", "project experience"
    ],
    "Education": [
        "education", "academic background",
        "academic qualifications", "qualifications"
    ],
    "Certifications": [
        "certifications", "certificates",
        "professional certifications", "credentials",
        "licences", "licenses"
    ]
}


def normalize_heading(line):
    return re.sub(r"[^a-z0-9 ]", "", line.lower()).strip()


def identify_heading(line):
    """Identify known heading variations."""
    normalized = normalize_heading(line)

    for category, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if normalized == normalize_heading(alias):
                return category

    return None


def is_possible_unknown_heading(line):
    """
    Identify high-confidence unfamiliar headings.

    Initially, only short standalone uppercase lines
    are considered unknown headings.
    """
    cleaned = line.strip()

    if not cleaned or len(cleaned) > 60:
        return False

    if len(cleaned.split()) > 7:
        return False

    # Avoid treating bullet points as headings.
    if cleaned.startswith(("•", "-", "*", "")):
        return False

    letters = [char for char in cleaned if char.isalpha()]

    if not letters:
        return False

    return all(char.isupper() for char in letters)


def split_text_into_chunks(text, chunk_size=100, overlap=20):

    lines = text.splitlines()
    sections = []

    current_section = {
        "section": "Other",
        "original_heading": "Document Start",
        "text": []
    }

    for line in lines:

        known_heading = identify_heading(line)

        if known_heading:
            if current_section["text"]:
                sections.append(current_section)

            current_section = {
                "section": known_heading,
                "original_heading": line.strip(),
                "text": []
            }

        else:
            current_section["text"].append(line)

    if current_section["text"]:
        sections.append(current_section)

    chunks = []

    for section in sections:

        section_text = " ".join(
            line.strip()
            for line in section["text"]
            if line.strip()
        )

        words = section_text.split()
        start = 0

        while start < len(words):

            end = start + chunk_size
            chunk_text = " ".join(words[start:end])

            chunks.append({
                "chunk_id": len(chunks) + 1,
                "section": section["section"],
                "original_heading": section["original_heading"],
                "text": chunk_text
            })

            if end >= len(words):
                break

            start = end - overlap

    return chunks


if __name__ == "__main__":

    resume_text = extract_resume_text(RESUME_PATH)

    chunks = split_text_into_chunks(resume_text)

    print("\nTotal chunks:", len(chunks))

    for chunk in chunks:
        print("\n" + "=" * 60)
        print("Chunk ID:", chunk["chunk_id"])
        print("Section:", chunk["section"])
        print("Original heading:", chunk["original_heading"])
        print("=" * 60)
        print(chunk["text"])
