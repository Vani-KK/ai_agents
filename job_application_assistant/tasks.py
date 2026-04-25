from crewai import Task
from agents import job_analyst, resume_tailor, cover_letter_writer


def create_tasks(job_description: str, user_background: str):
    
    analyze_job_task = Task(
        description=f"""
        Carefully analyze the following job description and extract:
        
        1. REQUIRED SKILLS: Technical and soft skills explicitly mentioned
        2. PREFERRED SKILLS: Nice to have skills mentioned
        3. KEY RESPONSIBILITIES: Main duties of the role
        4. COMPANY CULTURE: Values and work environment clues
        5. KEYWORDS: Important terms for ATS optimization
        6. EXPERIENCE LEVEL: Junior, mid, senior indicators
        
        JOB DESCRIPTION:
        {job_description}
        
        Be thorough and specific. Your analysis will be used to tailor
        the resume and cover letter so don't miss anything important.
        """,
        expected_output="""A structured analysis with clearly labeled sections:
        Required Skills, Preferred Skills, Key Responsibilities, 
        Company Culture, ATS Keywords, and Experience Level.
        """,
        agent=job_analyst
    )


    tailor_resume_task = Task(
        description=f"""
        Using the job analysis from the previous task, tailor the 
        candidate's resume to perfectly match this specific job.
        
        CANDIDATE BACKGROUND:
        {user_background}
        
        YOUR JOB:
        1. Rewrite the professional summary to match the role
        2. Highlight the most relevant experience and skills
        3. Naturally incorporate ATS keywords from the job analysis
        4. Quantify achievements where possible (numbers, percentages)
        5. Remove or minimize irrelevant experience
        6. Ensure the resume tells a compelling story for THIS specific job
        
        Format the resume professionally with clear sections:
        - Professional Summary
        - Skills
        - Work Experience
        - Education
        """,
        expected_output="""A complete, professionally formatted resume 
        tailored specifically for the job. Should include all standard 
        resume sections and naturally incorporate relevant keywords.
        """,
        agent=resume_tailor
    )

    cover_letter_task = Task(
        description=f"""
        Write a compelling, personalized cover letter for this job application.
        
        Use the job analysis and tailored resume from previous tasks to:
        1. Open with a strong, attention grabbing first paragraph
        2. Connect the candidate's specific experience to the job requirements
        3. Show genuine knowledge of and interest in the company
        4. Highlight 2-3 specific achievements most relevant to this role
        5. Close with a confident call to action
        
        IMPORTANT RULES:
        - Never use generic phrases like "I am writing to apply for..."
        - Make it feel personal and genuine, not templated
        - Keep it to 3-4 paragraphs maximum
        - Match the tone to the company culture identified in the analysis
        """,
        expected_output="""A complete cover letter, 3-4 paragraphs, 
        that feels personal and specific to this job and company.
        Professional but human in tone.
        """,
        agent=cover_letter_writer
    )
    
    return [analyze_job_task, tailor_resume_task, cover_letter_task]




