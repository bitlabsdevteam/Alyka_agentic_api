# simplified_social_media.py

import os
import argparse
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Social Media Analysis Tool")
    parser.add_argument("--hashtags", type=str, default="ai", help="Comma-separated list of hashtags to analyze")
    parser.add_argument("--min-items", type=int, default=3, help="Minimum items to collect per hashtag")
    parser.add_argument("--use-gpt35-fallback", action="store_true", help="Use GPT-3.5-Turbo instead of GPT-4o")
    args = parser.parse_args()
    
    # Process hashtags
    hashtags = [tag.strip() for tag in args.hashtags.split(",")]
    
    print(f"\nStarting Social Media Analysis")
    print(f"Hashtags: {', '.join(hashtags)}")
    print(f"Minimum items per hashtag: {args.min_items}")
    
    # Check API keys
    print(f"\nAPI Keys:")
    print(f"OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")
    
    try:
        # Initialize OpenAI LLM
        model_name = "gpt-3.5-turbo" if args.use_gpt35_fallback else "gpt-4o"
        print(f"\nUsing OpenAI model: {model_name}")
        
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.5,
            max_tokens=1024
        )
        
        # Create web crawler agent
        web_crawler = Agent(
            role="Web Crawler",
            goal="Collect social media data for specified hashtags and convert to CSV",
            backstory="You are a specialized web crawler focused on Instagram data collection and CSV conversion.",
            llm=llm,
            verbose=True
        )
        
        # Create trend analyst agent
        trend_analyst = Agent(
            role="Fashion Trend Analyst",
            goal="Analyze social media data to identify emerging fashion trends",
            backstory="You are an expert in fashion trend analysis with a keen eye for emerging styles.",
            llm=llm,
            verbose=True
        )
        
        # Create data collection task
        data_collection = Task(
            description=f"1. Collect Instagram posts for hashtags: {', '.join(hashtags)}\n2. Minimum {args.min_items} items per hashtag\n3. Convert data to CSV format",
            expected_output="JSON data with collected social media posts and CSV conversion details",
            agent=web_crawler
        )
        
        # Create trend analysis task
        trend_analysis = Task(
            description=f"1. Analyze Instagram data for hashtags: {', '.join(hashtags)}\n2. Identify emerging fashion trends\n3. Generate a comprehensive trend report",
            expected_output="Comprehensive trend analysis report with key insights",
            agent=trend_analyst
        )
        
        # Create and run the crew
        print("\nInitializing Social Media Crew...")
        crew = Crew(
            agents=[web_crawler, trend_analyst],
            tasks=[data_collection, trend_analysis],
            verbose=True,
            process=Process.sequential,
            memory=False  # Disable memory to reduce token usage
        )
        
        print("\nStarting Crew execution...")
        result = crew.kickoff()
        
        # Print the result
        print("\nResult:")
        print(result)
        
        # Save the result as text
        result_str = str(result)
        with open("social_media_analysis_result.txt", "w") as f:
            f.write(result_str)
        print(f"\nResult saved to social_media_analysis_result.txt")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()