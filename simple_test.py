# simple_test.py

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Check if API key is set
print(f"OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")

# Create a simple agent
try:
    # Initialize OpenAI LLM with minimal settings
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=500
    )
    
    # Create a simple agent
    researcher = Agent(
        role="Researcher",
        goal="Research and provide information",
        backstory="You are an AI research assistant.",
        llm=llm,
        verbose=True
    )
    
    # Create a simple task
    research_task = Task(
        description="Provide a brief summary of AI advancements in 2023.",
        expected_output="A short paragraph summarizing key AI advancements.",
        agent=researcher
    )
    
    # Create and run a simple crew
    print("\nInitializing Simple Crew...")
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
        process=Process.sequential,
        memory=False  # Disable memory to reduce token usage
    )
    
    print("\nStarting Crew execution...")
    result = crew.kickoff()
    
    # Print the result
    print("\nResult:")
    print(result)
    
except Exception as e:
    print(f"\nError: {str(e)}")
    import traceback
    print(traceback.format_exc())