# src/agentic_api/main.py

import os
import argparse
from dotenv import load_dotenv
from .crew import ResearchCrew

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the research crew."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run a research crew on a specific topic')
    parser.add_argument('--topic', type=str, default='Artificial Intelligence',
                        help='The topic to research (default: Artificial Intelligence)')
    args = parser.parse_args()
    
    # Create and run the crew
    crew = ResearchCrew()
    result = crew.build().kickoff(inputs={'topic': args.topic})
    
    # Print the result
    print("\nResearch Report:")
    print(result.raw)
    
    # Save the result to a file
    with open('report.md', 'w') as f:
        f.write(result.raw)
    
    print("\nReport saved to report.md")

if __name__ == "__main__":
    main()