# Troubleshooting

Common issues and solutions for the Stream Multimodal AI Chat.

## API Key Issues

**Problem:** "Please configure API keys..." or authentication errors.

**Solution:**
1.  Check that you have entered a valid API key for the selected provider.
2.  If using environment variables, ensure they are set in the terminal *before* running Streamlit.
3.  Verify the variable names match exactly (e.g., `GEMINI_API_KEY`, not `GOOGLE_API_KEY`).
4.  Check the "🔑 API Keys" section in the sidebar to see if the key is recognized.

## Model Quotas

**Problem:** Errors like `429 Too Many Requests` or `Quota Exceeded`.

**Solution:**
1.  Switch to a different model (e.g., from `GPT-4` to `GPT-4o-mini`).
2.  Switch to a different provider (e.g., Google Gemini usually has a generous free tier).
3.  Check your billing status on the provider's dashboard.

## BLIP Model Downloads

**Problem:** The app hangs or is slow when "Advanced Image Captioning" is enabled.

**Solution:**
-   The first time this feature is used, it downloads a ~1GB model. This can take time depending on your internet connection.
-   Check your console output for download progress.
-   Ensure you have enough disk space.

## Audio/Video Processing Errors

**Problem:** "Audio processing failed" or "Video processing failed".

**Solution:**
-   Ensure you have `ffmpeg` installed on your system if `moviepy` or `pydub` are failing (though the app attempts to handle basic formats).
-   Verify the file is not corrupted and is a supported format (`.mp3`, `.wav`, `.mp4`).

## Streamlit Issues

**Problem:** "Port already in use".

**Solution:**
-   Streamlit will automatically try the next port (8502, 8503, etc.).
-   You can kill existing processes: `pkill -f streamlit` (Linux/Mac) or via Task Manager (Windows).
