"""
Advanced Brain Configuration & Utilities
Helper functions and configuration for easy integration
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from brain_advanced import QueryComplexity


class AnalysisLevel(Enum):
    """Supported analysis detail levels"""
    BASIC = "basic"              # Primary response only
    DETAILED = "detailed"        # Full analysis with reasoning
    VERBOSE = "verbose"          # Maximum detail including debugging


class ResponseFormat(Enum):
    """Output format options"""
    MARKDOWN = "markdown"        # Markdown formatted
    PLAIN = "plain"             # Plain text
    JSON = "json"               # JSON structure
    HTML = "html"               # HTML formatted


@dataclass
class AdvancedBrainConfig:
    """Configuration for advanced brain"""
    
    # Enable features
    enable_complexity_analysis: bool = True
    enable_model_routing: bool = True
    enable_reasoning_extraction: bool = True
    enable_consensus_analysis: bool = True
    enable_internet_search: bool = False
    
    # Model selection
    max_models_to_consult: int = 4
    min_models_required: int = 1
    
    # Thresholds
    min_confidence_threshold: float = 0.4
    min_consensus_threshold: float = 0.3
    high_confidence_threshold: float = 0.8
    
    # Analysis settings
    analysis_level: AnalysisLevel = AnalysisLevel.DETAILED
    response_format: ResponseFormat = ResponseFormat.MARKDOWN
    
    # Optimization
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    enable_performance_tracking: bool = True
    
    # Display
    show_reasoning_chain: bool = True
    show_source_attribution: bool = True
    show_confidence_badges: bool = True
    show_consensus_indicators: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> "AdvancedBrainConfig":
        """Create config from dictionary"""
        # Filter to only known fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in config_dict.items() if k in valid_fields}
        return cls(**filtered)
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary"""
        return {
            "enable_complexity_analysis": self.enable_complexity_analysis,
            "enable_model_routing": self.enable_model_routing,
            "enable_reasoning_extraction": self.enable_reasoning_extraction,
            "enable_consensus_analysis": self.enable_consensus_analysis,
            "enable_internet_search": self.enable_internet_search,
            "max_models_to_consult": self.max_models_to_consult,
            "min_models_required": self.min_models_required,
            "min_confidence_threshold": self.min_confidence_threshold,
            "min_consensus_threshold": self.min_consensus_threshold,
            "high_confidence_threshold": self.high_confidence_threshold,
            "analysis_level": self.analysis_level.value,
            "response_format": self.response_format.value,
            "enable_caching": self.enable_caching,
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "enable_performance_tracking": self.enable_performance_tracking,
            "show_reasoning_chain": self.show_reasoning_chain,
            "show_source_attribution": self.show_source_attribution,
            "show_confidence_badges": self.show_confidence_badges,
            "show_consensus_indicators": self.show_consensus_indicators,
        }


# Default configurations for different use cases
CONFIGS = {
    "fast": AdvancedBrainConfig(
        max_models_to_consult=1,
        enable_internet_search=False,
        analysis_level=AnalysisLevel.BASIC,
        enable_reasoning_extraction=False,
    ),
    
    "balanced": AdvancedBrainConfig(
        max_models_to_consult=2,
        enable_internet_search=False,
        analysis_level=AnalysisLevel.DETAILED,
    ),
    
    "thorough": AdvancedBrainConfig(
        max_models_to_consult=4,
        enable_internet_search=True,
        analysis_level=AnalysisLevel.VERBOSE,
        enable_reasoning_extraction=True,
    ),
    
    "research": AdvancedBrainConfig(
        max_models_to_consult=4,
        enable_internet_search=True,
        min_confidence_threshold=0.7,
        analysis_level=AnalysisLevel.VERBOSE,
        enable_performance_tracking=True,
    ),
}


class PromptTemplates:
    """Templates for system prompts and instructions"""
    
    REASONING_PROMPT = """Provide a step-by-step reasoning for your answer. Break down your thinking into clear logical steps."""
    
    EXPERT_PROMPT = """You are an expert on this topic. Provide authoritative, well-reasoned insights with specific examples where applicable."""
    
    CONCISE_PROMPT = """Provide a concise, direct answer. Be specific and avoid unnecessary elaboration."""
    
    DETAILED_PROMPT = """Provide a comprehensive, well-structured answer. Include relevant context, examples, and supporting details."""
    
    COMPARATIVE_PROMPT = """Compare and contrast the key aspects. Highlight similarities, differences, and trade-offs."""
    
    EDUCATIONAL_PROMPT = """Explain this as if teaching someone new to the topic. Use clear language and helpful examples."""
    
    @staticmethod
    def get_prompt_for_complexity(complexity: QueryComplexity) -> str:
        """Get recommended prompt based on complexity"""
        prompts = {
            QueryComplexity.SIMPLE: PromptTemplates.CONCISE_PROMPT,
            QueryComplexity.MODERATE: PromptTemplates.DETAILED_PROMPT,
            QueryComplexity.COMPLEX: PromptTemplates.REASONING_PROMPT,
            QueryComplexity.EXPERT: PromptTemplates.EXPERT_PROMPT,
        }
        return prompts.get(complexity, PromptTemplates.DETAILED_PROMPT)


class ModelProfile:
    """Profiles for different AI models"""
    
    PROFILES = {
        "google/gemini": {
            "name": "Google Gemini",
            "strength": "Fast, general-purpose, good for simple to moderate queries",
            "best_for": ["simple", "moderate", "factual", "fast_response"],
            "weak_in": ["cutting_edge", "deep_reasoning"],
            "latency_ms": 1500,
            "cost_tier": "low",
        },
        
        "openai/gpt4": {
            "name": "OpenAI GPT-4",
            "strength": "Excellent reasoning, handles complex queries well",
            "best_for": ["complex", "reasoning", "code", "analysis"],
            "weak_in": ["speed", "cost"],
            "latency_ms": 3000,
            "cost_tier": "high",
        },
        
        "openai/gpt4o": {
            "name": "OpenAI GPT-4o",
            "strength": "Strong reasoning, multimodal, good balance",
            "best_for": ["complex", "reasoning", "expert", "balanced"],
            "weak_in": ["speed"],
            "latency_ms": 2500,
            "cost_tier": "medium-high",
        },
        
        "anthropic/claude": {
            "name": "Anthropic Claude",
            "strength": "Careful analysis, strong reasoning, safety-focused",
            "best_for": ["complex", "reasoning", "analysis", "safety"],
            "weak_in": ["speed"],
            "latency_ms": 2800,
            "cost_tier": "medium-high",
        },
        
        "together/llama": {
            "name": "Meta Llama",
            "strength": "Good general performance, code understanding",
            "best_for": ["moderate", "code", "balanced", "cost"],
            "weak_in": ["complex_reasoning"],
            "latency_ms": 2000,
            "cost_tier": "low",
        },
    }
    
    @staticmethod
    def get_profile(provider: str, model: str) -> Optional[Dict]:
        """Get model profile"""
        key = f"{provider}/{model.split('/')[-1].lower()}"
        return ModelProfile.PROFILES.get(key)


class PerformanceMetrics:
    """Track performance metrics"""
    
    def __init__(self):
        self.total_queries = 0
        self.total_response_time_ms = 0
        self.avg_confidence = 0
        self.avg_consensus = 0
        self.model_performance: Dict[str, Dict] = {}
    
    def record_query(
        self,
        query: str,
        response_time_ms: float,
        confidence: float,
        consensus: float,
        models_used: List[str]
    ):
        """Record a query execution"""
        self.total_queries += 1
        self.total_response_time_ms += response_time_ms
        
        # Update averages
        self.avg_confidence = (
            (self.avg_confidence * (self.total_queries - 1) + confidence) / self.total_queries
        )
        self.avg_consensus = (
            (self.avg_consensus * (self.total_queries - 1) + consensus) / self.total_queries
        )
        
        # Track model performance
        for model in models_used:
            if model not in self.model_performance:
                self.model_performance[model] = {
                    "count": 0,
                    "avg_response_time": 0,
                    "avg_confidence": 0,
                }
            
            perf = self.model_performance[model]
            perf["count"] += 1
            perf["avg_response_time"] = (
                (perf["avg_response_time"] * (perf["count"] - 1) + response_time_ms) / perf["count"]
            )
            perf["avg_confidence"] = (
                (perf["avg_confidence"] * (perf["count"] - 1) + confidence) / perf["count"]
            )
    
    def get_summary(self) -> Dict:
        """Get performance summary"""
        avg_response_time = (
            self.total_response_time_ms / max(self.total_queries, 1)
        )
        
        return {
            "total_queries": self.total_queries,
            "avg_response_time_ms": avg_response_time,
            "avg_confidence": self.avg_confidence,
            "avg_consensus": self.avg_consensus,
            "model_performance": self.model_performance,
        }
    
    def get_best_model(self) -> Optional[str]:
        """Get best performing model"""
        if not self.model_performance:
            return None
        
        return max(
            self.model_performance.keys(),
            key=lambda m: self.model_performance[m]["avg_confidence"]
        )


class CacheManager:
    """Simple cache for responses"""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, tuple] = {}  # (response, timestamp)
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str):
        """Get cached response"""
        if key not in self.cache:
            return None
        
        import time
        response, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl_seconds:
            del self.cache[key]
            return None
        
        return response
    
    def set(self, key: str, value):
        """Cache response"""
        import time
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
    
    def get_cache_key(self, query: str, models: List[str]) -> str:
        """Generate cache key"""
        import hashlib
        combined = f"{query}{''.join(sorted(models))}"
        return hashlib.md5(combined.encode()).hexdigest()


# Export utilities
__all__ = [
    "AdvancedBrainConfig",
    "AnalysisLevel",
    "ResponseFormat",
    "CONFIGS",
    "PromptTemplates",
    "ModelProfile",
    "PerformanceMetrics",
    "CacheManager",
]
