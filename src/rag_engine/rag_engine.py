# rag_engine.py
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from config.config import OPENAI_API_KEY, OPENAI_MODEL
from src.rag_engine.chroma_store import get_vectorstore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def generate_resume_coverletter(job_description: str, user_id: str) -> str:
    retriever = get_vectorstore().as_retriever(search_type="similarity", search_kwargs={"k": 10, "filter": {"user_id": user_id}})
    docs = retriever.get_relevant_documents(job_description)

    if not docs:
        raise ValueError(f"No relevant documents found for the job description and user '{user_id}'.")

    context = "\n\n".join([doc.page_content for doc in docs])

    resume_template = PromptTemplate(
        input_variables=["job_description", "context"],
        template=(f"""
        You are a professional resume writer. Your task is to write a complete, professional detailed tailored resume based on the user's previous resume data and the job description provided.

        Requirements:
        - ONLY use content found in the context — do not make up job titles, dates, or locations.
        - If a detail like address or phone is missing, omit it silently.
        - Use professional formatting: start with contact info, then a summary, then sections like EXPERIENCE, SKILLS, EDUCATION.
        - Extract the degree name, university name, location and year of graduation from the education section for all degrees.        
        - Do NOT include phrases like "insert here", "TBD", or similar placeholders.
        - Output ONLY the resume text — no commentary, no additional explanation.

        JOB DESCRIPTION:
        {job_description}

        USER RESUME DATA:
        {context}

        RESUME:
        """
        )
    )

    chain = LLMChain(
        llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3),
        prompt=resume_template
    )

    resume = chain.run({"job_description": job_description, "context": context})
    # Optionally do the same for cover letter

    # --- Cover Letter Prompt ---
    cover_prompt = PromptTemplate(
        input_variables=["job_description", "context"],
        template=(
            """
            You are a professional career writer. Write a customized, concise, and compelling cover letter tailored to the provided job description using the user's prior experience below.

            Guidelines:
            - Highlight the user's most relevant experiences, skills, and accomplishments.
            - Match tone and language to that of a professional job application.
            - Do NOT repeat the resume.
            - Begin with a strong introduction, a focused body, and a professional closing.
            - DO NOT include filler like “insert name here” or “to whom it may concern”. Infer based on job description/context if necessary.
            - Output ONLY the cover letter text.

            JOB DESCRIPTION:
            {job_description}

            USER RESUME DATA:
            {context}

            COVER LETTER:
            """
         )
    )

    cover_chain = LLMChain(
        llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.4),  # slightly more creative
        prompt=cover_prompt
    )

    cover_letter = cover_chain.run({"job_description": job_description, "context": context})

    return resume, cover_letter
