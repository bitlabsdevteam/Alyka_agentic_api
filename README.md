# Agentic API

A CrewAI-based API for running AI agent crews for research and social media analysis.

## Installation

### Standard Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your API keys
4. Run the server: `python server.py`

### Docker Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and add your API keys
3. Build and start the containers: `docker-compose up -d`
4. Access the API at `http://localhost:8000`

## Available Crews

### Research Crew

A crew that performs research on a given topic using specialized agents.

**Agents:**
- Researcher: Gathers information on the topic
- Analyst: Analyzes the information and generates a report

**Workflow:**
1. The researcher agent gathers information on the topic
2. The analyst agent analyzes the information and generates a report

**Usage:**
```bash
# API endpoint
POST /api/research

# Request body
{
  "topic": "The impact of AI on healthcare"
}
```

### Social Media Trend Analysis Crew

A crew that analyzes social media trends using specialized agents.

**Agents:**
- Web Crawler: Collects social media data for specified hashtags
- Trend Analyst: Analyzes social media data to identify emerging trends

**Workflow:**
1. The web crawler agent collects social media data for specified hashtags
2. The trend analyst agent analyzes the data and identifies emerging trends

**Usage:**
```bash
# API endpoint
POST /api/social-media-analysis

# Request body
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

## API Endpoints

### Research API

```
POST /api/research
```

Request parameters:
- `topic`: The topic to research

Response:
- `result`: The research report

### Social Media Analysis API

```
POST /api/social-media-analysis
```

Request parameters:
- `hashtags`: List of hashtags to analyze
- `min_items_per_hashtag`: Minimum number of items to collect per hashtag
- `platforms`: List of social media platforms to analyze
- `geo_focus`: Geographic focus for analysis
- `use_gpt35_fallback`: Use GPT-3.5-Turbo instead of GPT-4o
- `instagram_account_url`: Instagram account URL to crawl
- `instagram_max_images`: Maximum number of images to collect

Response:
- `result`: The social media analysis result

### Simplified Social Media Analysis API

```
GET /api/simplified-social-media-analysis
```

Query parameters:
- `hashtags`: Comma-separated list of hashtags to analyze
- `min_items`: Minimum items to collect per hashtag
- `use_gpt35_fallback`: Use GPT-3.5-Turbo instead of GPT-4o

Response:
- `result`: The social media analysis result

## Configuration

Copy `.env.example` to `.env` and add your API keys:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Other LLM providers
# GOOGLE_API_KEY=your_google_api_key_here

# Optional: Tool configurations
SERPER_API_KEY=your_serper_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here

# API Server Configuration
API_PORT=8000
```

## Docker Usage

### Starting the API Server

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### Stopping the API Server

```bash
docker-compose down
```

### Rebuilding the Docker Image

```bash
docker-compose build
```

## Required API Keys

- OpenAI API Key: Required for all crews
- Serper API Key: Required for web search functionality
- Google API Key (optional): Required for Gemini vision and text analysis tools