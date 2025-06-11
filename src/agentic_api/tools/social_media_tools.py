# src/agentic_api/tools/social_media_tools.py

from crewai.tools import BaseTool
from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timedelta
import os

class WebSearchTool(BaseTool):
    """A tool for searching the web using Serper API."""
    
    name: str = "web_search"
    description: str = "Search the web for information about specific hashtags or topics"
    
    def _run(self, query: str, **kwargs: Any) -> str:
        """Run the web search tool.
        
        Args:
            query: The search query
            
        Returns:
            A string with the search results
        """
        # In a real implementation, this would use the Serper API
        # For now, we'll return mock data
        return f"Web search results for '{query}':\n\n" \
               f"1. Recent article about {query} from TechCrunch\n" \
               f"2. Twitter trending topics related to {query}\n" \
               f"3. Reddit discussions about {query}"
    
    async def _arun(self, query: str, **kwargs: Any) -> str:
        """Run the web search tool asynchronously."""
        return self._run(query, **kwargs)


class SocialMediaScraperTool(BaseTool):
    """A tool for scraping social media content using OpenAI."""
    
    name: str = "social_media_scraper"
    description: str = "Extract recent (last 48h) images/text/posts for specified hashtags from Instagram using OpenAI"
    
    def _run(
        self, 
        hashtags: List[str], 
        filters: Dict[str, Any] = {"language": "English", "nsfw_blocked": True},
        min_items_per_hashtag: int = 25,
        **kwargs: Any
    ) -> str:
        """Run the social media scraper tool using OpenAI.
        
        Args:
            hashtags: List of hashtags to search for
            filters: Filters to apply to the search
            min_items_per_hashtag: Minimum number of items to collect per hashtag
            
        Returns:
            A JSON string with the scraped data
        """
        # In a real implementation, this would use OpenAI to analyze Instagram content
        # For now, we'll return mock data
        
        # Generate mock data
        results = []
        for hashtag in hashtags:
            for i in range(min_items_per_hashtag):
                platform = "Instagram"
                content_type = "text" if i % 3 == 0 else "image" if i % 3 == 1 else "video"
                
                # Create a timestamp within the last 48 hours
                hours_ago = i % 48
                timestamp = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
                
                # Generate mock engagement stats
                likes = (i + 1) * 10
                shares = (i + 1) * 5
                comments = (i + 1) * 3
                
                item = {
                    "id": f"{platform.lower()}_{hashtag}_{i}",
                    "url": f"https://{platform.lower()}.com/post/{hashtag}_{i}",
                    "platform": platform,
                    "hashtag": hashtag,
                    "content_type": content_type,
                    "raw_content": f"This is a sample {content_type} post about #{hashtag} on {platform}",
                    "timestamp": timestamp,
                    "engagement_stats": {
                        "likes": likes,
                        "shares": shares,
                        "comments": comments
                    }
                }
                
                results.append(item)
        
        return json.dumps(results, indent=2)
    
    async def _arun(
        self, 
        hashtags: List[str], 
        filters: Dict[str, Any] = {"language": "English", "nsfw_blocked": True},
        min_items_per_hashtag: int = 25,
        **kwargs: Any
    ) -> str:
        """Run the social media scraper tool asynchronously."""
        return self._run(hashtags, filters, min_items_per_hashtag, **kwargs)


class GeminiVisionAnalyzerTool(BaseTool):
    """A tool for analyzing images using Google's Gemini Vision capabilities."""
    
    name: str = "gemini_vision_analyzer"
    description: str = "Analyze images for sentiment, content, virality potential, and fashion elements using Google Gemini"
    
    def _run(self, image_url: str, **kwargs: Any) -> str:
        """Run the Gemini vision analyzer tool.
        
        Args:
            image_url: URL of the image to analyze
            
        Returns:
            A JSON string with the analysis results
        """
        # In a real implementation, this would use Google's Gemini Vision capabilities
        # For now, we'll return mock data
        
        # Generate mock analysis results
        analysis = {
            "image_url": image_url,
            "sentiment": {
                "positive": 0.7,
                "neutral": 0.2,
                "negative": 0.1
            },
            "content_categories": ["technology", "innovation", "digital"],
            "virality_score": 75,
            "key_elements": ["person using device", "modern setting", "bright colors"],
            "attention_hotspots": ["center of image", "device screen", "person's face"],
            # Added fashion elements analysis
            "fashion_elements": {
                "colors": {
                    "primary": ["navy blue", "white"],
                    "secondary": ["gray", "black"],
                    "accent": ["red"],
                    "color_harmony": "complementary"
                },
                "patterns": {
                    "types": ["solid", "minimal"],
                    "prominence": 0.3,
                    "trend_alignment": 0.8
                },
                "fabrics": {
                    "apparent_types": ["cotton", "denim"],
                    "texture": "smooth",
                    "quality_impression": 0.75
                },
                "silhouette": {
                    "shape": "fitted",
                    "structure": "tailored",
                    "proportion": "balanced",
                    "trend_alignment": 0.85
                }
            }
        }
        
        return json.dumps(analysis, indent=2)
    
    async def _arun(self, image_url: str, **kwargs: Any) -> str:
        """Run the Gemini vision analyzer tool asynchronously."""
        return self._run(image_url, **kwargs)


class GeminiTextAnalyzerTool(BaseTool):
    """A tool for analyzing text using Google's Gemini capabilities."""
    
    name: str = "gemini_text_analyzer"
    description: str = "Analyze text posts for sentiment, engagement potential, and key themes using Google Gemini"
    
    def _run(self, text: str, **kwargs: Any) -> str:
        """Run the Gemini text analyzer tool.
        
        Args:
            text: The text to analyze
            
        Returns:
            A JSON string with the analysis results
        """
        # In a real implementation, this would use Google's Gemini text analysis capabilities
        # For now, we'll return mock data
        
        # Generate mock analysis results
        analysis = {
            "text_snippet": text[:100] + "..." if len(text) > 100 else text,
            "sentiment": {
                "positive": 0.6,
                "neutral": 0.3,
                "negative": 0.1
            },
            "engagement_potential": 80,
            "key_themes": ["technology", "innovation", "future"],
            "language_quality": {
                "clarity": 85,
                "persuasiveness": 75,
                "originality": 70
            },
            "audience_appeal": ["tech enthusiasts", "professionals", "early adopters"]
        }
        
        return json.dumps(analysis, indent=2)
    
    async def _arun(self, text: str, **kwargs: Any) -> str:
        """Run the Gemini text analyzer tool asynchronously."""
        return self._run(text, **kwargs)


class ScoreCalculatorTool(BaseTool):
    """A tool for calculating composite impact scores for social media content."""
    
    name: str = "score_calculator"
    description: str = "Calculate composite impact scores (0-100) for social media content including fashion elements"
    
    def _run(
        self, 
        item_data: Dict[str, Any],
        weights: Dict[str, float] = {
            "virality": 0.3,
            "sentiment": 0.2,
            "visual_impact": 0.15,
            "author_influence": 0.05,
            "colors": 0.1,
            "patterns": 0.05,
            "fabrics": 0.05,
            "silhouette": 0.1
        },
        **kwargs: Any
    ) -> str:
        """Run the score calculator tool.
        
        Args:
            item_data: Data about the social media item
            weights: Weights for different factors in the score calculation
            
        Returns:
            A JSON string with the calculated scores
        """
        # In a real implementation, this would calculate scores based on actual data
        # For now, we'll return mock data
        
        # Generate mock score results
        item_id = item_data.get("id", "unknown_item")
        platform = item_data.get("platform", "unknown_platform")
        content_type = item_data.get("content_type", "unknown_type")
        
        # Generate a score based on the item's properties
        base_score = 50
        
        # Adjust score based on platform
        if platform.lower() == "instagram":
            platform_modifier = 15
        else:
            platform_modifier = 0
            
        # Adjust score based on content type
        if content_type.lower() == "image":
            type_modifier = 15
        elif content_type.lower() == "video":
            type_modifier = 20
        else:  # text
            type_modifier = 5
            
        # Calculate fashion elements score if available
        fashion_modifier = 0
        fashion_insights = []
        
        # Check if fashion elements are available in the item data
        if "fashion_elements" in item_data:
            fashion_elements = item_data["fashion_elements"]
            
            # Calculate color impact
            if "colors" in fashion_elements:
                color_harmony = fashion_elements["colors"].get("color_harmony", "")
                if color_harmony in ["complementary", "analogous", "triadic"]:
                    fashion_modifier += 5
                    fashion_insights.append(f"Strong {color_harmony} color harmony")
            
            # Calculate pattern impact
            if "patterns" in fashion_elements:
                pattern_trend = fashion_elements["patterns"].get("trend_alignment", 0)
                if pattern_trend > 0.7:
                    fashion_modifier += 5
                    fashion_insights.append("On-trend pattern design")
            
            # Calculate fabric impact
            if "fabrics" in fashion_elements:
                fabric_quality = fashion_elements["fabrics"].get("quality_impression", 0)
                if fabric_quality > 0.7:
                    fashion_modifier += 5
                    fashion_insights.append("High-quality fabric appearance")
            
            # Calculate silhouette impact
            if "silhouette" in fashion_elements:
                silhouette_trend = fashion_elements["silhouette"].get("trend_alignment", 0)
                if silhouette_trend > 0.8:
                    fashion_modifier += 5
                    fashion_insights.append("Highly trendy silhouette")
        
        # Calculate final score
        final_score = min(100, max(0, base_score + platform_modifier + type_modifier + fashion_modifier))
        
        # Determine trend category based on score
        if final_score >= 80:
            trend_category = "viral"
        elif final_score >= 60:
            trend_category = "trending"
        elif final_score >= 40:
            trend_category = "notable"
        else:
            trend_category = "standard"
            
        # Generate key insights
        key_insights = [
            f"Content performs well on {platform}",
            f"{content_type.capitalize()} format shows strong engagement",
            "Appeals to tech-savvy audience"
        ]
        
        # Add fashion insights if available
        if fashion_insights:
            key_insights.extend(fashion_insights)
        
        # Generate fashion element scores
        fashion_scores = {}
        if "fashion_elements" in item_data:
            fashion_elements = item_data["fashion_elements"]
            
            if "colors" in fashion_elements:
                color_score = min(100, max(0, 50 + (fashion_elements["colors"].get("color_harmony", "") == "complementary") * 30))
                fashion_scores["colors"] = {
                    "score": color_score,
                    "narrative": f"Color palette is {fashion_elements['colors'].get('color_harmony', 'basic')} with {', '.join(fashion_elements['colors'].get('primary', ['neutral']))} as primary colors"
                }
            
            if "patterns" in fashion_elements:
                pattern_score = min(100, max(0, 50 + int(fashion_elements["patterns"].get("trend_alignment", 0) * 50)))
                fashion_scores["patterns"] = {
                    "score": pattern_score,
                    "narrative": f"Pattern style is {', '.join(fashion_elements['patterns'].get('types', ['basic']))} with {int(fashion_elements['patterns'].get('trend_alignment', 0) * 100)}% trend alignment"
                }
            
            if "fabrics" in fashion_elements:
                fabric_score = min(100, max(0, 50 + int(fashion_elements["fabrics"].get("quality_impression", 0) * 50)))
                fashion_scores["fabrics"] = {
                    "score": fabric_score,
                    "narrative": f"Apparent fabric is {', '.join(fashion_elements['fabrics'].get('apparent_types', ['standard']))} with {fashion_elements['fabrics'].get('texture', 'medium')} texture"
                }
            
            if "silhouette" in fashion_elements:
                silhouette_score = min(100, max(0, 50 + int(fashion_elements["silhouette"].get("trend_alignment", 0) * 50)))
                fashion_scores["silhouette"] = {
                    "score": silhouette_score,
                    "narrative": f"Silhouette is {fashion_elements['silhouette'].get('shape', 'standard')} and {fashion_elements['silhouette'].get('structure', 'basic')} with {int(fashion_elements['silhouette'].get('trend_alignment', 0) * 100)}% trend alignment"
                }
        
        result = {
            item_id: {
                "score": final_score,
                "trend_category": trend_category,
                "key_insights": key_insights,
                "fashion_element_scores": fashion_scores
            }
        }
        
        return json.dumps(result, indent=2)
    
    async def _arun(
        self, 
        item_data: Dict[str, Any],
        weights: Dict[str, float] = {
            "virality": 0.3,
            "sentiment": 0.2,
            "visual_impact": 0.15,
            "author_influence": 0.05,
            "colors": 0.1,
            "patterns": 0.05,
            "fabrics": 0.05,
            "silhouette": 0.1
        },
        **kwargs: Any
    ) -> str:
        """Run the score calculator tool asynchronously."""
        return self._run(item_data, weights, **kwargs)


# ZOZOScraperTool has been removed as per requirements


# Add a new tool for crawling Kento Yamazaki's Instagram account

class InstagramAccountCrawlerTool(BaseTool):
    """A tool for crawling a specific Instagram account."""
    
    name: str = "instagram_account_crawler"
    description: str = "Extract images from a specific Instagram account with a maximum limit"
    
    def _run(
        self, 
        account_url: str = "https://www.instagram.com/kentooyamazaki/",
        max_images: int = 5,
        **kwargs: Any
    ) -> str:
        """Run the Instagram account crawler tool.
        
        Args:
            account_url: URL of the Instagram account to crawl
            max_images: Maximum number of images to collect
            
        Returns:
            A JSON string with the scraped data
        """
        # In a real implementation, this would use web scraping to extract images from the Instagram account
        # For now, we'll return mock data
        
        # Extract username from URL
        username = account_url.strip('/').split('/')[-1]
        
        # Generate mock data
        results = []
        for i in range(max_images):
            # Create a timestamp within the last week
            days_ago = i % 7
            timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
            
            # Generate mock engagement stats
            likes = (i + 1) * 10000 + 5000  # Kento is popular!
            comments = (i + 1) * 500 + 200
            
            # Create mock image data
            image = {
                "id": f"instagram_{username}_{i}",
                "url": f"https://instagram.com/{username}/post_{i}",
                "platform": "Instagram",
                "account": username,
                "content_type": "image",
                "image_url": f"https://instagram.com/{username}/images/post_{i}.jpg",
                "caption": f"Post caption #{i+1} from {username}'s Instagram",
                "timestamp": timestamp,
                "engagement_stats": {
                    "likes": likes,
                    "comments": comments
                },
                "tags": ["actor", "japanese", "entertainment", "celebrity"]
            }
            
            results.append(image)
        
        return json.dumps(results, indent=2)
    
    async def _arun(
        self, 
        account_url: str = "https://www.instagram.com/kentooyamazaki/",
        max_images: int = 5,
        **kwargs: Any
    ) -> str:
        """Run the Instagram account crawler tool asynchronously."""
        return self._run(account_url, max_images, **kwargs)


# Add a new tool for CSV conversion

class DatasetToCSVTool(BaseTool):
    """A tool for converting dataset to CSV format."""
    
    name: str = "dataset_to_csv"
    description: str = "Convert collected data from JSON to CSV format for easier analysis and sharing"
    
    def _run(
        self, 
        data: str,
        output_path: str = "social_media_data.csv",
        **kwargs: Any
    ) -> str:
        """Run the dataset to CSV conversion tool.
        
        Args:
            data: JSON string containing the dataset to convert
            output_path: Path where the CSV file should be saved
            
        Returns:
            A string with the path to the saved CSV file and summary statistics
        """
        # In a real implementation, this would convert JSON data to CSV and save it
        # For now, we'll return mock data
        
        try:
            # Parse the JSON data
            json_data = json.loads(data)
            
            # Count the number of items by platform/source
            platform_counts = {}
            for item in json_data:
                platform = item.get('platform', 'unknown')
                if platform in platform_counts:
                    platform_counts[platform] += 1
                else:
                    platform_counts[platform] = 1
            
            # Generate mock CSV conversion result
            result = {
                "status": "success",
                "output_path": output_path,
                "total_items": len(json_data),
                "platform_distribution": platform_counts,
                "columns": [
                    "id", "url", "platform", "content_type", "timestamp", 
                    "likes", "shares", "comments", "score", "trend_category"
                ],
                "sample_rows": 5,
                "file_size_kb": round(len(data) * 0.2 / 1024, 2)  # Rough estimate of CSV file size
            }
            
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            return json.dumps({
                "status": "error",
                "message": "Invalid JSON data provided",
                "output_path": None
            }, indent=2)
    
    async def _arun(
        self, 
        data: str,
        output_path: str = "social_media_data.csv",
        **kwargs: Any
    ) -> str:
        """Run the dataset to CSV conversion tool asynchronously."""
        return self._run(data, output_path, **kwargs)