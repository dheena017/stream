"""
AI Brain Module - Combines multiple AI models and internet knowledge
"""
import asyncio
from typing import List, Dict, Optional, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AIBrain:
    """
    Meta-AI system that combines responses from multiple models and internet sources
    """
    
    def __init__(self):
        self.conversation_memory = []
        self.internet_enabled = True
        
    def search_internet(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search the internet using DuckDuckGo"""
        try:
            from duckduckgo_search import DDGS  # type: ignore
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=num_results):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', '')
                    })
            return results
        except ImportError:
            logger.warning("DuckDuckGo search not available.")
            return [{"error": "DuckDuckGo search not available. Install: pip install duckduckgo-search"}]
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return [{"error": f"Search failed: {str(e)}"}]
    
    def scrape_webpage(self, url: str) -> str:
        """Extract text content from a webpage"""
        try:
            import requests  # type: ignore
            from bs4 import BeautifulSoup  # type: ignore
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 2000 characters
            return text[:2000]
        except Exception as e:
            logger.error(f"Failed to scrape webpage: {str(e)}")
            return f"Failed to scrape webpage: {str(e)}"
    
    def gather_internet_context(self, query: str) -> str:
        """Gather context from internet for the query"""
        if not self.internet_enabled:
            return ""
        
        # Search internet
        search_results = self.search_internet(query, num_results=3)
        
        context = "\n\n--- INTERNET KNOWLEDGE ---\n"
        
        for i, result in enumerate(search_results, 1):
            if 'error' in result:
                context += f"Search error: {result['error']}\n"
                continue
                
            context += f"\n{i}. {result['title']}\n"
            context += f"   {result['snippet']}\n"
            context += f"   Source: {result['url']}\n"
        
        return context
    
    async def query_model(
        self,
        provider: str,
        model_name: str,
        prompt: str,
        api_key: str,
        config: Dict[str, Any]
    ) -> Dict[str, str]:
        """Query a single AI model"""
        try:
                        # Validate prompt is not empty
            if not prompt or not prompt.strip():
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": "Error: Prompt cannot be empty",
                    "success": False
                }
            if provider == "google":
                from google import genai
                client = genai.Client(api_key=api_key)
                
                # New SDK doesn't accept config dict directly
                response = client.models.generate_content(
                    model=model_name,
                    contents=[{"role": "user", "parts": [{"text": prompt}]}]
                )
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.text,
                    "success": True
                }
            
            elif provider in ["openai", "together", "xai", "deepseek"]:
                from openai import OpenAI
                
                base_urls = {
                    "together": "https://api.together.xyz/v1",
                    "xai": "https://api.x.ai/v1",
                    "deepseek": "https://api.deepseek.com"
                }
                
                client = OpenAI(
                    api_key=api_key,
                    base_url=base_urls.get(provider)
                )
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.get("temperature", 0.7),
                    max_tokens=config.get("max_output_tokens", 1024)
                )
                
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.choices[0].message.content,
                    "success": True
                }
            
            elif provider == "anthropic":
                from anthropic import Anthropic
                client = Anthropic(api_key=api_key)
                
                response = client.messages.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=config.get("max_output_tokens", 1024),
                    temperature=config.get("temperature", 0.7)
                )
                
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.content[0].text,
                    "success": True
                }
                
        except Exception as e:
            return {
                "provider": provider,
                "model": model_name,
                "response": f"Error: {str(e)}",
                "success": False
            }
    
    async def query_multiple_models(
        self,
        query: str,
        models: List[Dict[str, Any]],
        config: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Query multiple AI models in parallel"""
        tasks = []
        for model_info in models:
            task = self.query_model(
                provider=model_info["provider"],
                model_name=model_info["model"],
                prompt=query,
                api_key=model_info["api_key"],
                config=config
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    def synthesize_responses(
        self,
        query: str,
        model_responses: List[Dict[str, str]],
        internet_context: str
    ) -> str:
        """Synthesize multiple AI responses and internet knowledge into a unified answer"""
        
        synthesis = f"# AI Brain Synthesis\n\n"
        synthesis += f"**Your Question:** {query}\n\n"
        
        # Add internet context if available
        if internet_context and internet_context.strip():
            synthesis += f"## Internet Knowledge\n{internet_context}\n\n"
        
        # Add model responses
        synthesis += "## AI Model Responses\n\n"
        
        successful_responses = [r for r in model_responses if r.get("success")]
        
        for i, response in enumerate(successful_responses, 1):
            synthesis += f"### {i}. {response['provider'].upper()} - {response['model']}\n"
            synthesis += f"{response['response']}\n\n"
        
        # Add failed models if any
        failed_responses = [r for r in model_responses if not r.get("success")]
        if failed_responses:
            synthesis += "\n## Failed Queries\n"
            for response in failed_responses:
                synthesis += f"- {response['provider']}/{response['model']}: {response['response']}\n"
        
        # Add summary
        synthesis += "\n---\n\n"
        synthesis += f"**Total models consulted:** {len(model_responses)}\n"
        synthesis += f"**Successful responses:** {len(successful_responses)}\n"
        synthesis += f"**Internet search:** {'✓ Enabled' if internet_context else '✗ Disabled'}\n"
        
        return synthesis
    
    def add_to_memory(self, query: str, response: str):
        """Store conversation in memory"""
        self.conversation_memory.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response
        })
        
        # Keep only last 100 interactions
        if len(self.conversation_memory) > 100:
            self.conversation_memory = self.conversation_memory[-100:]
    
    def export_memory(self) -> str:
        """Export conversation memory as JSON"""
        return json.dumps(self.conversation_memory, indent=2)
    
    def get_memory_summary(self) -> str:
        """Get a summary of stored memories"""
        if not self.conversation_memory:
            return "No memories stored yet."
        
        summary = f"Total memories: {len(self.conversation_memory)}\n"
        summary += f"First memory: {self.conversation_memory[0]['timestamp']}\n"
        summary += f"Latest memory: {self.conversation_memory[-1]['timestamp']}\n"
        
        return summary
