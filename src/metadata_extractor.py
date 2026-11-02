
import re


DATE_PATTERN = re.compile(
    r"([A-Za-z]{3,9}\s+\d{4})"
    r"\s*[–—-]\s*"
    r"(Present|Current|[A-Za-z]{3,9}\s+\d{4})",
    re.IGNORECASE
)


def extract_employment_metadata(resume_text):

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    employment_records = []

    for index, line in enumerate(lines):

        # Employment details are expected on the following line.
        if index + 1 >= len(lines):
            continue

        details = lines[index + 1]

        # Require a date range to distinguish employment
        # headings from certifications and education.
        date_match = DATE_PATTERN.search(details)

        if not date_match:
            continue

        # Support common dash separators.
        separator_match = re.search(r"\s+[—–-]\s+", line)

        if not separator_match:
            continue

        employer = line[:separator_match.start()].strip()
        job_title = line[separator_match.end():].strip()

        if not employer or not job_title:
            continue

        start_date = date_match.group(1)
        end_date = date_match.group(2)

        # Extract client if available.
        client_match = re.search(
            r"Client:\s*(.*?)(?:\s*\||$)",
            details,
            re.IGNORECASE
        )

        client = (
            client_match.group(1).strip()
            if client_match else None
        )

        # Extract location if available.
        location = None

        if "|" in details:
            location = details.split("|", 1)[0].strip()

        employment_records.append({
            "employer": employer,
            "job_title": job_title,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "client": client,
            "evidence": line
        })

    return employment_records


if __name__ == "__main__":

    from pathlib import Path
    import json

    from resume_parser import extract_resume_text

    project_root = Path(__file__).resolve().parent.parent
    resume_path = project_root / "resume.pdf"

    resume_text = extract_resume_text(resume_path)

    records = extract_employment_metadata(resume_text)

    print("\nEXTRACTED EMPLOYMENT METADATA:\n")
    print(json.dumps(records, indent=4))
    print("\nTotal employment records:", len(records))
