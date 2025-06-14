# src/agentic_api/api.py

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import crew modules
from .crew import ResearchCrew
from .social_media_crew import SocialMediaCrew

# Import authentication modules
from .auth import (
    get_current_active_user, 
    get_cognito_login_url, 
    get_cognito_logout_url,
    exchange_code_for_tokens,
    create_access_token,
    User,
    Token
)
from .middleware import get_auth_middleware

# Load environment variables
load_dotenv()

# Get the directory of the current file
CURRENT_DIR = Path(__file__).parent
STATIC_DIR = CURRENT_DIR / "static"

# Initialize FastAPI app
app = FastAPI(
    title="Agentic API",
    description="API for running AI agent crews for research and social media analysis",
    version="0.1.0"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Add authentication middleware
app.add_middleware(get_auth_middleware())

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
async def root(request: Request):
    # Check if user is authenticated by looking for the access_token cookie
    access_token = request.cookies.get("access_token")
    
    if access_token and access_token.startswith("Bearer "):
        # User is authenticated, return welcome message
        return {"message": "Welcome to the Agentic API for CrewAI", "authenticated": True}
    else:
        # User is not authenticated, serve the login page
        return FileResponse(STATIC_DIR / "login.html")

# Authentication endpoints
@app.get("/auth/login")
async def login():
    """Redirect to Cognito hosted UI for login"""
    return RedirectResponse(url=get_cognito_login_url())

@app.get("/auth/callback")
async def callback(code: str, request: Request, response: Response):
    """Handle the callback from Cognito after successful authentication"""
    try:
        # Exchange the authorization code for tokens
        tokens = await exchange_code_for_tokens(code)
        
        # Create our own JWT token
        access_token, expires_at = create_access_token(
            data={"sub": "user123"}  # In a real app, this would be the user ID from Cognito
        )
        
        # Set the token in a cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=1800,  # 30 minutes
            expires=1800,
            path="/",
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        # Redirect to the home page
        return RedirectResponse(url="/")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

@app.get("/auth/logout")
async def logout(response: Response):
    """Log out the user"""
    # Clear the token cookie
    response.delete_cookie(key="access_token", path="/")
    
    # Redirect to Cognito logout
    return RedirectResponse(url=get_cognito_logout_url())

@app.get("/auth/me", response_model=User)
async def get_user(current_user: User = Depends(get_current_active_user)):
    """Get the current user's information"""
    return current_user

@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_active_user)):
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
async def run_social_media_analysis(request: SocialMediaRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_active_user)):
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
    use_gpt35_fallback: bool = Query(False, description="Use GPT-3.5-Turbo instead of GPT-4o"),
    current_user: User = Depends(get_current_active_user)
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