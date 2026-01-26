# Internet Search Integration Guide

## Overview
The Internet Search feature has been integrated into the Antigravity AI chat application, allowing users to augment AI responses with real-time web information powered by DuckDuckGo.

## Features

### 1. **Web Search**
   - Real-time search of the internet for current information
   - Returns up to 10 results per query
   - Extracts title, description, and source URL

### 2. **Search Display**
   - Search results are displayed in an expandable section
   - Results show title, source domain, description, and URL
   - Easy-to-read formatted output

### 3. **Prompt Augmentation**
   - Search results are automatically integrated into the AI prompt
   - Allows AI models to provide responses based on current web information
   - Improves accuracy for time-sensitive queries

### 4. **Status Indicator**
   - New status bar showing "🌐 Web ON" or "📱 Local" mode
   - Quick visual feedback on search capability status

## How to Use

### Enabling Internet Search

1. **In Chat Interface:**
   - Check the "🌐 Enable Internet Search" checkbox
   - Adjust "Results" slider (1-10) for number of search results
   - Select search type: "Web" or "News"

2. **Default Settings:**
   - Internet search is disabled by default
   - Can be enabled/disabled per message
   - Search result count defaults to 5

### Search Workflow

```
User Message
    ↓
Enable Internet Search? (if yes)
    ↓
Perform DuckDuckGo Search
    ↓
Display Results to User
    ↓
Augment Prompt with Search Context
    ↓
Send Enhanced Prompt to AI Model
    ↓
Display AI Response
```

## Module Structure

### `ui/internet_search.py`
Main Internet Search module containing:

#### Classes:
- **`InternetSearchEngine`**: Wrapper around DuckDuckGo API
  - `search()`: General web search
  - `search_news()`: News-specific search
  - `search_images()`: Image search (experimental)
  - `fetch_url_content()`: Retrieve full content from URLs

#### Functions:
- `format_search_results_for_chat()`: Format results for display
- `create_search_context()`: Prepare search results for AI processing

### `ui/chat_utils.py`
Enhanced with search functions:

- `get_internet_search_engine()`: Cached search engine initialization
- `perform_internet_search()`: Wrapper to execute searches
- `augment_prompt_with_search()`: Integrate search results into prompts

### `ui/chat.py`
UI integration:

- Internet search checkbox and configuration
- Search results display
- Automatic prompt augmentation

### `app.py`
Session state management:

- `enable_internet_search`: Enable/disable search
- `search_result_count`: Number of results to fetch

## API Details

### Internet Search Engine

```python
from ui.internet_search import InternetSearchEngine

engine = InternetSearchEngine(timeout=10)

# Web Search
results = engine.search("latest AI news", max_results=5)

# News Search
news = engine.search_news("stock market", max_results=5)

# Image Search
images = engine.search_images("nature photography", max_results=5)

# Fetch URL Content
content = engine.fetch_url_content("https://example.com")
```

### Result Format

Each search result is a dictionary containing:

```python
{
    'title': str,          # Result title
    'body': str,           # Result description/snippet
    'href': str,           # Full URL
    'source': str          # Domain name
}
```

## Configuration

### Search Settings

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| Enable Search | False | - | Toggle internet search on/off |
| Result Count | 5 | 1-10 | Number of search results |
| Search Type | Web | Web/News | Type of search to perform |
| Timeout | 10s | - | API timeout in seconds |

## Performance Considerations

- **Search Latency**: ~1-3 seconds per search
- **Prompt Size**: Search results increase context window
- **API Rate Limiting**: DuckDuckGo has fair use limits
- **Cache**: Search engine is cached for performance

## Error Handling

- **No Results**: Returns empty list, continues without search context
- **Network Errors**: Gracefully falls back to local-only mode
- **Timeout**: Uses default timeout of 10 seconds
- **Logging**: All errors logged for debugging

## Best Practices

1. **Enable Search for Time-Sensitive Queries:**
   - Current events
   - Latest news
   - Real-time stock prices
   - Recent research

2. **Disable Search for:**
   - General knowledge questions
   - Historical information
   - Privacy-sensitive queries
   - Offline usage

3. **Optimize Results:**
   - Use specific keywords
   - Start with 5 results, adjust as needed
   - Check "Web" vs "News" for appropriate content type

## Limitations

- DuckDuckGo results may vary in comprehensiveness
- No authentication required, but subject to rate limiting
- News search availability depends on feed availability
- Image search limited to URL extraction

## Future Enhancements

- [ ] Support for multiple search engines (Google, Bing)
- [ ] Advanced search filters (date range, language)
- [ ] Search result caching
- [ ] Custom search operators
- [ ] Integration with browser history
- [ ] Search analytics and usage statistics

## Troubleshooting

### Search Not Working
- Check internet connection
- Verify DuckDuckGo is accessible
- Check timeout settings
- Review logs for error messages

### Slow Searches
- Reduce number of results
- Increase timeout value
- Check network bandwidth
- Consider disabling for local queries

### Prompt Too Long
- Reduce search result count
- Use more specific search queries
- Enable summarization (future feature)

## Examples

### Example 1: Current News Query
```
User: "What are the latest developments in AI?"
Search: Enabled, 5 results
Result: Gets latest AI news from web
Response: AI-generated answer with current information
```

### Example 2: Local Knowledge Query
```
User: "Explain machine learning"
Search: Disabled
Result: No web search performed
Response: AI-generated answer from training data
```

### Example 3: Mixed Query
```
User: "Who won the latest Nobel Prize and explain their work"
Search: Enabled, 3 results
Result: Gets latest Nobel Prize winner
Response: Combined with AI's knowledge of their research
```

## Dependencies

- `duckduckgo-search`: For web search API
- `requests`: For URL content fetching
- `streamlit`: For UI integration
- Standard library: `logging`, `typing`, `urllib`, `html.parser`

## Code Examples

### Basic Search Usage
```python
from ui.chat_utils import perform_internet_search

# Perform search
results, context = perform_internet_search(
    query="Python programming tips",
    enable_search=True,
    max_results=5
)

# Use in prompt
augmented_prompt = augment_prompt_with_search(
    "What are best practices?",
    results
)
```

### Custom Search Engine
```python
from ui.internet_search import InternetSearchEngine

engine = InternetSearchEngine(timeout=15)
results = engine.search("your query", max_results=3)

for result in results:
    print(f"Title: {result['title']}")
    print(f"Source: {result['source']}")
    print(f"URL: {result['href']}")
    print(f"Summary: {result['body']}\n")
```

## Support & Feedback

For issues or suggestions regarding Internet Search:
1. Check logs for error details
2. Verify dependencies are installed
3. Test internet connectivity
4. Review DuckDuckGo API status

---

**Last Updated**: January 21, 2026
**Version**: 1.0
