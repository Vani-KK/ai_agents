import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import job_analyst, resume_tailor, cover_letter_writer
from tasks import create_tasks

load_dotenv()

def run_crew(job_description: str, user_background: str) -> dict:
    
    # Create tasks with the actual inputs
    tasks = create_tasks(job_description, user_background)
    
    # Assemble the crew
    crew = Crew(
        agents=[job_analyst, resume_tailor, cover_letter_writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Kick off the crew
    result = crew.kickoff()
    
    # Extract each task's output separately
    return {
        "job_analysis": tasks[0].output.raw if tasks[0].output else "",
        "tailored_resume": tasks[1].output.raw if tasks[1].output else "",
        "cover_letter": tasks[2].output.raw if tasks[2].output else ""
    }


if __name__ == "__main__":
    # Test with sample data
    job_desc = """
    We are looking for a Python Developer with 2+ years of experience.
    Requirements:
    - Strong Python skills
    - Experience with REST APIs
    - Knowledge of SQL databases
    - Good communication skills
    - Team player
    """
    
    background = """
    My name is Vani. I have 1 year of experience in Python development.
    I have built REST APIs using Flask, worked with MySQL databases,
    and collaborated with teams using Git. I am a quick learner
    and have strong communication skills.
    """
    
    print("Running Job Application Assistant...\n")
    result = run_crew(job_desc, background)
    
    print("\n" + "="*50)
    print("JOB ANALYSIS:")
    print(result["job_analysis"])
    
    print("\n" + "="*50)
    print("TAILORED RESUME:")
    print(result["tailored_resume"])
    
    print("\n" + "="*50)
    print("COVER LETTER:")
    print(result["cover_letter"])

