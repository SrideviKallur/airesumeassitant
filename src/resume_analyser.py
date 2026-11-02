from resume_parser import extract_resume_text
from app import ask_bedrock

RESUME_PATH = "resume.pdf"


def analyse_resume():

    resume_text = extract_resume_text(RESUME_PATH)

    prompt = f"""
    You are an experienced technical recruiter.

    Analyse the following resume.

    Provide:

    1. Professional experience summary.
    2. Strongest technical skills.
    3. Backend engineering experience.
    4. Cloud and AWS experience.
    5. Event-driven architecture and Kafka experience.
    6. Areas where the candidate could improve.

    Resume:

    {resume_text}
    """

    print("\nAnalysing resume with Amazon Bedrock...\n")

    response = ask_bedrock(prompt)

    if response:
        print("\nRESUME ANALYSIS:\n")
        print(response)


if __name__ == "__main__":
    analyse_resume()