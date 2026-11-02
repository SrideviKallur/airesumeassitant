# AI Resume Assistant

An AI-powered resume analysis and job matching application built with Python and Amazon Bedrock. The application extracts information from resumes, evaluates candidates against job descriptions, and answers questions using Retrieval-Augmented Generation (RAG).

## Features

### 1. Resume Parsing
- Extracts text from PDF resumes.
- Processes resume content for downstream analysis.
- Supports different resume section headings and layouts, with unknown headings preserved.

### 2. Resume Analysis
- Generates a professional experience summary.
- Identifies technical skills and backend engineering experience.
- Evaluates cloud, AWS and Kafka experience.
- Highlights potential areas for improvement.

### 3. Job Description Matching
- Compares a candidate's resume against a job description.
- Identifies strong matches, partial matches and skill gaps.
- Provides supporting evidence from the resume.
- Generates relevant interview questions.
- Returns structured JSON results.

### 4. Employment Metadata Extraction
Extracts employment information, including:
- Employer
- Job title
- Location
- Employment start and end dates
- Client name, when available
- Supporting text evidence

The extractor uses rule-based pattern matching and does not hardcode specific employer or client names.

### 5. Retrieval-Augmented Generation (RAG)
- Splits resume content into smaller chunks.
- Generates vector embeddings using Amazon Bedrock.
- Stores and searches embeddings using FAISS.
- Retrieves relevant resume content for user questions.
- Generates answers grounded in retrieved resume evidence.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Amazon Bedrock | Generative AI and embeddings |
| Amazon Nova Lite | Language model |
| Amazon Titan Text Embeddings V2 | Text embeddings |
| FAISS | Vector similarity search |
| boto3 | AWS SDK |
| pypdf | PDF text extraction |
| NumPy | Vector operations |
| unittest | Automated testing |

## Project Structure

```text
airesumeassitant/
│
├── src/
│   ├── app.py
│   ├── resume_parser.py
│   ├── resume_analyser.py
│   ├── job_matcher.py
│   ├── metadata_extractor.py
│   ├── text_chunker.py
│   ├── embedding_service.py
│   ├── vector_store.py
│   ├── rag_service.py
│   ├── test_text_chunker.py
│   └── test_metadata_extractor.py
│
├── data/                    # Generated vector data (not committed)
├── resume.pdf               # Local sample resume (not committed)
├── .gitignore
├── README.md
└── venv/                    # Python virtual environment (not committed)
```

## Prerequisites

- Python 3.9 or later
- AWS account
- AWS CLI
- Amazon Bedrock model access in your selected AWS region
- Git

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/SrideviKallur/airesumeassitant.git
cd airesumeassitant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install boto3 python-dotenv pypdf faiss-cpu numpy
```

### 4. Configure AWS authentication

Authenticate using your own AWS account:

```bash
aws login --profile personal --region ap-southeast-2
```

Verify your AWS identity:

```bash
aws sts get-caller-identity --profile personal
```

Ensure the returned account is your intended personal AWS account.

The application currently uses:
- AWS profile: `personal`
- AWS region: `ap-southeast-2`
- Language model inference profile: `apac.amazon.nova-lite-v1:0`
- Embedding model: `amazon.titan-embed-text-v2:0`

You must have appropriate Amazon Bedrock permissions and model access.

### 5. Add a resume

Place a PDF resume in the project root and name it:

```text
resume.pdf
```

The sample resume is intentionally excluded from Git.

## Running the Application

Run commands from the project root with the virtual environment activated.

### Resume text extraction

```bash
python src/resume_parser.py
```

### Resume analysis

```bash
python src/resume_analyser.py
```

### Job description matching

```bash
python src/job_matcher.py
```

Paste the job description into the terminal and enter `END` on a new line when finished.

### Employment metadata extraction

```bash
python src/metadata_extractor.py
```

### Build the vector store

```bash
python src/vector_store.py
```

This extracts the resume, creates chunks, generates embeddings and saves the FAISS index and chunk metadata under `data/`.

### Ask questions using RAG

```bash
python src/rag_service.py
```

Enter questions about the resume. Type `EXIT` to stop.

## Running Tests

Run the automated unit tests:

```bash
python -m unittest discover -s src -p "test_*.py" -v
```

The current test suite covers:
- Resume chunking with different numbers of sections.
- Unknown and missing resume headings.
- Employment metadata extraction.
- Multiple employment records.
- Certifications and education exclusions.
- Employment records without client information.

## Privacy and Security

- Resume documents and generated candidate data are excluded from Git.
- AWS credentials should never be committed to the repository.
- Use your own AWS account and appropriate IAM permissions.
- Keep candidate documents and generated embeddings appropriately protected.

## Current Limitations

- PDF text extraction may not preserve the original document layout.
- Employment metadata extraction currently relies on common heading and date patterns.
- The metadata extractor may need improvements for resumes with unusual layouts.
- The vector store currently uses a local FAISS index.
- The application is a RAG-based assistant, not yet an autonomous AI agent.
- Multi-candidate isolation and a user interface are planned enhancements.

## Future Enhancements

- Support for DOCX and additional resume formats.
- More robust employment and candidate metadata extraction.
- Support for multiple candidates with isolated vector stores.
- Improved semantic resume and job matching.
- Streamlit-based user interface.
- AI agent capabilities and tool calling.
- Cloud deployment and scalable document storage.

## Author

Developed as a personal learning and engineering project exploring Generative AI, Amazon Bedrock, embeddings, vector databases and Retrieval-Augmented Generation.