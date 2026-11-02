
import boto3
import json
from botocore.exceptions import ClientError

# Connect to personal AWS account
session = boto3.Session(
    profile_name="personal",
    region_name="ap-southeast-2"
)

bedrock = session.client("bedrock-runtime")

MODEL_ID = "apac.amazon.nova-lite-v1:0"


# Function 1: Call Amazon Bedrock
def ask_bedrock(question):
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": question}]
                }
            ],
            inferenceConfig={
                "maxTokens": 2000,
                "temperature": 0.3
            }
        )

        return response["output"]["message"]["content"][0]["text"]

    except ClientError as error:
        print("Bedrock error:", error.response["Error"]["Message"])
        return None


# Function 2: Parse AI response as JSON
def ask_bedrock_json(question):

    prompt = f"""
    {question}

    Return ONLY a valid JSON object.
    Do not include markdown code fences or explanations outside the JSON.
    """

    response = ask_bedrock(prompt)

    if not response:
        return None

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace("```json", "", 1)
            cleaned_response = cleaned_response.replace("```", "", 1)

        cleaned_response = cleaned_response.strip()

        return json.loads(cleaned_response)

    except json.JSONDecodeError as error:
        print("Could not parse JSON:", error)
        print("Raw response:", response)
        return None


# Main execution
if __name__ == "__main__":

    question = """
    Return a JSON object with:
    - greeting
    - message
    """

    print("\nAsking Amazon Bedrock...\n")

    result = ask_bedrock_json(question)

    if result:
        print("JSON RESPONSE:")
        print(json.dumps(result, indent=4))
