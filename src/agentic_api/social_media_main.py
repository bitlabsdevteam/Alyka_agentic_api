# src/agentic_api/social_media_main.py

import os
import argparse
import json
from dotenv import load_dotenv
# Fix import path
try:
    from src.agentic_api.social_media_crew import SocialMediaCrew
except ModuleNotFoundError:
    # Try relative import if absolute import fails
    from social_media_crew import SocialMediaCrew

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the social media trend analysis crew."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run a social media trend analysis crew')
    parser.add_argument('--hashtags', type=str, nargs='+', default=['tech', 'ai'],
                        help='The hashtags to analyze (default: tech ai)')
    parser.add_argument('--min-items', type=int, default=25,
                        help='Minimum number of items to collect per hashtag (default: 25)')
    parser.add_argument('--platforms', type=str, nargs='+', default=['Instagram'],
                        help='Social media platforms to analyze (default: Instagram)')
    parser.add_argument('--geo-focus', type=str, nargs='+', default=['North America', 'EU'],
                        help='Geographic focus for analysis (default: North America EU)')
    parser.add_argument('--output', type=str, default='trend_report.json',
                        help='Output file for the trend report (default: trend_report.json)')
    
    # Add ZOZO.jp specific arguments (kept for compatibility but will be disabled)
    parser.add_argument('--zozo-categories', type=str, nargs='+', default=['tops', 'shoes', 'pants'],
                        help='ZOZO.jp apparel categories to crawl (default: tops shoes pants)')
    parser.add_argument('--zozo-gender', type=str, nargs='+', default=['men', 'women', 'kids'],
                        help='ZOZO.jp gender sections to crawl (default: men women kids)')
    parser.add_argument('--zozo-brands', type=str, nargs='+', default=[],
                        help='Specific brands to filter on ZOZO.jp (default: all brands)')
    parser.add_argument('--zozo-min-items', type=int, default=10,
                        help='Minimum number of items to collect per ZOZO.jp category (default: 10)')
    
    # Add Instagram account crawler specific arguments
    parser.add_argument('--instagram-account', type=str, default='https://www.instagram.com/kentooyamazaki/',
                        help='Instagram account URL to crawl (default: https://www.instagram.com/kentooyamazaki/)')
    parser.add_argument('--instagram-max-images', type=int, default=5,
                        help='Maximum number of images to collect from the Instagram account (default: 5)')
    
    # Add argument for CSV output path
    parser.add_argument(
        '--csv-output-path',
        type=str,
        default='social_media_data.csv',
        help='Path where the CSV file should be saved'
    )
    
    # Add argument for using GPT-3.5-Turbo as a fallback model
    parser.add_argument(
        '--use-gpt35-fallback',
        action='store_true',
        help='Use GPT-3.5-Turbo instead of GPT-4o to avoid rate limits'
    )
    args = parser.parse_args()
    
    # Create inputs dictionary
    inputs = {
        'hashtags': args.hashtags,
        'min_items_per_hashtag': args.min_items,
        'platforms': ['Instagram'],  # Only use Instagram
        'geo_focus': args.geo_focus,
        'filters': {'language': 'English', 'nsfw_blocked': True},
        # ZOZO crawler is disabled by setting empty values
        'zozo_categories': [],
        'zozo_gender': [],
        'zozo_brands': [],
        'zozo_min_items_per_category': 0,
        # Instagram settings
        'instagram_account_url': args.instagram_account,
        'instagram_max_images': 5,  # Hard limit to 5 images as requested
        'csv_output_path': args.csv_output_path  # Add CSV output path
    }
    
    # Print execution information
    print(f"\nStarting Social Media Analysis (Instagram Only)")
    print(f"Hashtags: {', '.join(inputs['hashtags'])}")
    print(f"Platforms: {', '.join(inputs['platforms'])}")
    print(f"Minimum items per hashtag: {inputs['min_items_per_hashtag']}")
    print(f"Geographic focus: {', '.join(inputs['geo_focus'])}")
    
    # ZOZO crawler is disabled
    print(f"\nZOZO.jp Crawling: DISABLED")
    
    print(f"\nInstagram Account Crawling Configuration:")
    print(f"Account URL: {inputs['instagram_account_url']}")
    print(f"Maximum images: {inputs['instagram_max_images']} (Limited to 5 records as requested)")
    print(f"\nCSV Output Configuration:")
    print(f"CSV Output Path: {inputs['csv_output_path']}")
    print("\n" + "-"*50 + "\n")
    
    # Create agents directly
    from src.agentic_api.tools.social_media_tools import WebSearchTool, SocialMediaScraperTool, GeminiVisionAnalyzerTool, GeminiTextAnalyzerTool, ScoreCalculatorTool, InstagramAccountCrawlerTool, DatasetToCSVTool
    from crewai import Agent, Task, Crew, Process
    from crewai.llm import LLM
    import yaml
    import os
    
    # Load agent and task configurations
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, 'config/social_media_agents.yaml'), 'r') as f:
        agents_config = yaml.safe_load(f)
    with open(os.path.join(base_dir, 'config/social_media_tasks.yaml'), 'r') as f:
        tasks_config = yaml.safe_load(f)
        
    # Initialize LLMs with optimized settings and debugging
    try:
        # Use GPT-3.5-Turbo as fallback if specified
        openai_model = "openai/gpt-3.5-turbo" if args.use_gpt35_fallback else "openai/gpt-4o"
        print(f"Using OpenAI model: {openai_model}")
        
        print("API Keys:")
        print(f"OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")
        print(f"Google Gemini API Key: {'Set' if os.getenv('GOOGLE_GEMINI_API_KEY') else 'Not Set'}")
        
        # Use OpenAI model for both agents since Gemini API has quota issues
        openai_llm = LLM(
            model=openai_model,
            temperature=0.5,  # Lower temperature for more focused responses
            streaming=True,   # Enable streaming to reduce latency and token usage
            max_tokens=1024   # Limit token generation to reduce usage
        )
        # Use OpenAI model for both agents
        gemini_llm = openai_llm  # Use the same OpenAI LLM for both agents
        
        # Create web crawler agent
        web_crawler = Agent(
            role=agents_config['web_crawler']['role'],
            goal=agents_config['web_crawler']['goal'],
            backstory=agents_config['web_crawler']['backstory'],
            llm=openai_llm,  # Use the initialized OpenAI LLM
            verbose=True,
            tools=[
                WebSearchTool(),
                SocialMediaScraperTool(),
                InstagramAccountCrawlerTool(),
                DatasetToCSVTool()
            ]
        )
        
        # Create trend analyst agent
        trend_analyst = Agent(
            role=agents_config['trend_analyst']['role'],
            goal=agents_config['trend_analyst']['goal'],
            backstory=agents_config['trend_analyst']['backstory'],
            llm=gemini_llm,  # Use the initialized Gemini LLM
            verbose=True,
            tools=[
                GeminiVisionAnalyzerTool(),
                GeminiTextAnalyzerTool(),
                ScoreCalculatorTool()
            ]
        )
        
        # Create tasks
        data_collection = Task(
            description=tasks_config['data_collection_task']['description'],
            expected_output=tasks_config['data_collection_task']['expected_output'],
            agent=web_crawler
        )
        
        trend_analysis = Task(
            description=tasks_config['trend_analysis_task']['description'],
            expected_output=tasks_config['trend_analysis_task']['expected_output'],
            agent=trend_analyst
        )
        
        # Create and run the crew with optimized settings
        print("\nInitializing Social Media Crew...")
        crew = Crew(
            agents=[web_crawler, trend_analyst],
            tasks=[data_collection, trend_analysis],
            verbose=True,
            process=Process.sequential,
            max_rpm=10,  # Limit requests per minute to avoid rate limits
            memory=False  # Disable memory to reduce token usage
        )
        
        print("\nStarting Crew execution...")
        try:
            result = crew.kickoff(inputs=inputs)
        except Exception as e:
            print(f"\nError during crew execution: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
    except Exception as e:
        print(f"\nError during initialization: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise
    
    # Print the result summary
    print("\nInstagram Analysis Complete!")
    print("\nSummary:")
    
    # Extract and print key information from the result
    try:
        # Try to parse the result as JSON
        result_data = json.loads(result.raw)
        
        # Print top items if available
        if 'top_items' in result_data:
            print("\nTop Trending Items:")
            for i, item in enumerate(result_data['top_items'][:5]):
                print(f"{i+1}. {item['title']} - Score: {item['score']}")
        
        # Print key insights if available
        if 'key_insights' in result_data:
            print("\nKey Insights:")
            for i, insight in enumerate(result_data['key_insights']):
                print(f"{i+1}. {insight}")
        
        # Print platform breakdown if available
        if 'platform_breakdown' in result_data:
            print("\nPlatform Breakdown:")
            for platform, stats in result_data['platform_breakdown'].items():
                print(f"{platform}: {stats['item_count']} items, Avg Score: {stats['avg_score']}")
        
        # Save the full result to the output file
        output_file = args.output
        with open(output_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        print(f"\nFull report saved to {output_file}")
        
    except (json.JSONDecodeError, AttributeError):
        # If the result is not valid JSON or doesn't have the expected structure
        print("\nRaw result:")
        print(result)

if __name__ == "__main__":
    main()