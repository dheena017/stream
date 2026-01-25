# Troubleshooting Guide

## Login Issues

### "Invalid email/username or password"
-   Ensure you are using the correct credentials.
-   **Default Admin:** `admin` / `admin123`
-   **Default User:** `user` / `user123`
-   If you registered a new account, ensure you are typing the password exactly as created.

### Google Login Not Working
-   If the "Sign in with Google" button is missing or returns an error:
    1.  Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_REDIRECT_URI` are set in your environment variables.
    2.  Check that the Authorized Javascript Origins and Redirect URIs in your Google Cloud Console match your running application (usually `http://localhost:8501`).

## Application Issues

### App fails to start
-   Check your python environment:
    ```bash
    python --version  # Should be 3.8+
    pip install -r requirements.txt
    ```
-   Ensure no other service is using port 8501.

### "Module not found" errors
-   Make sure you have installed all dependencies:
    ```bash
    pip install -r requirements.txt
    ```
-   If using optional features (like BLIP), you may need additional packages:
    ```bash
    pip install transformers torch torchvision
    ```

## Feature Issues

### Internet Search Not Working
-   **Rate Limits:** DuckDuckGo may rate limit requests if too many are made in a short time. Wait a few moments and try again.
-   **Connection:** Ensure your server has internet access.
-   **Logs:** Check the terminal output for specific error messages from `duckduckgo_search`.

### Advanced Image Captioning (BLIP) Slow
-   **First Run:** On the first use, the app downloads a large model (~1GB). This can take time depending on your internet speed.
-   **Performance:** Running BLIP on a CPU (without NVIDIA GPU) is slow. Consider using the **Hosted Caption API** option if local performance is poor. See [Hosted Caption Setup](HOSTED_CAPTION_SETUP.md) for details.

### Voice Input Not Working
-   Ensure your browser has permission to access your microphone.
-   If running remotely, audio input might not pass through to the server unless you are using a secure context (HTTPS) or localhost.

## Still Stuck?
-   Check the logs in your terminal for detailed error messages.
-   Reset the application by stopping (Ctrl+C) and restarting `streamlit run app.py`.
