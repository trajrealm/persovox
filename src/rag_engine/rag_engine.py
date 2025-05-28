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

    return resume, "Cover letter coming soon..."
    # for doc in docs:
    #     print("\n--- Retrieved chunk ---\n")
    #     print(doc.page_content)

    # llm = ChatOpenAI(model_name=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY)

    # qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    
    # resume_prompt = (
    #     "Based ONLY on the user's resume data retrieved below, "
    #     "generate a tailored resume for this job:\n\n"
    #     f"JOB DESCRIPTION:\n{job_description}\n\n"
    #     "USER RESUME DATA:\n{context}\n\n"
    #     "Do NOT make up degrees, jobs, or skills. Only use what’s in the context."
    # )    
    
    # cover_letter_prompt = (
    #     "Based ONLY on the user's resume data retrieved below, "
    #     "generate a tailored cover letter for this job:\n\n"
    #     f"JOB DESCRIPTION:\n{job_description}\n\n"
    #     "USER RESUME DATA:\n{context}\n\n"
    #     "Do NOT make up degrees, jobs, or skills. Only use what’s in the context."
    # )

    # tailored_resume = qa_chain.run(resume_prompt)
    # cover_letter = qa_chain.run(cover_letter_prompt)

    # return tailored_resume, cover_letter
