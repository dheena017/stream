"""
Advanced Brain Integration Module
Provides utilities to integrate brain_advanced.py with the main app.py
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from brain_advanced import (
    AdvancedAIBrain,
    QueryComplexity,
    ModelResponse,
    SynthesisResult,
    create_advanced_brain,
    get_complexity_emoji
)


class BrainIntegrator:
    """Bridge between app.py and advanced brain"""
    
    def __init__(self):
        self.advanced_brain = create_advanced_brain()
        self.session_analysis_cache: Dict[str, Dict] = {}
    
    async def process_query_with_advanced_brain(
        self,
        query: str,
        model_responses_raw: List[Dict],
        available_models: List[Dict],
        internet_context: Optional[str] = None,
        enable_detailed_analysis: bool = True
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Process query using advanced brain capabilities
        Returns: (formatted_response, analysis_metadata)
        """
        
        # Phase 1: Analyze query and route
        complexity, recommended_models, complexity_score = self.advanced_brain.analyze_and_route(
            query,
            available_models
        )
        
        # Phase 2: Process raw responses into enhanced ModelResponse objects
        enhanced_responses: List[ModelResponse] = []
        for raw_response in model_responses_raw:
            # Find matching model info
            model_info = next(
                (m for m in available_models if m.get("provider") == raw_response.get("provider")),
                {"model": "unknown"}
            )
            
            enhanced_response = self.advanced_brain.process_response(raw_response, model_info)
            enhanced_responses.append(enhanced_response)
        
        # Phase 3: Synthesize with advanced knowledge synthesis
        synthesis_result = self.advanced_brain.knowledge_synthesis.synthesize_with_weighting(
            query,
            enhanced_responses,
            internet_context
        )
        
        # Phase 4: Format output
        if enable_detailed_analysis:
            formatted_output = self._format_advanced_response(
                synthesis_result,
                complexity,
                enhanced_responses
            )
        else:
            formatted_output = synthesis_result.primary_response
        
        # Create metadata
        metadata = {
            "complexity": complexity.value,
            "complexity_score": complexity_score,
            "confidence_score": synthesis_result.confidence_score,
            "consensus_level": synthesis_result.consensus_level,
            "model_votes": synthesis_result.model_votes,
            "reasoning_chain_length": len(synthesis_result.reasoning_chain),
            "sources": synthesis_result.sources,
            "analysis_quality": self._calculate_analysis_quality(enhanced_responses, synthesis_result)
        }
        
        return formatted_output, metadata
    
    def _format_advanced_response(
        self,
        synthesis_result: SynthesisResult,
        complexity: QueryComplexity,
        enhanced_responses: List[ModelResponse]
    ) -> str:
        """Format response with advanced insights"""
        
        output = ""
        
        # Header with complexity indicator
        output += f"## {get_complexity_emoji(complexity)} Query Analysis ({complexity.value.title()})\n\n"
        
        # Confidence badges
        confidence_pct = synthesis_result.confidence_score * 100
        consensus_pct = synthesis_result.consensus_level * 100
        
        confidence_badge = self._get_confidence_badge(confidence_pct)
        consensus_badge = self._get_consensus_badge(consensus_pct)
        
        output += f"**Confidence:** {confidence_badge} {confidence_pct:.0f}% | "
        output += f"**Consensus:** {consensus_badge} {consensus_pct:.0f}%\n\n"
        
        # Primary response
        output += "### 💬 Answer\n\n"
        output += synthesis_result.primary_response + "\n\n"
        
        # Supporting perspectives
        if synthesis_result.supporting_evidence:
            output += "### 📚 Supporting Perspectives\n\n"
            for evidence in synthesis_result.supporting_evidence:
                output += f"{evidence}\n\n"
        
        # Quality indicators
        output += "### 📊 Analysis Quality\n\n"
        for response in enhanced_responses[:3]:
            if response.success:
                quality_msg = self._format_quality_metrics(response)
                output += f"- **{response.provider.upper()}**: {quality_msg}\n"
        
        # Reasoning transparency
        if synthesis_result.reasoning_chain:
            output += "\n### 🔗 Key Reasoning Steps\n\n"
            for i, step in enumerate(synthesis_result.reasoning_chain[:3], 1):
                output += f"{i}. _{step.model}_: {step.reasoning[:100]}...\n"
        
        # Data sources
        output += f"\n### 🔍 Sources ({len(synthesis_result.sources)})\n\n"
        for source in synthesis_result.sources:
            output += f"- {source}\n"
        
        return output
    
    def _get_confidence_badge(self, confidence_pct: float) -> str:
        """Get badge emoji based on confidence"""
        if confidence_pct >= 85:
            return "🟢"  # Very high
        elif confidence_pct >= 70:
            return "🟡"  # High
        elif confidence_pct >= 50:
            return "🟠"  # Moderate
        else:
            return "🔴"  # Low
    
    def _get_consensus_badge(self, consensus_pct: float) -> str:
        """Get badge emoji based on consensus"""
        if consensus_pct >= 80:
            return "🔄"  # Strong
        elif consensus_pct >= 60:
            return "🔄"  # Moderate
        else:
            return "⚠️"   # Weak
    
    def _format_quality_metrics(self, response: ModelResponse) -> str:
        """Format quality metrics for a response"""
        metrics = response.response_quality_metrics
        
        scores = []
        if metrics.get("length_score", 0) > 0.7:
            scores.append("✓ Detailed")
        if metrics.get("coherence_score", 0) > 0.6:
            scores.append("✓ Coherent")
        if metrics.get("specificity_score", 0) > 0.6:
            scores.append("✓ Specific")
        
        quality_str = ", ".join(scores) if scores else "Basic"
        return f"{quality_str} (Confidence: {response.confidence_score * 100:.0f}%)"
    
    def _calculate_analysis_quality(
        self,
        enhanced_responses: List[ModelResponse],
        synthesis_result: SynthesisResult
    ) -> str:
        """Calculate overall analysis quality"""
        if not enhanced_responses:
            return "insufficient_data"
        
        success_rate = sum(1 for r in enhanced_responses if r.success) / len(enhanced_responses)
        
        if success_rate < 0.5:
            quality = "low"
        elif synthesis_result.consensus_level < 0.4:
            quality = "conflicting"
        elif synthesis_result.confidence_score < 0.6:
            quality = "moderate"
        elif synthesis_result.confidence_score < 0.8:
            quality = "good"
        else:
            quality = "excellent"
        
        return quality
    
    def get_model_recommendations(
        self,
        query: str,
        available_models: List[Dict]
    ) -> Dict[str, Any]:
        """Get model recommendations without executing queries"""
        complexity, recommended_models, complexity_score = self.advanced_brain.analyze_and_route(
            query,
            available_models
        )
        
        return {
            "query_complexity": complexity.value,
            "complexity_score": complexity_score,
            "recommended_models": [
                {
                    "provider": m.get("provider"),
                    "model": m.get("model"),
                    "recommendation_score": m.get("recommendation_score", 0),
                    "rationale": self._get_recommendation_rationale(m, complexity)
                }
                for m in recommended_models[:5]
            ]
        }
    
    def _get_recommendation_rationale(self, model_info: Dict, complexity: QueryComplexity) -> str:
        """Explain why a model is recommended"""
        provider = model_info.get("provider", "unknown")
        score = model_info.get("recommendation_score", 0)
        
        if complexity == QueryComplexity.SIMPLE:
            reasons = ["Fast", "Accurate for simple queries"]
        elif complexity == QueryComplexity.MODERATE:
            reasons = ["Good reasoning", "Balanced performance"]
        elif complexity == QueryComplexity.COMPLEX:
            reasons = ["Strong reasoning", "Handles complexity well"]
        else:  # EXPERT
            reasons = ["Advanced reasoning", "Specialized knowledge"]
        
        if provider == "openai" or provider == "anthropic":
            reasons.append("Strong reasoning")
        if provider == "google":
            reasons.append("Fast responses")
        
        return f"{score:.0%} - " + " + ".join(reasons)


class AdvancedBrainUI:
    """UI utilities for displaying advanced brain analysis"""
    
    @staticmethod
    def create_complexity_indicator(complexity: QueryComplexity, score: float) -> str:
        """Create visual indicator for query complexity"""
        emoji = get_complexity_emoji(complexity)
        bar_length = int(score * 10)
        bar = "█" * bar_length + "░" * (10 - bar_length)
        
        return f"{emoji} {complexity.value.title()} [{bar}] {score * 100:.0f}%"
    
    @staticmethod
    def create_consensus_indicator(consensus: float, model_count: int) -> str:
        """Create visual indicator for consensus level"""
        if consensus >= 0.8:
            badge = "🔄 Strong"
        elif consensus >= 0.6:
            badge = "🔄 Moderate"
        elif consensus >= 0.4:
            badge = "⚠️ Weak"
        else:
            badge = "❌ Conflicting"
        
        return f"{badge} consensus from {model_count} model(s)"
    
    @staticmethod
    def create_confidence_indicator(confidence: float) -> str:
        """Create visual indicator for confidence"""
        pct = confidence * 100
        
        if pct >= 85:
            badge = "🟢 Very High"
        elif pct >= 70:
            badge = "🟡 High"
        elif pct >= 50:
            badge = "🟠 Moderate"
        else:
            badge = "🔴 Low"
        
        return f"{badge} confidence ({pct:.0f}%)"
    
    @staticmethod
    def create_quality_summary(metadata: Dict[str, Any]) -> str:
        """Create quality summary for display"""
        quality = metadata.get("analysis_quality", "unknown")
        
        quality_emojis = {
            "excellent": "⭐⭐⭐",
            "good": "⭐⭐",
            "moderate": "⭐",
            "conflicting": "⚠️",
            "low": "❌",
            "insufficient_data": "❓"
        }
        
        emoji = quality_emojis.get(quality, "❓")
        return f"{emoji} Analysis Quality: {quality.replace('_', ' ').title()}"


# Export main integrator
integrator = BrainIntegrator()
ui_helper = AdvancedBrainUI()


def setup_advanced_brain() -> BrainIntegrator:
    """Setup function to initialize advanced brain"""
    return BrainIntegrator()
