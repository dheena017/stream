"""
AI Brain Module - Combines multiple AI models and internet knowledge
"""

import asyncio
import json
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from ui.ethics import EthicsGuardian
=======
from typing import Any, Dict, List
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
import logging
>>>>>>> origin/code-review-security-fixes-5343699314450815094
from datetime import datetime
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Any, Dict, List, Optional
=======
import streamlit as st


@st.cache_data(ttl=3600)
def _scrape_webpage_cached(url: str) -> str:
    """Extract text content from a webpage (cached)"""
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
        return f"Failed to scrape webpage: {str(e)}"
>>>>>>> performance-optimization-13534932852089819512
=======
import streamlit as st
>>>>>>> origin/performance-optimizations-caching-2508816788705387048

logger = logging.getLogger(__name__)
=======
import time
from datetime import datetime
from monitoring import get_monitor
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949


class AIBrain:
    """
    Meta-AI system that combines responses from multiple models and internet sources
    """

    def __init__(self):
        self.conversation_memory = []
        self.internet_enabled = True
<<<<<<< HEAD

    def search_internet(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
=======
        
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner=False)
    def search_internet(query: str, num_results: int = 5) -> List[Dict[str, str]]:
>>>>>>> origin/performance-optimizations-caching-2508816788705387048
        """Search the internet using DuckDuckGo"""
        try:
            from duckduckgo_search import DDGS  # type: ignore

            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=num_results):
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("href", ""),
                            "snippet": result.get("body", ""),
                        }
                    )
            return results
        except ImportError:
<<<<<<< HEAD
            return [
                {
                    "error": "DuckDuckGo search not available. Install: pip install duckduckgo-search"
                }
            ]
=======
            logger.warning("DuckDuckGo search not available.")
            return [{"error": "DuckDuckGo search not available. Install: pip install duckduckgo-search"}]
>>>>>>> origin/code-review-security-fixes-5343699314450815094
        except Exception as e:
<<<<<<< HEAD
            logger.error(f"Search failed: {str(e)}")
=======
            logger.error(f"Internet search failed: {e}")
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
            return [{"error": f"Search failed: {str(e)}"}]
<<<<<<< HEAD

    def scrape_webpage(self, url: str) -> str:
=======
    
    @staticmethod
    @st.cache_data(ttl=86400, show_spinner=False)
    def scrape_webpage(url: str) -> str:
>>>>>>> origin/performance-optimizations-caching-2508816788705387048
        """Extract text content from a webpage"""
<<<<<<< HEAD
        try:
            import requests  # type: ignore
            from bs4 import BeautifulSoup  # type: ignore

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            # Limit to first 2000 characters
            return text[:2000]
        except Exception as e:
<<<<<<< HEAD
            logger.error(f"Failed to scrape webpage: {str(e)}")
=======
            logger.error(f"Webpage scraping failed: {e}")
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
            return f"Failed to scrape webpage: {str(e)}"

=======
        return _scrape_webpage_cached(url)
    
>>>>>>> performance-optimization-13534932852089819512
    def gather_internet_context(self, query: str) -> str:
        """Gather context from internet for the query"""
        if not self.internet_enabled:
            return ""

        # Search internet
        search_results = self.search_internet(query, num_results=3)
<<<<<<< HEAD

        context = "\n\n--- INTERNET KNOWLEDGE ---\n"

        for i, result in enumerate(search_results, 1):
            if "error" in result:
                context += f"Search error: {result['error']}\n"
                continue

            context += f"\n{i}. {result['title']}\n"
            context += f"   {result['snippet']}\n"
            context += f"   Source: {result['url']}\n"

        return context
=======
        
        context_parts = ["\n\n--- INTERNET KNOWLEDGE ---\n"]
        
        for i, result in enumerate(search_results, 1):
            if 'error' in result:
                context_parts.append(f"Search error: {result['error']}\n")
                continue
                
            context_parts.append(f"\n{i}. {result['title']}\n")
            context_parts.append(f"   {result['snippet']}\n")
            context_parts.append(f"   Source: {result['url']}\n")
        
        return "".join(context_parts)
    
    async def _query_google(
        self,
        model_name: str,
        prompt: str,
        api_key: str
    ) -> Dict[str, Any]:
        """Helper to query Google models"""
        try:
            from google import genai
            client = genai.Client(api_key=api_key)

            # New SDK doesn't accept config dict directly
            response = client.models.generate_content(
                model=model_name,
                contents=[{"role": "user", "parts": [{"text": prompt}]}]
            )
            return {
                "provider": "google",
                "model": model_name,
                "response": response.text,
                "success": True
            }
        except Exception as e:
            logger.error(f"Google query failed: {e}")
            return {
                "provider": "google",
                "model": model_name,
                "response": f"Error: {str(e)}",
                "success": False
            }

    async def _query_openai_compatible(
        self,
        provider: str,
        model_name: str,
        prompt: str,
        api_key: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Helper to query OpenAI-compatible models"""
        try:
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
        except Exception as e:
            logger.error(f"{provider} query failed: {e}")
            return {
                "provider": provider,
                "model": model_name,
                "response": f"Error: {str(e)}",
                "success": False
            }

    async def _query_anthropic(
        self,
        model_name: str,
        prompt: str,
        api_key: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Helper to query Anthropic models"""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)

            response = client.messages.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get("max_output_tokens", 1024),
                temperature=config.get("temperature", 0.7)
            )

            return {
                "provider": "anthropic",
                "model": model_name,
                "response": response.content[0].text,
                "success": True
            }
        except Exception as e:
            logger.error(f"Anthropic query failed: {e}")
            return {
                "provider": "anthropic",
                "model": model_name,
                "response": f"Error: {str(e)}",
                "success": False
            }
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949

    async def query_model(
        self,
        provider: str,
        model_name: str,
        prompt: str,
        api_key: str,
        config: Dict[str, Any],
    ) -> Dict[str, str]:
        """Query a single AI model"""
<<<<<<< HEAD
<<<<<<< HEAD

        # Ethics Check on Prompt
        guardian = EthicsGuardian()
        is_safe_prompt, prompt_issue = guardian.check_safety(prompt)
        if not is_safe_prompt:
             # Append neutrality instruction to prompt since we don't have separate system msg here easily
             prompt = f"{prompt}\n\n[System Note: {guardian.augment_system_instruction('', prompt_issue)}]"

=======
        monitor = get_monitor()
        start_time = time.time()
>>>>>>> origin/monitoring-setup-15681340840960488850
        try:
            # Validate prompt is not empty
            if not prompt or not prompt.strip():
                monitor.log_request(provider, model_name, 0, False, "Empty prompt")
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": "Error: Prompt cannot be empty",
                    "success": False,
                }
            if provider == "google":
                from google import genai

                client = genai.Client(api_key=api_key)

                # New SDK doesn't accept config dict directly
                response = client.models.generate_content(
                    model=model_name,
                    contents=[{"role": "user", "parts": [{"text": prompt}]}],
                )
                monitor.log_request(provider, model_name, time.time() - start_time, True)
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.text,
                    "success": True,
                }
<<<<<<< HEAD

            elif provider in ["openai", "together", "xai", "deepseek"]:
=======
            
            elif provider in ["openai", "together", "xai", "deepseek", "groq"]:
>>>>>>> api-integrations-groq-3434217061461873316
                from openai import OpenAI

                base_urls = {
                    "together": "https://api.together.xyz/v1",
                    "xai": "https://api.x.ai/v1",
                    "deepseek": "https://api.deepseek.com",
<<<<<<< HEAD
=======
                    "groq": "https://api.groq.com/openai/v1"
>>>>>>> api-integrations-groq-3434217061461873316
                }

                client = OpenAI(api_key=api_key, base_url=base_urls.get(provider))

                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.get("temperature", 0.7),
                    max_tokens=config.get("max_output_tokens", 1024),
                )
<<<<<<< HEAD

=======
                
                monitor.log_request(provider, model_name, time.time() - start_time, True)
>>>>>>> origin/monitoring-setup-15681340840960488850
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.choices[0].message.content,
                    "success": True,
                }

            elif provider == "anthropic":
                from anthropic import Anthropic

                client = Anthropic(api_key=api_key)

                response = client.messages.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=config.get("max_output_tokens", 1024),
                    temperature=config.get("temperature", 0.7),
                )
<<<<<<< HEAD

=======
                
                monitor.log_request(provider, model_name, time.time() - start_time, True)
>>>>>>> origin/monitoring-setup-15681340840960488850
                return {
                    "provider": provider,
                    "model": model_name,
                    "response": response.content[0].text,
                    "success": True,
                }

        except Exception as e:
            monitor.log_request(provider, model_name, time.time() - start_time, False, str(e))
            return {
                "provider": provider,
                "model": model_name,
                "response": f"Error: {str(e)}",
                "success": False,
=======
        # Validate prompt is not empty
        if not prompt or not prompt.strip():
            return {
                "provider": provider,
                "model": model_name,
                "response": "Error: Prompt cannot be empty",
                "success": False
            }

        if provider == "google":
            return await self._query_google(model_name, prompt, api_key)

        elif provider in ["openai", "together", "xai", "deepseek"]:
            return await self._query_openai_compatible(
                provider, model_name, prompt, api_key, config
            )

        elif provider == "anthropic":
            return await self._query_anthropic(model_name, prompt, api_key, config)

        else:
            return {
                "provider": provider,
                "model": model_name,
                "response": f"Error: Unsupported provider {provider}",
                "success": False
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
            }

    async def query_multiple_models(
        self, query: str, models: List[Dict[str, Any]], config: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Query multiple AI models in parallel"""
        tasks = []
        for model_info in models:
            task = self.query_model(
                provider=model_info["provider"],
                model_name=model_info["model"],
                prompt=query,
                api_key=model_info["api_key"],
                config=config,
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results

    def synthesize_responses(
        self, query: str, model_responses: List[Dict[str, str]], internet_context: str
    ) -> str:
<<<<<<< HEAD
        """Synthesize multiple AI responses and internet knowledge into a unified answer"""
<<<<<<< HEAD
=======
        
        guardian = EthicsGuardian()
>>>>>>> 9a44f3f (Ethics: [bias fixes])

        synthesis = f"# AI Brain Synthesis\n\n"
        synthesis += f"**Your Question:** {query}\n\n"

        # Add internet context if available
        if internet_context and internet_context.strip():
            synthesis += f"## Internet Knowledge\n{internet_context}\n\n"

        # Add model responses
        synthesis += "## AI Model Responses\n\n"

=======
        """Synthesize multiple AI responses and internet knowledge"""
        
        parts = [f"# AI Brain Synthesis\n\n**Your Question:** {query}\n\n"]
        
        # Add internet context if available
        if internet_context and internet_context.strip():
            parts.append(f"## Internet Knowledge\n{internet_context}\n\n")
        
        # Add model responses
        parts.append("## AI Model Responses\n\n")
        
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
        successful_responses = [r for r in model_responses if r.get("success")]

        for i, response in enumerate(successful_responses, 1):
<<<<<<< HEAD
            synthesis += (
                f"### {i}. {response['provider'].upper()} - {response['model']}\n"
            )
            synthesis += f"{response['response']}\n\n"

=======
            parts.append(
                f"### {i}. {response['provider'].upper()} - {response['model']}\n"
            )
            parts.append(f"{response['response']}\n\n")
        
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
        # Add failed models if any
        failed_responses = [r for r in model_responses if not r.get("success")]
        if failed_responses:
            parts.append("\n## Failed Queries\n")
            for response in failed_responses:
<<<<<<< HEAD
                synthesis += f"- {response['provider']}/{response['model']}: {response['response']}\n"

        # Add summary
        synthesis += "\n---\n\n"
        synthesis += f"**Total models consulted:** {len(model_responses)}\n"
        synthesis += f"**Successful responses:** {len(successful_responses)}\n"
        synthesis += f"**Internet search:** {'✓ Enabled' if internet_context else '✗ Disabled'}\n"
<<<<<<< HEAD
=======
        
        # Ethics check on synthesis
        is_safe, issue = guardian.check_safety(synthesis)
        if not is_safe:
            synthesis += guardian.get_disclaimer(issue)
>>>>>>> 9a44f3f (Ethics: [bias fixes])

        return synthesis

=======
                parts.append(
                    f"- {response['provider']}/{response['model']}: "
                    f"{response['response']}\n"
                )
        
        # Add summary
        parts.append("\n---\n\n")
        parts.append(f"**Total models consulted:** {len(model_responses)}\n")
        parts.append(f"**Successful responses:** {len(successful_responses)}\n")
        parts.append(
            f"**Internet search:** {'✓ Enabled' if internet_context else '✗ Disabled'}\n"
        )
        
        return "".join(parts)
    
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
    def add_to_memory(self, query: str, response: str):
        """Store conversation in memory"""
        self.conversation_memory.append(
            {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response,
            }
        )

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
