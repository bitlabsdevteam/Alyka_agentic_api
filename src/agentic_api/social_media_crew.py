# src/agentic_api/social_media_crew.py

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
import os
# Fix import path
try:
    from src.agentic_api.tools.social_media_tools import WebSearchTool, SocialMediaScraperTool, GeminiVisionAnalyzerTool, GeminiTextAnalyzerTool, ScoreCalculatorTool, InstagramAccountCrawlerTool, DatasetToCSVTool
except ModuleNotFoundError:
    # Try relative import if absolute import fails
    from tools.social_media_tools import WebSearchTool, SocialMediaScraperTool, GeminiVisionAnalyzerTool, GeminiTextAnalyzerTool, ScoreCalculatorTool, InstagramAccountCrawlerTool, DatasetToCSVTool

@CrewBase
class SocialMediaCrew:
    """A crew that analyzes social media trends using specialized agents."""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Paths to YAML configuration files with absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_config = os.path.join(base_dir, 'config/social_media_agents.yaml')
    tasks_config = os.path.join(base_dir, 'config/social_media_tasks.yaml')

    @before_kickoff
    def prepare_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs before the crew starts."""
        # Validate hashtags input
        if 'hashtags' not in inputs or not inputs['hashtags']:
            inputs['hashtags'] = ['tech', 'ai']  # Default hashtags
        
        # Set default parameters if not provided
        if 'min_items_per_hashtag' not in inputs:
            inputs['min_items_per_hashtag'] = 25
            
        if 'platforms' not in inputs:
            inputs['platforms'] = ['Instagram']  # Default to Instagram only
            
        if 'filters' not in inputs:
            inputs['filters'] = {'language': 'English', 'nsfw_blocked': True}
            
        if 'geo_focus' not in inputs:
            inputs['geo_focus'] = ['North America', 'EU']
            
        # Set default parameters for ZOZO.jp scraping (disabled by default)
        if 'zozo_categories' not in inputs:
            inputs['zozo_categories'] = []
            
        if 'zozo_gender' not in inputs:
            inputs['zozo_gender'] = []
            
        if 'zozo_brands' not in inputs:
            inputs['zozo_brands'] = []
            
        if 'zozo_min_items_per_category' not in inputs:
            inputs['zozo_min_items_per_category'] = 0
            
        # Set default parameters for Instagram account crawler
        if 'instagram_account_url' not in inputs:
            inputs['instagram_account_url'] = 'https://www.instagram.com/kentooyamazaki/'
            
        if 'instagram_max_images' not in inputs:
            inputs['instagram_max_images'] = 5
            
        # Set default parameter for CSV output path
        if 'csv_output_path' not in inputs:
            inputs['csv_output_path'] = 'social_media_data.csv'
            
        return inputs

    @after_kickoff
    def process_output(self, output):
        """Process output after the crew finishes."""
        # Format the final output if needed
        return output

    @agent
    def web_crawler(self) -> Agent:
        """Create the web crawler agent."""
        # Create tools list - ZOZO crawler is removed
        tools = [
            WebSearchTool(),
            SocialMediaScraperTool(),
            InstagramAccountCrawlerTool(),  # Only Instagram crawler is active
            DatasetToCSVTool()
        ]
        
        # Create agent with tools
        web_crawler_config = self.agents_config['web_crawler']
        agent = Agent(
            role=web_crawler_config['role'],
            goal=web_crawler_config['goal'],
            backstory=web_crawler_config['backstory'],
            llm=web_crawler_config['llm'],
            verbose=True,
            tools=tools
        )
        
        return agent

    @agent
    def trend_analyst(self) -> Agent:
        """Create the trend analyst agent."""
        # Create tools list
        tools = [
            GeminiVisionAnalyzerTool(),
            GeminiTextAnalyzerTool(),
            ScoreCalculatorTool()
        ]
        
        # Create agent with tools
        trend_analyst_config = self.agents_config['trend_analyst']
        agent = Agent(
            role=trend_analyst_config['role'],
            goal=trend_analyst_config['goal'],
            backstory=trend_analyst_config['backstory'],
            llm=trend_analyst_config['llm'],
            verbose=True,
            tools=tools
        )
        
        return agent

    @task
    def data_collection_task(self) -> Task:
        """Create the task for crawling social media."""
        data_collection_config = self.tasks_config['data_collection_task']
        return Task(
            description=data_collection_config['description'],
            expected_output=data_collection_config['expected_output'],
            agent=self.web_crawler
        )

    @task
    def trend_analysis_task(self) -> Task:
        """Create the task for analyzing trends."""
        trend_analysis_config = self.tasks_config['trend_analysis_task']
        return Task(
            description=trend_analysis_config['description'],
            expected_output=trend_analysis_config['expected_output'],
            agent=self.trend_analyst
        )

    @crew
    def build(self) -> Crew:
        """Build the crew with the agents and tasks."""
        return Crew(
            agents=[self.web_crawler, self.trend_analyst],
            tasks=[self.data_collection_task, self.trend_analysis_task],
            verbose=2,
            process=Process.sequential,
            max_rpm=10,  # Limit requests per minute to avoid rate limits
            memory=False  # Disable memory to reduce token usage
        )