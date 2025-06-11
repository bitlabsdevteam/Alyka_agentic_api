# Agentic API

A collection of CrewAI-based multi-agent systems for various tasks, accessible via API endpoints.

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -e .`
5. Copy `.env.example` to `.env` and add your API keys

## API Server

The project includes a FastAPI server that exposes the agent crews as API endpoints.

### Starting the API Server

```bash
python server.py
```

By default, the server runs on port 8000. You can change this by setting the `API_PORT` environment variable in your `.env` file.

### API Endpoints

#### Research Crew

```
POST /api/research
```

Request body:
```json
{
  "topic": "Quantum Computing"
}
```

Response:
```json
{
  "result": "Comprehensive research report on Quantum Computing..."
}
```

#### Social Media Analysis Crew

```
POST /api/social-media-analysis
```

Request body:
```json
{
  "hashtags": ["tech", "ai"],
  "min_items_per_hashtag": 25,
  "platforms": ["Instagram"],
  "geo_focus": ["North America", "EU"],
  "use_gpt35_fallback": false,
  "instagram_account_url": "https://www.instagram.com/kentooyamazaki/",
  "instagram_max_images": 5
}
```

Response:
```json
{
  "result": "Detailed social media trend analysis..."
}
```

#### Simplified Social Media Analysis

```
GET /api/simplified-social-media-analysis?hashtags=ai,tech&min_items=3&use_gpt35_fallback=false
```

Query parameters:
- `hashtags`: Comma-separated list of hashtags to analyze (default: "ai")
- `min_items`: Minimum items to collect per hashtag (default: 3)
- `use_gpt35_fallback`: Use GPT-3.5-Turbo instead of GPT-4o (default: false)

Response:
```json
{
  "result": "Simplified social media trend analysis..."
}
```

## Available Crews

### Research Crew

A crew that researches a topic and creates a comprehensive report.

#### Usage

```bash
python -m src.agentic_api.main --topic "Quantum Computing"
```

### Social Media Trend Analysis Crew

A multi-agent system with two specialized agents that sequentially analyze social media trends using OpenAI for crawling and Google Gemini for analysis.

#### Agents

1. **Web Crawler Agent**
   - Role: Social Media Content Collector
   - Goal: Extract recent (last 48h) images/text/posts for specified hashtags
   - Tools:
     - `web_search` (Serper API)
     - Custom `social_media_scraper` (using OpenAI)
   - LLM: OpenAI GPT-4-Turbo

2. **Trend Analyst Agent**
   - Role: Multimodal Impact Evaluator
   - Goal: Generate composite impact scores (0-100) using Gemini's multimodal capabilities
   - Tools:
     - `gemini_vision_analyzer` for image sentiment/virality
     - `gemini_text_analyzer` for post sentiment/engagement
     - Custom `score_calculator` with weighted scoring
   - LLM: Google Gemini Pro Vision

#### Workflow

1. **Data Collection Phase**
   - Web Crawler Agent collects social media content for specified hashtags
   - Outputs a structured dataset with URLs, content type, raw content, and engagement statistics

2. **Trend Analysis Phase**
   - Trend Analyst Agent analyzes the collected data
   - Produces a comprehensive trend report with top items, comparison matrix, anomalies, and visual highlights

#### Usage

```bash
python -m src.agentic_api.social_media_main --hashtags tech ai --min-items 25 --platforms Twitter Instagram Reddit
```

#### Additional Options

- `--hashtags`: Space-separated list of hashtags to analyze (default: tech ai)
- `--min-items`: Minimum number of items to collect per hashtag (default: 25)
- `--platforms`: Social media platforms to analyze (default: Twitter Instagram Reddit)
- `--geo-focus`: Geographic focus for analysis (default: North America EU)
- `--output`: Output file for the trend report (default: trend_report.json)

## Configuration

All crews use YAML configuration files for agents and tasks, located in the `src/agentic_api/config` directory.

## API Keys

The following API keys are required:

- `OPENAI_API_KEY`: For the Research Crew (using GPT-4o) and Web Crawler Agent
- `GOOGLE_GEMINI_API_KEY`: For the Trend Analyst Agent (using Gemini Pro Vision)

Optional API keys:

- `SERPER_API_KEY`: For web search functionality
- `TAVILY_API_KEY`: For additional search capabilities