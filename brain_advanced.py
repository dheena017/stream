"""
Enhanced Advanced AI Brain Mode (v2.0)
Advanced reasoning, model orchestration, and knowledge synthesis
Features: Chain-of-thought, multi-level learning, confidence scoring, consensus analysis
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import json
import re
from collections import Counter, defaultdict


class QueryComplexity(Enum):
    """Query complexity levels"""
    SIMPLE = "simple"           # Factual, single-topic queries
    MODERATE = "moderate"       # Multi-part, requires reasoning
    COMPLEX = "complex"         # Requires deep reasoning, synthesis
    EXPERT = "expert"           # Highly specialized, cutting-edge


class ConfidenceLevel(Enum):
    """Response confidence levels"""
    LOW = "low"              # 0-40%
    MEDIUM = "medium"        # 40-70%
    HIGH = "high"            # 70-90%
    VERY_HIGH = "very_high"  # 90%+


@dataclass
class ReasoningStep:
    """A single step in chain-of-thought reasoning"""
    step_number: int
    description: str
    model: str
    reasoning: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ModelResponse:
    """Enhanced model response with metadata"""
    provider: str
    model: str
    response_text: str
    confidence_score: float
    reasoning_steps: List[ReasoningStep]
    keywords_extracted: List[str]
    response_quality_metrics: Dict[str, float]
    success: bool
    error: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class SynthesisResult:
    """Final synthesized response with all metadata"""
    query: str
    primary_response: str
    supporting_evidence: List[str]
    confidence_score: float
    consensus_level: float
    model_votes: Dict[str, int]
    reasoning_chain: List[ReasoningStep]
    sources: List[str]
    internet_context: Optional[str] = None
    synthesized_at: str = field(default_factory=lambda: datetime.now().isoformat())


class AdvancedReasoningEngine:
    """Implements chain-of-thought and multi-step reasoning"""
    
    def __init__(self):
        self.reasoning_cache: Dict[str, List[ReasoningStep]] = {}
        self.inference_history: List[Dict] = []
    
    def analyze_query_complexity(self, query: str) -> Tuple[QueryComplexity, float]:
        """
        Analyze query complexity level
        Returns: (complexity_level, complexity_score 0-1)
        """
        words = query.lower().split()
        char_count = len(query)
        question_count = query.count('?')
        
        # Feature extraction
        has_multiple_entities = len(set(words)) > 20
        has_conditional = any(kw in query.lower() for kw in ['if', 'when', 'given', 'suppose'])
        has_comparison = any(kw in query.lower() for kw in ['compare', 'difference', 'vs', 'versus', 'better', 'worse'])
        has_chain = any(kw in query.lower() for kw in ['chain', 'sequence', 'step', 'process', 'how does'])
        has_speculation = any(kw in query.lower() for kw in ['why', 'how', 'what if', 'could', 'might', 'predict'])
        
        complexity_score = 0.0
        
        # Base score on length
        if char_count < 50:
            complexity_score += 0.1
        elif char_count < 150:
            complexity_score += 0.25
        elif char_count < 300:
            complexity_score += 0.4
        else:
            complexity_score += 0.55
        
        # Feature contributions
        if has_multiple_entities:
            complexity_score += 0.15
        if has_conditional:
            complexity_score += 0.15
        if has_comparison:
            complexity_score += 0.1
        if has_chain:
            complexity_score += 0.15
        if has_speculation:
            complexity_score += 0.1
        if question_count > 1:
            complexity_score += 0.1
        
        complexity_score = min(complexity_score, 1.0)  # Cap at 1.0
        
        # Classify
        if complexity_score < 0.25:
            return QueryComplexity.SIMPLE, complexity_score
        elif complexity_score < 0.50:
            return QueryComplexity.MODERATE, complexity_score
        elif complexity_score < 0.75:
            return QueryComplexity.COMPLEX, complexity_score
        else:
            return QueryComplexity.EXPERT, complexity_score
    
    def extract_reasoning_chain(self, response_text: str, model: str) -> List[ReasoningStep]:
        """Extract reasoning steps from model response"""
        steps = []
        
        # Look for numbered steps, bullets, or explicit reasoning markers
        patterns = [
            r'(?:Step|step)\s+(\d+)[:\s]+(.+?)(?=(?:Step|step)\s+\d+|$)',
            r'(?:Therefore|Thus|Hence|So|Because)[:\s]+(.+?)(?=(?:Therefore|Thus|Hence|So|Because)[:\s]|$)',
            r'(?:First|Second|Third|Finally)[:\s]+(.+?)(?=(?:First|Second|Third|Finally)[:\s]|$)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, response_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                reasoning_text = match.group(1) if len(match.groups()) > 0 else match.group(0)
                confidence = self._score_confidence(reasoning_text)
                
                step = ReasoningStep(
                    step_number=len(steps) + 1,
                    description=f"Step {len(steps) + 1}",
                    model=model,
                    reasoning=reasoning_text.strip()[:500],
                    confidence=confidence
                )
                steps.append(step)
        
        return steps
    
    def _score_confidence(self, text: str) -> float:
        """Score confidence of a statement based on keywords"""
        high_confidence_words = ['definitely', 'certainly', 'proven', 'verified', 'always', 'never']
        medium_confidence_words = ['likely', 'probably', 'usually', 'generally', 'typically']
        low_confidence_words = ['might', 'could', 'perhaps', 'possibly', 'maybe', 'uncertain']
        
        text_lower = text.lower()
        
        high_count = sum(1 for w in high_confidence_words if w in text_lower)
        medium_count = sum(1 for w in medium_confidence_words if w in text_lower)
        low_count = sum(1 for w in low_confidence_words if w in text_lower)
        
        if high_count > 0:
            return 0.85
        elif medium_count > 0:
            return 0.65
        elif low_count > 0:
            return 0.40
        else:
            return 0.60


class AdaptiveModelRouter:
    """Intelligently route queries to best models based on history and complexity"""
    
    def __init__(self):
        self.model_specialties: Dict[str, List[str]] = defaultdict(list)
        self.model_performance_by_complexity: Dict[str, Dict[QueryComplexity, float]] = defaultdict(lambda: defaultdict(float))
        self.response_latencies: Dict[str, List[float]] = defaultdict(list)
    
    def recommend_models(
        self,
        query: str,
        available_models: List[Dict],
        query_complexity: QueryComplexity,
        performance_history: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Recommend best models for the query
        Returns: Sorted list of models ranked by recommendation score
        """
        recommendations = []
        
        for model in available_models:
            provider = model.get("provider", "unknown")
            model_name = model.get("model", "unknown")
            
            score = 0.0
            
            # 1. Performance history (40% weight)
            if performance_history and provider in performance_history:
                perf = performance_history[provider]
                success_rate = perf.get('success', 0) / max(perf.get('total', 1), 1)
                score += success_rate * 0.40
            
            # 2. Complexity alignment (30% weight)
            base_complexity_scores = {
                QueryComplexity.SIMPLE: {
                    'google': 0.85, 'openai': 0.80, 'anthropic': 0.85,
                    'together': 0.75, 'xai': 0.70, 'deepseek': 0.75
                },
                QueryComplexity.MODERATE: {
                    'google': 0.80, 'openai': 0.85, 'anthropic': 0.85,
                    'together': 0.80, 'xai': 0.75, 'deepseek': 0.80
                },
                QueryComplexity.COMPLEX: {
                    'google': 0.80, 'openai': 0.90, 'anthropic': 0.90,
                    'together': 0.80, 'xai': 0.75, 'deepseek': 0.85
                },
                QueryComplexity.EXPERT: {
                    'google': 0.75, 'openai': 0.90, 'anthropic': 0.90,
                    'together': 0.75, 'xai': 0.70, 'deepseek': 0.85
                }
            }
            
            complexity_score = base_complexity_scores.get(query_complexity, {}).get(provider, 0.7)
            score += complexity_score * 0.30
            
            # 3. Model variety (15% weight) - penalize if same provider already selected
            selected_providers = [r["provider"] for r in recommendations[:2]]
            if provider not in selected_providers:
                score += 0.15
            
            # 4. Base model quality (15% weight)
            model_quality = {
                'google': 0.82, 'openai': 0.88, 'anthropic': 0.87,
                'together': 0.75, 'xai': 0.72, 'deepseek': 0.80
            }
            score += model_quality.get(provider, 0.70) * 0.15
            
            recommendations.append({
                **model,
                "recommendation_score": score
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations


class AdvancedKnowledgeSynthesis:
    """Advanced synthesis of multiple model responses with consensus analysis"""
    
    def __init__(self):
        self.source_credibility: Dict[str, float] = defaultdict(lambda: 0.7)
        self.conflict_history: List[Dict] = []
    
    def analyze_consensus(self, model_responses: List[ModelResponse]) -> Dict[str, Any]:
        """
        Analyze agreement between models
        Returns: Consensus score (0-1), conflict points, common themes
        """
        if not model_responses or not any(r.success for r in model_responses):
            return {"consensus_score": 0, "agreement_level": "no_consensus"}
        
        successful_responses = [r for r in model_responses if r.success]
        
        # Extract key phrases/entities
        key_phrases = []
        for response in successful_responses:
            phrases = self._extract_key_phrases(response.response_text)
            key_phrases.extend(phrases)
        
        # Count phrase frequency
        phrase_counts = Counter(key_phrases)
        most_common = phrase_counts.most_common(10)
        
        # Calculate consensus
        if len(successful_responses) < 2:
            consensus_score = 1.0 if successful_responses else 0
        else:
            # Count agreements on main themes
            agreements = sum(count for _, count in most_common) / (len(successful_responses) * len(most_common) + 1)
            consensus_score = min(agreements, 1.0)
        
        # Determine agreement level
        if consensus_score > 0.75:
            agreement_level = "strong_consensus"
        elif consensus_score > 0.50:
            agreement_level = "moderate_consensus"
        elif consensus_score > 0.25:
            agreement_level = "weak_consensus"
        else:
            agreement_level = "conflicting"
        
        return {
            "consensus_score": consensus_score,
            "agreement_level": agreement_level,
            "common_themes": [phrase for phrase, _ in most_common[:5]],
            "conflicting_points": self._identify_conflicts(successful_responses)
        }
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract important phrases from text"""
        # Simple noun phrase extraction
        sentences = text.split('.')
        phrases = []
        
        for sentence in sentences[:5]:  # First 5 sentences
            words = sentence.strip().split()
            if len(words) > 3:
                # Take 2-4 word chunks
                for i in range(len(words) - 1):
                    chunk = ' '.join(words[i:min(i+3, len(words))])
                    if len(chunk) > 5:
                        phrases.append(chunk.lower())
        
        return phrases[:10]
    
    def _identify_conflicts(self, responses: List[ModelResponse]) -> List[str]:
        """Identify conflicting points between responses"""
        conflicts = []
        
        if len(responses) < 2:
            return conflicts
        
        # Simple conflict detection: different conclusions
        conclusions = []
        for resp in responses:
            # Look for definitive statements
            if 'is' in resp.response_text or 'are' in resp.response_text:
                sentences = resp.response_text.split('.')
                if sentences:
                    conclusions.append(sentences[0].lower()[:100])
        
        # Check for contradictions
        for i, conc1 in enumerate(conclusions):
            for conc2 in conclusions[i+1:]:
                if 'not' in conc1 and 'not' not in conc2:
                    conflicts.append(f"Potential contradiction: {conc1[:50]}...")
        
        return conflicts[:3]
    
    def synthesize_with_weighting(
        self,
        query: str,
        model_responses: List[ModelResponse],
        internet_context: Optional[str] = None
    ) -> SynthesisResult:
        """
        Synthesize responses with confidence weighting
        """
        successful_responses = [r for r in model_responses if r.success]
        
        if not successful_responses:
            return SynthesisResult(
                query=query,
                primary_response="No successful responses from models.",
                supporting_evidence=[],
                confidence_score=0.0,
                consensus_level=0.0,
                model_votes={},
                reasoning_chain=[],
                sources=[]
            )
        
        # Analyze consensus
        consensus_analysis = self.analyze_consensus(model_responses)
        
        # Calculate weighted response (prioritize high-confidence responses)
        weighted_responses = []
        for response in successful_responses:
            weight = response.confidence_score * 0.7 + (
                1.0 - abs(response.confidence_score - consensus_analysis["consensus_score"])
            ) * 0.3
            weighted_responses.append((weight, response))
        
        weighted_responses.sort(key=lambda x: x[0], reverse=True)
        
        # Primary response from highest-weighted model
        primary_response = weighted_responses[0][1].response_text if weighted_responses else ""
        
        # Collect supporting evidence
        supporting_evidence = [
            f"**{r[1].provider.upper()} ({r[1].model}):** {r[1].response_text[:200]}..."
            for r in weighted_responses[1:3]
        ]
        
        # Calculate final confidence
        avg_confidence = sum(r.confidence_score for r in successful_responses) / len(successful_responses)
        final_confidence = (avg_confidence + consensus_analysis["consensus_score"]) / 2
        
        # Model votes (majority voting on key themes)
        model_votes = {}
        for resp in successful_responses:
            model_votes[resp.provider] = model_votes.get(resp.provider, 0) + 1
        
        # Build reasoning chain
        reasoning_chain = []
        for resp in weighted_responses[:3]:
            reasoning_chain.extend(resp[1].reasoning_steps)
        
        # Sources
        sources = [f"{r.provider}/{r.model}" for r in successful_responses]
        if internet_context:
            sources.append("Internet Search")
        
        return SynthesisResult(
            query=query,
            primary_response=primary_response,
            supporting_evidence=supporting_evidence,
            confidence_score=final_confidence,
            consensus_level=consensus_analysis["consensus_score"],
            model_votes=model_votes,
            reasoning_chain=reasoning_chain,
            sources=sources,
            internet_context=internet_context
        )


class AdvancedAIBrain:
    """
    Advanced AI Brain with reasoning, adaptive routing, and sophisticated synthesis
    """
    
    def __init__(self):
        self.reasoning_engine = AdvancedReasoningEngine()
        self.model_router = AdaptiveModelRouter()
        self.knowledge_synthesis = AdvancedKnowledgeSynthesis()
        self.learning_history: List[SynthesisResult] = []
        self.model_performance_history: Dict[str, Dict] = defaultdict(lambda: {"success": 0, "total": 0})
    
    def analyze_and_route(
        self,
        query: str,
        available_models: List[Dict]
    ) -> Tuple[QueryComplexity, List[Dict], float]:
        """
        Analyze query and recommend best models
        Returns: (complexity, ranked_models, complexity_score)
        """
        complexity, complexity_score = self.reasoning_engine.analyze_query_complexity(query)
        
        recommended_models = self.model_router.recommend_models(
            query,
            available_models,
            complexity,
            self.model_performance_history
        )
        
        return complexity, recommended_models, complexity_score
    
    def process_response(
        self,
        response_dict: Dict,
        model_info: Dict
    ) -> ModelResponse:
        """
        Process raw model response into enhanced ModelResponse
        """
        provider = response_dict.get("provider", "unknown")
        success = response_dict.get("success", False)
        response_text = response_dict.get("response", "")
        
        # Extract reasoning steps
        reasoning_steps = self.reasoning_engine.extract_reasoning_chain(response_text, model_info.get("model", ""))
        
        # Calculate confidence
        confidence_score = self._calculate_response_confidence(response_text, success)
        
        # Extract keywords
        keywords = self._extract_keywords(response_text)
        
        # Quality metrics
        quality_metrics = {
            "length_score": min(len(response_text) / 500, 1.0),
            "coherence_score": self._score_coherence(response_text),
            "specificity_score": self._score_specificity(response_text),
            "reasoning_depth": len(reasoning_steps) / 5.0
        }
        
        return ModelResponse(
            provider=provider,
            model=model_info.get("model", "unknown"),
            response_text=response_text,
            confidence_score=confidence_score,
            reasoning_steps=reasoning_steps,
            keywords_extracted=keywords,
            response_quality_metrics=quality_metrics,
            success=success,
            error=response_dict.get("error")
        )
    
    def _calculate_response_confidence(self, response_text: str, success: bool) -> float:
        """Calculate confidence score for a response"""
        if not success or not response_text:
            return 0.0
        
        score = 0.5  # Base score
        
        # Length (longer isn't always better, but extremely short is bad)
        if len(response_text) > 100:
            score += 0.15
        elif len(response_text) > 50:
            score += 0.08
        
        # Specific language
        if any(word in response_text.lower() for word in ['specifically', 'particularly', 'for example', 'like']):
            score += 0.15
        
        # Evidence of thinking
        if any(word in response_text.lower() for word in ['because', 'therefore', 'thus', 'since', 'as']):
            score += 0.10
        
        # Avoid hedging (unless appropriate)
        hedge_count = sum(1 for word in ['perhaps', 'might', 'could', 'maybe'] if word in response_text.lower())
        if hedge_count == 0:
            score += 0.05
        elif hedge_count > 3:
            score -= 0.10
        
        return min(max(score, 0.0), 1.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        words = text.lower().split()
        # Filter out common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been'}
        keywords = [w.strip('.,!?;:') for w in words if w.lower() not in stopwords and len(w) > 3]
        return list(set(keywords[:15]))
    
    def _score_coherence(self, text: str) -> float:
        """Score how coherent/well-structured the response is"""
        sentences = text.split('.')
        if len(sentences) < 2:
            return 0.4
        
        # Check for transitions
        transitions = ['furthermore', 'moreover', 'however', 'therefore', 'thus', 'additionally', 'finally']
        transition_count = sum(1 for t in transitions if t in text.lower())
        
        score = min(transition_count / 3.0, 1.0)
        return score
    
    def _score_specificity(self, text: str) -> float:
        """Score how specific and concrete the response is"""
        # Look for numbers, examples, specific terms
        has_numbers = any(c.isdigit() for c in text)
        has_examples = any(word in text.lower() for word in ['example', 'such as', 'like', 'for instance'])
        has_quotes = '"' in text or "'" in text
        
        score = 0.3
        if has_numbers:
            score += 0.25
        if has_examples:
            score += 0.25
        if has_quotes:
            score += 0.2
        
        return min(score, 1.0)
    
    def format_advanced_report(self, synthesis_result: SynthesisResult, complexity: QueryComplexity) -> str:
        """Format an advanced analysis report"""
        report = "# 🧠 Advanced Brain Analysis Report\n\n"
        
        # Header
        report += f"**Query:** {synthesis_result.query}\n"
        report += f"**Complexity Level:** {complexity.value.upper()}\n"
        report += f"**Generated:** {synthesis_result.synthesized_at}\n\n"
        
        # Confidence indicators
        report += "## 📊 Confidence & Consensus\n\n"
        confidence_pct = synthesis_result.confidence_score * 100
        consensus_pct = synthesis_result.consensus_level * 100
        
        report += f"- **Overall Confidence:** {confidence_pct:.1f}% "
        if confidence_pct >= 80:
            report += "✅ (Very High)\n"
        elif confidence_pct >= 60:
            report += "🟡 (High)\n"
        else:
            report += "⚠️ (Moderate)\n"
        
        report += f"- **Model Consensus:** {consensus_pct:.1f}% "
        if consensus_pct >= 75:
            report += "🔄 (Strong Agreement)\n"
        elif consensus_pct >= 50:
            report += "🔄 (Moderate Agreement)\n"
        else:
            report += "⚠️ (Low Agreement)\n"
        
        # Primary response
        report += "\n## 💬 Primary Response\n\n"
        report += synthesis_result.primary_response + "\n\n"
        
        # Supporting evidence
        if synthesis_result.supporting_evidence:
            report += "## 📚 Supporting Evidence\n\n"
            for evidence in synthesis_result.supporting_evidence:
                report += f"- {evidence}\n\n"
        
        # Reasoning chain
        if synthesis_result.reasoning_chain:
            report += "## 🔗 Reasoning Chain\n\n"
            for step in synthesis_result.reasoning_chain[:5]:
                report += f"**Step {step.step_number}** ({step.model}):\n"
                report += f"{step.reasoning}\n"
                report += f"_Confidence: {step.confidence * 100:.0f}%_\n\n"
        
        # Sources
        report += "## 🔍 Sources\n\n"
        for source in synthesis_result.sources:
            report += f"- {source}\n"
        
        # Model voting
        if synthesis_result.model_votes:
            report += "\n## 🗳️ Model Voting\n\n"
            for model, votes in sorted(synthesis_result.model_votes.items(), key=lambda x: x[1], reverse=True):
                report += f"- {model.upper()}: {votes} response(s)\n"
        
        return report


# Utility functions for integration
def create_advanced_brain() -> AdvancedAIBrain:
    """Factory function to create an advanced brain instance"""
    return AdvancedAIBrain()


def get_complexity_emoji(complexity: QueryComplexity) -> str:
    """Get emoji representation of complexity"""
    emoji_map = {
        QueryComplexity.SIMPLE: "🟢",
        QueryComplexity.MODERATE: "🟡",
        QueryComplexity.COMPLEX: "🟠",
        QueryComplexity.EXPERT: "🔴"
    }
    return emoji_map.get(complexity, "⚪")
