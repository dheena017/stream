"""
Enhanced AI Brain with Learning Capabilities
Learns from model responses and improves over time
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json

# Limits to avoid unbounded growth
MAX_HISTORY = 200
MAX_KB_PER_TOPIC = 20
SUCCESS_RATE_WEIGHT = 10  # weight multiplier for global success rate
STATE_VERSION = 1


def search_internet(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the internet using DuckDuckGo"""
    try:
        from duckduckgo_search import DDGS  # type: ignore
        
        with DDGS() as ddgs:
            results = []
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('href', '')
                })
            return results
    except ImportError:
        return [{'title': 'Error', 'snippet': 'DuckDuckGo search requires: pip install duckduckgo-search', 'url': ''}]
    except Exception as e:
        return [{'title': 'Search Error', 'snippet': f'Search failed: {str(e)}', 'url': ''}]


def format_search_results(results: List[Dict[str, str]]) -> str:
    """Format search results into a readable string"""
    if not results:
        return "No search results found."
    
    formatted = "🌐 **Internet Search Results:**\n\n"
    for i, result in enumerate(results, 1):
        formatted += f"**{i}. {result['title']}**\n"
        formatted += f"{result['snippet']}\n"
        if result['url']:
            formatted += f"🔗 {result['url']}\n"
        formatted += "\n"
    return formatted


@dataclass
class KnowledgeEntry:
    query: str
    answers: List[str]
    timestamp: str
    models_used: List[str]


@dataclass
class ConversationRecord:
    query: str
    timestamp: str
    models: List[str]
    success_count: int


class LearningBrain:
    """AI Brain that learns from multiple models and internet"""
    
    def __init__(self):
        self.knowledge_base: Dict[str, List[KnowledgeEntry]] = {}  # Learned facts indexed by topic
        self.model_performance = {}  # Track success rates
        self.topic_expertise = {}  # Which models excel at which topics
        self.conversation_history: List[ConversationRecord] = []
        
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract simple keywords by filtering stopwords and short tokens."""
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was',
            'were', 'what', 'how', 'why', 'when', 'where', 'who', 'with', 'from', 'that', 'this',
            'these', 'those', 'into', 'about', 'also'
        }
        words = [w.strip('.,!?()[]{}"\'":;').lower() for w in text.split()]
        keywords: List[str] = []
        seen = set()
        for w in words:
            if len(w) <= 3 or w in common_words:
                continue
            if w in seen:
                continue
            seen.add(w)
            keywords.append(w)
            if len(keywords) >= 8:
                break
        return keywords

    def _normalize_response_text(self, response: Dict[str, Any]) -> str:
        text = response.get('response')
        if isinstance(text, str):
            return text.strip()
        payload = response.get('text') or response.get('content')
        return (payload or '').strip()

    def _is_successful_response(self, response: Dict[str, Any], normalized_text: Optional[str] = None) -> bool:
        normalized_text = normalized_text if normalized_text is not None else self._normalize_response_text(response)
        return bool(response.get('success')) or bool(normalized_text)
    
    def learn_from_responses(self, query: str, model_responses: List[Dict]):
        """Learn which models perform best and store concise knowledge snippets."""
        keywords = self._extract_keywords(query)
        if not keywords:
            keywords = ['general']
        now_ts = datetime.now().isoformat()
        successful_models: List[str] = []
        successful_answers: List[str] = []
        success_count = 0

        for response in model_responses:
            provider = response.get('provider', 'unknown')
            text = self._normalize_response_text(response)
            success = self._is_successful_response(response, text)

            if provider not in self.model_performance:
                self.model_performance[provider] = {'success': 0, 'total': 0, 'avg_length': 0}

            self.model_performance[provider]['total'] += 1
            if success:
                self.model_performance[provider]['success'] += 1
                response_length = len(text)
                current_avg = self.model_performance[provider]['avg_length']
                total_success = self.model_performance[provider]['success']
                self.model_performance[provider]['avg_length'] = (
                    (current_avg * (total_success - 1) + response_length) / total_success
                )

            if success:
                successful_models.append(provider)
                successful_answers.append(text)
                success_count += 1
                for keyword in keywords:
                    expertise = self.topic_expertise.setdefault(keyword, {})
                    expertise[provider] = expertise.get(provider, 0) + 1

        if successful_answers:
                unique_models = list(dict.fromkeys(successful_models))
                for keyword in keywords:
                    kb_entries = self.knowledge_base.setdefault(keyword, [])
                    entry = KnowledgeEntry(
                        query=query,
                        answers=successful_answers,
                        timestamp=now_ts,
                        models_used=unique_models or [r.get('provider', 'unknown') for r in model_responses]
                    )
                    if kb_entries and kb_entries[-1].query == entry.query and kb_entries[-1].answers == entry.answers:
                        continue
                    kb_entries.append(entry)
                if len(kb_entries) > MAX_KB_PER_TOPIC:
                    self.knowledge_base[keyword] = kb_entries[-MAX_KB_PER_TOPIC:]

        self.conversation_history.append(ConversationRecord(
            query=query,
            timestamp=now_ts,
            models=[r.get('provider', 'unknown') for r in model_responses],
            success_count=success_count
        ))
        if len(self.conversation_history) > MAX_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_HISTORY:]
    
    def recommend_models(self, query: str, available_models: List[str]) -> List[str]:
        """Recommend best models for a query using topic hits + global success rate."""
        keywords = self._extract_keywords(query)
        model_scores = {model: 0.0 for model in available_models}

        for model in available_models:
            topic_score = sum(
                self.topic_expertise.get(keyword, {}).get(model, 0) for keyword in keywords
            )
            perf_score = 0
            if model in self.model_performance:
                perf = self.model_performance[model]
                if perf['total'] > 0:
                    success_rate = perf['success'] / perf['total']
                    perf_score = success_rate * SUCCESS_RATE_WEIGHT
            model_scores[model] = topic_score + perf_score

        return sorted(model_scores.keys(), key=lambda m: model_scores[m], reverse=True)

    def summarize_model_strengths(self) -> List[Dict]:
        """Return a compact table of model success rates and top topics."""
        summary = []
        for model, perf in self.model_performance.items():
            success_rate = (perf['success'] / perf['total'] * 100) if perf['total'] else 0
            top_topics = []
            for topic, providers in self.topic_expertise.items():
                if providers.get(model):
                    top_topics.append((topic, providers[model]))
            top_topics.sort(key=lambda x: x[1], reverse=True)
            summary.append({
                'model': model,
                'success_rate': round(success_rate, 1),
                'total': perf['total'],
                'success': perf['success'],
                'top_topics': [t for t, _ in top_topics[:5]]
            })
        summary.sort(key=lambda x: x['success_rate'], reverse=True)
        return summary
    
    def get_related_knowledge(self, query: str, limit: int = 3) -> List[Dict]:
        """Retrieve related knowledge from past conversations"""
        keywords = self._extract_keywords(query)
        related = []
        
        for keyword in keywords:
            if keyword in self.knowledge_base:
                related.extend(self.knowledge_base[keyword][-limit:])
        related.sort(key=lambda x: x.timestamp if hasattr(x, 'timestamp') else '', reverse=True)
        return [asdict(entry) for entry in related[:limit]]
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about what the brain has learned"""
        stats = {
            'total_topics': len(self.knowledge_base),
            'total_conversations': len(self.conversation_history),
            'models_tracked': len(self.model_performance),
            'model_performance': {},
            'top_topics': [],
            'model_strengths': self.summarize_model_strengths()
        }
        
        # Model performance
        for provider, perf in self.model_performance.items():
            success_rate = (perf['success'] / perf['total'] * 100) if perf['total'] > 0 else 0
            stats['model_performance'][provider] = {
                'success_rate': round(success_rate, 1),
                'total_queries': perf['total'],
                'successful_queries': perf['success'],
                'avg_response_length': round(perf['avg_length'], 0)
            }
        
        # Top topics
        top_topics = sorted(self.knowledge_base.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        stats['top_topics'] = [{'topic': topic, 'count': len(entries)} for topic, entries in top_topics]
        
        return stats
    
    def format_learning_report(self) -> str:
        """Format a readable learning report"""
        stats = self.get_learning_stats()
        
        report = "# 🧠 AI Brain Learning Report\n\n"
        report += f"**Total Knowledge Topics:** {stats['total_topics']}\n"
        report += f"**Total Conversations:** {stats['total_conversations']}\n"
        report += f"**Models Tracked:** {stats['models_tracked']}\n\n"
        
        report += "## 📊 Model Performance\n\n"
        for provider, perf in stats['model_performance'].items():
            report += f"### {provider.upper()}\n"
            report += f"- Success Rate: **{perf['success_rate']}%** ({perf['successful_queries']}/{perf['total_queries']})\n"
            report += f"- Avg Response Length: {perf['avg_response_length']} chars\n\n"
        
        report += "## 📚 Top Knowledge Topics\n\n"
        for topic_info in stats['top_topics']:
            report += f"- **{topic_info['topic']}**: {topic_info['count']} conversations\n"

        if stats['model_strengths']:
            report += "\n## 🏅 Model Strengths\n\n"
            for row in stats['model_strengths']:
                topics = ', '.join(row['top_topics']) if row['top_topics'] else '—'
                report += (
                    f"- **{row['model']}**: {row['success_rate']}% success"
                    f" ({row['success']}/{row['total']}); top topics: {topics}\n"
                )
        
        report += f"\n---\n💡 *The brain is learning! It now knows which models work best for different topics.*\n"
        
        return report

    def register_feedback(self, provider: str, success: bool):
        """Allow manual feedback to nudge performance stats."""
        if provider not in self.model_performance:
            self.model_performance[provider] = {'success': 0, 'total': 0, 'avg_length': 0}
        self.model_performance[provider]['total'] += 1
        if success:
            self.model_performance[provider]['success'] += 1

    def reset_learning(self):
        """Reset all learned data."""
        self.knowledge_base = {}
        self.model_performance = {}
        self.topic_expertise = {}
        self.conversation_history = []
    
    def export_knowledge(self) -> str:
        """Export all learned knowledge as JSON"""
        export_data = {
              'knowledge_base': {
                 topic: [asdict(entry) for entry in entries]
                 for topic, entries in self.knowledge_base.items()
              },
              'model_performance': self.model_performance,
              'topic_expertise': self.topic_expertise,
              'conversation_history': [asdict(record) for record in self.conversation_history],
            'exported_at': datetime.now().isoformat(),
            'version': STATE_VERSION
        }
        return json.dumps(export_data, indent=2)
    
    def import_knowledge(self, json_data: str):
        """Import previously learned knowledge"""
        try:
            data = json.loads(json_data)
            raw_kb = data.get('knowledge_base', {})
            self.knowledge_base = {
                topic: [KnowledgeEntry(**entry) for entry in entries]
                for topic, entries in raw_kb.items()
            }
            self.model_performance = data.get('model_performance', {})
            self.topic_expertise = data.get('topic_expertise', {})
            history = data.get('conversation_history', [])
            self.conversation_history = [ConversationRecord(**record) for record in history]
            return True
        except Exception:
            return False

    def save_to_file(self, path: str) -> bool:
        """Persist learning state to disk."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.export_knowledge())
            return True
        except Exception:
            return False

    def load_from_file(self, path: str) -> bool:
        """Load learning state from disk."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
            return self.import_knowledge(data)
        except FileNotFoundError:
            return False
        except Exception:
            return False
