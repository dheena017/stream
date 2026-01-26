# Troubleshooting Guide

Encountering issues? Here are some common problems and their solutions.

## API Key Issues

### "Missing API Key" Error
- **Symptom**: The chat returns an error starting with "Error: Missing API Key" or similar.
- **Cause**: The application cannot find the API key for the selected provider.
- **Solution**:
    1.  Check your `.env` file or `.streamlit/secrets.toml`.
    2.  Ensure the variable names are exact: `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
    3.  Restart the Streamlit app after making changes (`Ctrl+C` and run `streamlit run app.py` again).

### "Invalid API Key" or Auth Errors
- **Symptom**: 401 Unauthorized errors from the provider.
- **Solution**: Regenerate your key from the provider's console and update your configuration.

## Installation & Startup

### `ModuleNotFoundError`
- **Symptom**: `ModuleNotFoundError: No module named '...'`
- **Solution**:
    1.  Ensure you have activated your virtual environment.
    2.  Run `pip install -r requirements.txt` again.

### Streamlit Port Issues
- **Symptom**: "Port 8501 is already in use".
- **Solution**:
    - Streamlit will automatically try the next port (8502).
    - To force a specific port: `streamlit run app.py --server.port 8502`.
    - To kill the process using the port: `kill $(lsof -t -i :8501)` (Linux/Mac).

## Feature-Specific Issues

### Internet Search Returns No Results
- **Cause**: DuckDuckGo might be rate-limiting requests, or the query is too obscure.
- **Solution**: Try a different query. If the issue persists, check the logs for connection timeouts.

### Image Captioning is Slow or Fails
- **Cause**: Local BLIP model requires downloading heavy weights (approx 1GB) on the first run.
- **Solution**:
    - Wait for the download to complete. Check the terminal for progress bars.
    - If you see memory errors, ensure you have enough RAM or switch to a cloud-based multimodal provider (e.g., Gemini Vision).
    - If `torch` is not installed, the feature will gracefully degrade (return standard fallback text).

### Voice Input Not Working
- **Cause**: Browser permission denied or missing system libraries.
- **Solution**:
    - Allow microphone access in your browser.
    - On Linux, install `portaudio19-dev`.
