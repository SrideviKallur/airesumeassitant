
import boto3
import json

# Connect to our personal AWS account
session = boto3.Session(
    profile_name="personal",
    region_name="ap-southeast-2"
)

bedrock = session.client("bedrock-runtime")

MODEL_ID = "amazon.titan-embed-text-v2:0"


def generate_embedding(text):

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "inputText": text,
            "dimensions": 1024,
            "normalize": True
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]


if __name__ == "__main__":

    sample_text = "I have 11 years of experience in Java, Spring Boot, AWS and Kafka."

    embedding = generate_embedding(sample_text)

    print("\nEmbedding generated successfully!")
    print("Number of dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])
