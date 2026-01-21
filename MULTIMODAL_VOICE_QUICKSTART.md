# 📎 Multimodal & Voice Features - Quick Start Guide

Get up and running with advanced multimodal and voice capabilities in 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 min)

```bash
# Core multimodal dependencies
pip install pillow python-docx PyPDF2

# Audio processing
pip install pydub librosa

# Video processing
pip install moviepy

# Choose your speech providers (pick at least one)
pip install google-cloud-texttospeech google-cloud-speech  # Google
pip install azure-cognitiveservices-speech                  # Azure
pip install openai                                          # OpenAI
pip install elevenlabs                                      # ElevenLabs
```

### Step 2: Set Up API Keys (2 min)

```bash
# Google Cloud (download key.json from Cloud Console)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Azure Speech Services
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"

# OpenAI
export OPENAI_API_KEY="your-key"

# ElevenLabs
export ELEVENLABS_API_KEY="your-key"
```

### Step 3: Basic Usage (1 min)

```python
from multimodal_advanced import MultimodalManager
from voice_advanced import TextToSpeech, TTSConfig

# Process a file
manager = MultimodalManager()
result = manager.process_file("photo.jpg")
print(result.to_dict())

# Generate speech
config = TTSConfig(
    provider="openai",
    voice_name="alloy",
    language="en-US"
)
tts = TextToSpeech(config)
audio, metadata = tts.synthesize("Hello, world!")
```

## 🎯 Common Tasks

### Task 1: Upload and Analyze Images

```python
from multimodal_advanced import ImageProcessor

# Validate image
is_valid, msg = ImageProcessor.validate_image("photo.jpg")
print(f"Valid: {is_valid}")

# Extract metadata (EXIF, dimensions, etc.)
metadata = ImageProcessor.extract_image_metadata("photo.jpg")
print(f"Image size: {metadata['width']}x{metadata['height']}")
print(f"EXIF: {metadata.get('exif', {})}")

# Optimize for AI processing
optimized = ImageProcessor.optimize_for_ai("photo.jpg")
# Save if needed: with open("optimized.png", "wb") as f: f.write(optimized)
```

### Task 2: Extract Text from Documents

```python
from multimodal_advanced import DocumentProcessor

# Extract from PDF
text, metadata = DocumentProcessor.extract_text_from_pdf("document.pdf")
print(f"Pages: {metadata['pages']}")
print(f"Text preview: {text[:200]}...")

# Extract from DOCX
text, metadata = DocumentProcessor.extract_text_from_docx("report.docx")

# Extract from CSV
text, metadata = DocumentProcessor.extract_csv_data("data.csv")
print(f"Rows: {metadata['rows']}, Columns: {metadata['columns']}")
```

### Task 3: Process Audio Files

```python
from multimodal_advanced import AudioProcessor

# Get duration
duration = AudioProcessor.get_audio_duration("speech.mp3")
print(f"Duration: {duration} seconds")

# Extract audio features
features = AudioProcessor.extract_audio_features("speech.mp3")
print(f"Sample rate: {features['sample_rate']}Hz")
print(f"Duration: {features['duration']}s")
print(f"Energy: {features['rms_energy']}")

# Normalize audio level
normalized = AudioProcessor.normalize_audio("speech.mp3")
# Save: with open("normalized.wav", "wb") as f: f.write(normalized)
```

### Task 4: Extract Video Frames

```python
from multimodal_advanced import VideoProcessor

# Get video info
info = VideoProcessor.get_video_info("movie.mp4")
print(f"Resolution: {info['resolution']}")
print(f"FPS: {info['fps']}")
print(f"Duration: {info['duration']}s")

# Extract 5 key frames
frames = VideoProcessor.extract_frames("movie.mp4", num_frames=5)
print(f"Extracted {len(frames)} frames")

# Create thumbnail at 5 second mark
thumb = VideoProcessor.create_video_thumbnail("movie.mp4", time_offset=5.0)
# Save: with open("thumb.png", "wb") as f: f.write(thumb)
```

### Task 5: Text-to-Speech (Multiple Providers)

```python
from voice_advanced import TextToSpeech, TTSConfig, VoiceProfile

# Google Cloud (Natural voice)
config = TTSConfig(
    provider="google",
    voice_name="en-US-Neural2-C",
    language="en-US",
    profile=VoiceProfile.NATURAL,
    speed=1.0
)
tts = TextToSpeech(config)
audio, _ = tts.synthesize("This is a test message.")

# OpenAI (Fast & reliable)
config = TTSConfig(
    provider="openai",
    voice_name="nova",
    language="en-US",
    profile=VoiceProfile.PROFESSIONAL,
    speed=1.1
)
tts = TextToSpeech(config)
audio, _ = tts.synthesize("Speaking clearly and naturally.")

# ElevenLabs (High quality)
config = TTSConfig(
    provider="elevenlabs",
    voice_name="bella",
    language="en-US",
    profile=VoiceProfile.FRIENDLY,
    speed=0.95
)
tts = TextToSpeech(config)
audio, _ = tts.synthesize("Hello from ElevenLabs!")

# Azure (Enterprise grade)
config = TTSConfig(
    provider="azure",
    voice_name="en-US-AriaNeural",
    language="en-US",
    profile=VoiceProfile.CALM,
    speed=1.0
)
tts = TextToSpeech(config)
audio, _ = tts.synthesize("Azure speech services.")
```

### Task 6: Speech-to-Text

```python
from voice_advanced import SpeechToText, STTConfig

# OpenAI Whisper (Recommended - no API needed locally)
config = STTConfig(
    provider="openai",
    language="en-US",
    enable_punctuation=True,
    enable_profanity_filter=True
)
stt = SpeechToText(config)
text, metadata = stt.transcribe("recording.mp3")
print(f"Transcribed: {text}")

# Google Cloud (For streaming)
config = STTConfig(
    provider="google",
    language="en-US",
    use_context_hints=True,
    context_hints=["Gemini", "AI", "Python"]
)
stt = SpeechToText(config)
text, metadata = stt.transcribe("audio.wav")

# Azure (Enterprise)
config = STTConfig(
    provider="azure",
    language="en-US",
    enable_profanity_filter=True
)
stt = SpeechToText(config)
text, metadata = stt.transcribe("audio.wav")
```

### Task 7: Streamlit Integration

```python
# Add to your app.py sidebar
import streamlit as st
from multimodal_voice_integration import add_multimodal_sidebar_section

# In your Streamlit app
add_multimodal_sidebar_section()

# Or use in main page
from multimodal_voice_integration import create_multimodal_features_page

if selected_page == "Multimodal":
    create_multimodal_features_page()
```

### Task 8: Voice Sessions

```python
from voice_advanced import VoiceSessionManager

manager = VoiceSessionManager()

# Create session
manager.create_session("session_001", "user_123")

# Add messages
manager.add_voice_message("session_001", "Hello, how are you?", 3.2, is_user=True)
manager.add_voice_message("session_001", "I'm doing great, thanks!", 2.8, is_user=False)
manager.add_voice_message("session_001", "That's wonderful to hear!", 2.1, is_user=True)

# Get statistics
stats = manager.get_session_stats("session_001")
print(f"Duration: {stats['duration']:.1f}s")
print(f"User messages: {stats['user_messages']}")
print(f"Assistant messages: {stats['assistant_messages']}")

# Close session
closed_session = manager.close_session("session_001")
```

### Task 9: Real-time Audio Recording

```python
from voice_advanced import RealTimeAudioProcessor

processor = RealTimeAudioProcessor(sample_rate=16000)

# Start recording
processor.start_recording()

# Simulate audio stream (in real app, get from microphone)
for chunk in audio_chunks:
    processor.add_audio_chunk(chunk)
    
    # Check audio level
    level = processor.get_audio_level(chunk)
    print(f"Audio level: {level:.2%}")
    
    # Detect silence
    if processor.detect_silence(chunk, threshold=0.02):
        print("Silence detected")

# Stop and get audio
final_audio = processor.stop_recording()
```

### Task 10: Batch Processing Multiple Files

```python
from multimodal_advanced import MultimodalManager
import os

manager = MultimodalManager()

# Process all files in a directory
input_dir = "uploads/"
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    try:
        result = manager.process_file(filepath)
        print(f"✅ {filename}: {result.media_type.value}")
    except Exception as e:
        print(f"❌ {filename}: {e}")

# Get summary
summary = manager.get_processing_summary()
print(f"\nTotal files: {summary['total_files']}")
print(f"By type: {summary['files_by_type']}")
print(f"Total size: {summary['total_size'] / 1024:.1f} KB")
```

## 📊 Configuration Presets

### Professional Voice
```python
config = TTSConfig(
    provider="google",
    voice_name="en-US-Neural2-C",
    profile=VoiceProfile.PROFESSIONAL,
    speed=0.95,
    pitch=1.0,
    volume_gain=1.0
)
```

### Friendly Voice
```python
config = TTSConfig(
    provider="openai",
    voice_name="nova",
    profile=VoiceProfile.FRIENDLY,
    speed=1.0,
    pitch=1.1,
    volume_gain=1.0
)
```

### Calm Voice
```python
config = TTSConfig(
    provider="elevenlabs",
    voice_name="bella",
    profile=VoiceProfile.CALM,
    speed=0.85,
    pitch=0.95,
    volume_gain=0.9
)
```

### Energetic Voice
```python
config = TTSConfig(
    provider="azure",
    voice_name="en-US-GuyNeural",
    profile=VoiceProfile.ENERGETIC,
    speed=1.2,
    pitch=1.1,
    volume_gain=1.0
)
```

## 🔍 Troubleshooting

### Issue: "Module not found"
```bash
# Install missing module
pip install <module-name>

# Example
pip install pillow  # For image processing
```

### Issue: "API Key not found"
```bash
# Check environment variable
echo $OPENAI_API_KEY

# Set it
export OPENAI_API_KEY="your-key-here"

# Or in code
import os
os.environ["OPENAI_API_KEY"] = "your-key-here"
```

### Issue: Audio file format not supported
```python
# Convert to supported format first
from multimodal_advanced import AudioProcessor

# Convert to WAV
wav_audio = AudioProcessor.convert_audio_format("input.m4a", "wav")
with open("converted.wav", "wb") as f:
    f.write(wav_audio)
```

### Issue: PDF extraction not working
```bash
# Install PyPDF2
pip install PyPDF2

# Test import
python -c "import PyPDF2; print('OK')"
```

## 💡 Tips & Tricks

1. **Cache results** - Save processed metadata for repeated files
2. **Batch process** - Process multiple files at once for efficiency
3. **Use threads** - Process different file types in parallel
4. **Monitor memory** - Large videos can use significant RAM
5. **Optimize images** - Resize before processing for speed
6. **Use closest provider** - Select API server closest to you
7. **Set timeouts** - Add timeout for long-running operations
8. **Log everything** - Use the built-in history tracking

## 📈 Next Steps

1. ✅ Choose your TTS provider (start with OpenAI)
2. ✅ Upload your first file (try an image)
3. ✅ Generate your first audio (use provided text)
4. ✅ Transcribe an audio file (use Whisper)
5. ✅ Create a voice session (for continuity)
6. ✅ Integrate with Streamlit (add to sidebar)
7. ✅ Combine with advanced brain (for context-aware responses)

## 🎓 Learning Resources

- [multimodal_advanced.py](multimodal_advanced.py) - Full source code
- [voice_advanced.py](voice_advanced.py) - Full source code
- [multimodal_voice_integration.py](multimodal_voice_integration.py) - Integration layer
- [MULTIMODAL_VOICE_GUIDE.md](MULTIMODAL_VOICE_GUIDE.md) - Complete documentation

---

**Need help?** Check the comprehensive guides or review the demo script for working examples!
