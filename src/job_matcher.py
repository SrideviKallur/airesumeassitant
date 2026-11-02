
from pathlib import Path
import json

from resume_parser import extract_resume_text
from app import ask_bedrock_json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESUME_PATH = PROJECT_ROOT / "resume.pdf"


def match_job_description():

    # Step 1: Extract resume text
    resume_text = extract_resume_text(RESUME_PATH)

    # Step 2: Get job description
    print("\nPaste the job description below.")
    print("Enter END on a new line when finished.\n")

    job_description_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        job_description_lines.append(line)

    job_description = "\n".join(job_description_lines)

    if not job_description.strip():
        print("Job description cannot be empty.")
        return

    # Step 3: Build AI prompt
    prompt = f"""
    You are a strict technical recruitment evaluator.

    Compare the candidate's resume against the job description.

    IMPORTANT RULES:
    1. Only use information explicitly supported by the resume.
    2. Never assume the candidate has a skill based on general knowledge.
    3. Do not invent projects, responsibilities or achievements.
    4. If there is no supporting evidence, classify the skill as
       "Not demonstrated".
    5. Distinguish between hands-on production experience,
       learning experience and familiarity with a tool.
    6. Give a confidence level for each assessment.

    Return a JSON object using this structure:

    {{
        "match_percentage": 0,
        "strong_matches": [
            {{
                "skill": "Java",
                "evidence": "Specific evidence from the resume",
                "confidence": "High"
            }}
        ],
        "partial_matches": [
            {{
                "skill": "AI agents",
                "evidence": "What the resume actually demonstrates",
                "missing_evidence": "What is not demonstrated",
                "confidence": "Medium"
            }}
        ],
        "skill_gaps": [
            {{
                "skill": "Skill name",
                "reason": "Why the resume does not demonstrate it"
            }}
        ],
        "relevant_experience": [],
        "resume_improvements": [],
        "interview_questions": []
    }}

    Match percentage must be between 0 and 100.
    Provide exactly five interview questions.
    Return only valid JSON without Markdown code fences.

    CANDIDATE RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """

    # Step 4: Call Amazon Bedrock
    print("\nComparing your resume with the job description...\n")

    result = ask_bedrock_json(prompt)

    if result:

        required_fields = [
            "match_percentage",
            "strong_matches",
            "partial_matches",
            "skill_gaps",
            "relevant_experience",
            "resume_improvements",
            "interview_questions"
        ]

        # Check that all required fields exist
        missing_fields = [
            field for field in required_fields
            if field not in result
        ]

        if missing_fields:
            print("Invalid AI response. Missing fields:", missing_fields)
            return

        # Validate match percentage
        score = result["match_percentage"]

        if not isinstance(score, (int, float)) or not 0 <= score <= 100:
            print("Invalid match percentage.")
            return

        # Validate interview questions
        if not isinstance(result["interview_questions"], list):
            print("Interview questions must be a list.")
            return

        if len(result["interview_questions"]) != 5:
            print("Expected exactly five interview questions.")
            return

        print("\nJOB MATCH ANALYSIS:\n")
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    match_job_description()
