# src/agentic_api/api.py

import os
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import crew modules
from .crew import ResearchCrew
from .social_media_crew import SocialMediaCrew

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Agentic API",
    description="API for running AI agent crews for research and social media analysis",
    version="0.1.0"
)

# Define request and response models
class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The topic to research")

class SocialMediaRequest(BaseModel):
    hashtags: List[str] = Field(default=["tech", "ai"], description="The hashtags to analyze")
    min_items_per_hashtag: int = Field(default=25, description="Minimum number of items to collect per hashtag")
    platforms: List[str] = Field(default=["Instagram"], description="Social media platforms to analyze")
    geo_focus: List[str] = Field(default=["North America", "EU"], description="Geographic focus for analysis")
    use_gpt35_fallback: bool = Field(default=False, description="Use GPT-3.5-Turbo instead of GPT-4o to avoid rate limits")
    instagram_account_url: Optional[str] = Field(default="https://www.instagram.com/kentooyamazaki/", description="Instagram account URL to crawl")
    instagram_max_images: int = Field(default=5, description="Maximum number of images to collect from the Instagram account")

class ResearchResponse(BaseModel):
    result: str = Field(..., description="The research report")

class SocialMediaResponse(BaseModel):
    result: str = Field(..., description="The social media analysis result")

# Define API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic API for CrewAI"}

@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Run a research crew on a specific topic"""
    try:
        # Create and run the crew
        crew = ResearchCrew()
        result = crew.build().kickoff(inputs={'topic': request.topic})
        
        # Return the result
        return {"result": result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running research crew: {str(e)}")

@app.post("/api/social-media-analysis", response_model=SocialMediaResponse)
async def run_social_media_analysis(request: SocialMediaRequest, background_tasks: BackgroundTasks):
    """Run a social media trend analysis crew"""
    try:
        # Create inputs dictionary
        inputs = {
            'hashtags': request.hashtags,
            'min_items_per_hashtag': request.min_items_per_hashtag,
            'platforms': request.platforms,
            'geo_focus': request.geo_focus,
            'filters': {'language': 'English', 'nsfw_blocked': True},
            # ZOZO crawler is disabled by setting empty values
            'zozo_categories': [],
            'zozo_gender': [],
            'zozo_brands': [],
            'zozo_min_items_per_category': 0,
            # Instagram settings
            'instagram_account_url': request.instagram_account_url,
            'instagram_max_images': request.instagram_max_images,
            'csv_output_path': 'social_media_data.csv'  # Default CSV output path
        }
        
        # Create and run the crew
        crew = SocialMediaCrew(use_gpt35_fallback=request.use_gpt35_fallback)
        result = crew.build().kickoff(inputs=inputs)
        
        # Return the result
        return {"result": result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running social media analysis crew: {str(e)}")

@app.get("/api/simplified-social-media-analysis")
async def run_simplified_social_media_analysis(
    hashtags: str = Query("ai", description="Comma-separated list of hashtags to analyze"),
    min_items: int = Query(3, description="Minimum items to collect per hashtag"),
    use_gpt35_fallback: bool = Query(False, description="Use GPT-3.5-Turbo instead of GPT-4o")
):
    """Run a simplified social media trend analysis"""
    try:
        # Process hashtags
        hashtag_list = [tag.strip() for tag in hashtags.split(",")]
        
        # Import the simplified social media module
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        
        # Initialize OpenAI LLM
        model_name = "gpt-3.5-turbo" if use_gpt35_fallback else "gpt-4o"
        
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
            description=f"1. Collect Instagram posts for hashtags: {', '.join(hashtag_list)}\n2. Minimum {min_items} items per hashtag\n3. Convert data to CSV format",
            expected_output="JSON data with collected social media posts and CSV conversion details",
            agent=web_crawler
        )
        
        # Create trend analysis task
        trend_analysis = Task(
            description=f"1. Analyze Instagram data for hashtags: {', '.join(hashtag_list)}\n2. Identify emerging fashion trends\n3. Generate a comprehensive trend report",
            expected_output="Comprehensive trend analysis report with key insights",
            agent=trend_analyst
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[web_crawler, trend_analyst],
            tasks=[data_collection, trend_analysis],
            verbose=True,
            process=Process.sequential,
            memory=False  # Disable memory to reduce token usage
        )
        
        result = crew.kickoff()
        
        # Return the result
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running simplified social media analysis: {str(e)}")