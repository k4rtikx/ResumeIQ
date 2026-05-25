

# import fitz  # PyMuPDF
# pdf_path = r"learning_phase/sample_resume.pdf"
# doc = fitz.open(pdf_path)
# full_text = ""
# for page in doc:
#     text = page.get_text()
#     full_text += text


# if (len(full_text) <= 50):
#     # OCR-based extraction
#     # # pyrefly: ignore [missing-import]
#     from pdf2image import convert_from_path
#     import pytesseract
#     pages = convert_from_path("learning_phase/sample_resume.pdf")

#     full_text = ""

#     for page in pages:
#         text = pytesseract.image_to_string(page)
#         full_text += text

# # to reframe the normal text to better text to use for gemini 
# import re
# full_text = re.sub(r"\s+", " ", full_text)
# full_text = full_text.strip()


# # production level find direct .env file location 
# from dotenv import load_dotenv
# from pathlib import Path
# env_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path=env_path)
# #================================================================================
# # normal one look for .env in SAME folder as current file
# """import os
# from dotenv import load_dotenv
# # pyrefly: ignore [missing-import]
# from google import genai

# # Load the .env file — this reads GEMINI_API_KEY into environment
# # before =.env is just a normal text file. 
# # after =opens .env reads all variables injects them into environment variables

# load_dotenv()
# #without this os.getenv returns None

# # Read the actual key value from environment (NOT the string "GEMINI_API_KEY")
# #Go to environment variables,find variable named GEMINI_API_KEY,return its value."""
# import os 
# # pyrefly: ignore [missing-import]
# from google import genai
# api_key = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents = f"""
# You are an ATS resume analyzer.

# Analyze the resume carefully.

# Return ONLY valid JSON.

# Do not add explanations.
# Do not add markdown.
# Do not add headings.
# Do not add extra text.

# JSON format:

# {{
#     "match_score": "",
#     "missing_skills": [],
#     "strong_points": [],
#     "weak_points": [],
#     "suggestions": [],
#     "project_alignment": ""
# }}

# Resume:
# {full_text}
# """
# )
# import json

# data = json.loads(response.text)
# print(data["match_score"])
# print(response.text)


########################################################################################################################
#1 Extraction of text from the PDF and clean it
import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    # doc = fitz.open(pdf_path) # normally we do this but here not
    # basically we are taking <InMemoryUploadedFile> these are not the same thing.
    doc = fitz.open(
        stream=pdf_path.read(),
        filetype="pdf"#doc → PyMuPDF Document Not a path.
    )
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def extract_text_from_pdf_ocr(pdf_path,full_text):
    if len(full_text) <= 50:
        pdf_path.seek(0)

        # OCR-based extraction
        # pyrefly: ignore [missing-import]
        from pdf2image import convert_from_bytes
        # from pdf2image import convert_from_path  == firstly we convert from path now bytes
        import pytesseract # library to extract text from image

        pages = convert_from_bytes(pdf_path.read())
        full_text = ""
        for page in pages:
            text = pytesseract.image_to_string(page)
            full_text += text
    full_text = re.sub(r"\s+", " ", full_text)
    full_text = full_text.strip()
    return full_text

#2 Loading .env file
from dotenv import load_dotenv
from pathlib import Path
def load_env():
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)


#3 Analyzing the text
import os 
# pyrefly: ignore [missing-import]
from google import genai    
def analyze_resume(full_text, job_description, job_title):
    prompt=f"""
You are an expert ATS (Applicant Tracking System) resume analyzer.

Analyze the resume against the job description and return ONLY valid JSON.
No markdown, no explanation, no extra text. Just raw JSON.

JSON format (follow exactly):
{{
    "ats_score": 0,
    "match_score": 0,
    "ats_passed": false,
    "matched_skills": [],
    "missing_skills": [],
    "keywords_found": 0,
    "keywords_total": 0,
    "keywords_found_list": [],
    "keyword_gaps": [],
    "strong_points": [],
    "weak_points": [],
    "suggestions": [],
    "section_scores": {{
        "summary": 0,
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "education": 0
    }},
    "project_alignment": ""
}}

Rules:
- ats_score: integer 0-100. How well the resume passes ATS filters based on keyword density, formatting signals, and role relevance.
- match_score: integer 0-100. Overall semantic match between resume and job description.
- ats_passed: true if ats_score >= 60, false otherwise.
- matched_skills: list of skills present in BOTH resume and job description.
- missing_skills: list of skills in job description NOT found in resume.
- keywords_found: count of JD keywords found in resume.
- keywords_total: total important keywords extracted from job description.
- keywords_found_list: actual keyword strings found in resume.
- keyword_gaps: actual keyword strings missing from resume.
- strong_points: list of resume strengths as specific sentences.
- suggestions: list of actionable improvement recommendations.
- section_scores: score each resume section from 0-10 based on quality and relevance.
- project_alignment: 2-3 sentence paragraph of overall recruiter-style feedback.

Job Title: {job_title}

        Resume:
        {full_text}

        Job Description:
        {job_description}

        """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text



import json
def gemini_resume_analyzer(resume,job_description,job_title):
    
    pdf_path = resume
    job_description = job_description
    # extract normal pdf text
    full_text = extract_text_from_pdf(pdf_path)

    # check for ocr
    full_text = extract_text_from_pdf_ocr(pdf_path,full_text)

    # load .env
    load_env()

    # analyze using Gemini
    response = analyze_resume(full_text, job_description,job_title)

    # print(response.text)

    import json

    response_text = response.strip()

    # Remove markdown if Gemini returns ```json ... ```
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")
    response_text = response_text.strip()
    data = json.loads(response_text)

    print(data["match_score"])
    print(data["matched_skills"])

    return data

# # Gemini ALWAYS returns valid JSON.
# That is dangerous.

# Sometimes Gemini may return:

# ```json
# {
#  ...
# }
# which breaks parsing.

# Later you’ll learn:
# - try/except
# - response cleaning
# - validation
