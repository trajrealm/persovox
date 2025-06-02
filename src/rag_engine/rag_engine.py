# rag_engine.py
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from config.config import OPENAI_API_KEY, OPENAI_MODEL
from src.rag_engine.chroma_store import get_vectorstore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def generate_resume_coverletter(job_description: str, user_id: str) -> str:
    retriever = get_vectorstore(user_id).as_retriever(search_type="mmr", search_kwargs={"k": 25}
    )
    docs = retriever.get_relevant_documents(job_description)

    if not docs:
        raise ValueError(f"No relevant documents found for the job description and user '{user_id}'.")

    context = "\n\n".join([doc.page_content for doc in docs])

    resume_template = PromptTemplate(
        input_variables=["job_description", "context"],
        template=(f"""
        You are a professional resume writer. Your task is to write a complete, professional detailed tailored resume based on the user's previous resume data and the job description provided.

        KEY RULES:
        - Start with a contact section using the provided name, email, phone, etc.
        - **DO NOT invent** information. Use only the content from the context below.
        - **DO include every job/experience** mentioned in the context, even if it seems unrelated to the job.
        - **DO include every educational background** mentioned in the context, even if it seems unrelated to the job.
        - If a role is not directly relevant, still include it with **at least one bullet point** describing a meaningful contribution.
        - Maintain full **chronological continuity** of the user’s job history.
        - Always include these sections if available: **Contact Info**, **Professional Summary**, **Highlights**, **Experience**, **Skills**, and **Education**.
        - Ensure the resume includes ALL previous job roles and ALL educational history found in the context. If the information spans multiple chunks or pages, reconstruct it accurately. Do not omit job roles even if they seem less relevant.
        - Use a clean and professional formatting style.
        - Omit missing details (like address or phone) silently.
        - DO NOT include placeholders like "insert here" or "TBD".
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
            - Start with a professional greeting (e.g., “Dear Hiring Manager,”)
            - Mention the role and where it was found.
            - Summarize the candidate's relevant experience, skills, accomplishments, and interest in the company.
            - Refer to specific skills or experience from context that match the job description.
            - Match tone and language to that of a professional job application.
            - Do NOT repeat the resume.
            - Begin with a strong introduction, a focused body, and a professional closing.
            - DO NOT include filler like “insert name here” or “to whom it may concern”. 
            - NEVER use placeholder text like [Your Name].
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
