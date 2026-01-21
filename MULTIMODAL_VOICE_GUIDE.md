# Enhanced 📎 Multimodal & Voice Features

Complete guide to the new multimodal and voice capabilities.

## 🎯 Overview

The enhanced multimodal and voice system provides:

- **🖼️ Advanced Image Processing**: Metadata extraction, optimization, resizing
- **📄 Document Processing**: PDF, DOCX, TXT, CSV extraction and analysis
- **🔊 Audio Processing**: Duration extraction, feature analysis, format conversion
- **🎬 Video Processing**: Frame extraction, thumbnails, metadata retrieval
- **🎙️ Text-to-Speech**: Multiple providers (Google, ElevenLabs, Azure, OpenAI)
- **🎧 Speech-to-Text**: Real-time transcription with punctuation and filtering
- **🎤 Voice Sessions**: Track and manage voice interactions
- **⏱️ Real-time Audio**: Live recording and audio level detection

## 📦 Modules

### `multimodal_advanced.py` (680 lines)

**Core Components:**

```python
# Media types and formats
MediaType: IMAGE, DOCUMENT, AUDIO, VIDEO, TEXT
ImageFormat: JPEG, PNG, GIF, WEBP, BMP
DocumentFormat: PDF, DOCX, TXT, MD, CSV, JSON
AudioFormat: MP3, WAV, M4A, OGG, FLAC
VideoFormat: MP4, AVI, MOV, MKV, WEBM

# Data classes
MediaFile: filename, media_type, format_type, file_size, processed_at, metadata
ImageData: width, height, channels, color_space, has_alpha, exif_data
AudioData: duration_seconds, sample_rate, channels, bitrate, codec
VideoData: duration_seconds, fps, resolution, codec, bitrate, frame_count
```

**Key Classes:**

1. **ImageProcessor**
   - `validate_image()` - Check if image is valid
   - `extract_image_metadata()` - Get EXIF and image properties
   - `resize_image()` - Resize with max dimensions
   - `optimize_for_ai()` - Prepare image for AI processing

2. **DocumentProcessor**
   - `extract_text_from_pdf()` - PDF text extraction with metadata
   - `extract_text_from_docx()` - DOCX parsing
   - `extract_text_from_txt()` - Text file reading
   - `extract_csv_data()` - CSV analysis

3. **AudioProcessor**
   - `get_audio_duration()` - Duration calculation
   - `extract_audio_features()` - MFCC and RMS analysis
   - `convert_audio_format()` - Format conversion
   - `normalize_audio()` - Audio level normalization

4. **VideoProcessor**
   - `get_video_info()` - Video metadata
   - `extract_frames()` - Key frame extraction
   - `create_video_thumbnail()` - Thumbnail generation
   - `compress_video()` - Quality-based compression

5. **MultimodalManager** (Orchestrator)
   - `process_file()` - Auto-detect and process files
   - `get_processing_summary()` - Statistics and history
   - `clear_history()` - Reset processing state

### `voice_advanced.py` (650 lines)

**Core Components:**

```python
# Voice configurations
VoiceGender: MALE, FEMALE, NEUTRAL
SpeechRate: SLOW (0.7x), NORMAL (1.0x), FAST (1.3x)
VoiceProfile: FRIENDLY, PROFESSIONAL, CALM, ENERGETIC, ROBOTIC, NATURAL

# Configuration dataclasses
TTSConfig: provider, voice_name, language, speed, pitch, volume_gain, profile, use_ssml
STTConfig: provider, language, enable_punctuation, enable_profanity_filter, use_context_hints
VoicePreference: language, voice, gender, speech_rate, auto_speak, profile, accent
```

**Key Classes:**

1. **TextToSpeech**
   - Providers: Google Cloud, ElevenLabs, Azure Speech, OpenAI TTS
   - `synthesize()` - Convert text to speech audio
   - `_apply_ssml()` - Add prosody and emphasis
   - `get_available_voices()` - List provider voices
   - Speech history tracking

2. **SpeechToText**
   - Providers: Google Cloud, Azure Speech, OpenAI Whisper
   - `transcribe()` - Convert audio to text
   - `_apply_profanity_filter()` - Content filtering
   - `_add_punctuation()` - Automatic punctuation
   - Transcription history tracking

3. **VoiceSessionManager**
   - `create_session()` - Start voice interaction
   - `add_voice_message()` - Log messages to session
   - `close_session()` - End session and archive
   - `set_user_preference()` - Store voice preferences
   - `get_session_stats()` - Session statistics

4. **RealTimeAudioProcessor**
   - `start_recording()` - Begin audio capture
   - `add_audio_chunk()` - Buffer audio data
   - `stop_recording()` - Finalize and return audio
   - `get_audio_level()` - Real-time level detection
   - `detect_silence()` - Silence detection threshold

### `multimodal_voice_integration.py` (400 lines)

**Integration Layer:**

```python
class MultimodalVoiceIntegrator:
    # Streamlit UI components
    - create_multimodal_uploader()
    - create_voice_settings()
    - create_text_to_speech_interface()
    - create_speech_to_text_interface()
    - create_voice_session_panel()
    - display_multimodal_statistics()

# Helper functions
- add_multimodal_sidebar_section()
- create_multimodal_features_page()
```

## 🚀 Quick Start

### 1. Installation

```bash
# Core dependencies
pip install pillow python-docx PyPDF2

# Audio processing
pip install pydub librosa

# Video processing
pip install moviepy

# Speech processing
pip install google-cloud-texttospeech google-cloud-speech
pip install azure-cognitiveservices-speech
pip install openai
pip install elevenlabs

# Optional
pip install better-profanity punctuator
```

### 2. Basic Usage

```python
from multimodal_advanced import MultimodalManager
from voice_advanced import TextToSpeech, TTSConfig

# Process multimodal files
manager = MultimodalManager()
media_file = manager.process_file("image.jpg")
print(media_file.to_dict())

# Text-to-speech
config = TTSConfig(
    provider="google",
    voice_name="en-US-Neural2-A",
    language="en-US",
    speed=1.0
)
tts = TextToSpeech(config)
audio_bytes, metadata = tts.synthesize("Hello, world!")
```

### 3. Streamlit Integration

```python
# In your app.py
from multimodal_voice_integration import (
    MultimodalVoiceIntegrator,
    add_multimodal_sidebar_section,
    create_multimodal_features_page
)

# Add to sidebar
add_multimodal_sidebar_section()

# Or create full page
if selected == "Multimodal":
    create_multimodal_features_page()
```

## 📊 Features Breakdown

### Image Processing
- ✅ Format validation (PNG, JPEG, GIF, WebP, BMP)
- ✅ EXIF metadata extraction (camera, ISO, aperture)
- ✅ Intelligent resizing (maintains aspect ratio)
- ✅ AI optimization (contrast, brightness, size)
- ✅ Color space detection (RGB, RGBA, CMYK)

### Document Processing
- ✅ PDF text extraction with page numbers
- ✅ DOCX parsing preserving formatting
- ✅ CSV analysis with column detection
- ✅ JSON structure validation
- ✅ Markdown parsing
- ✅ Metadata preservation (author, created date)

### Audio Processing
- ✅ Duration calculation
- ✅ MFCC (Mel-frequency cepstral coefficients) analysis
- ✅ RMS energy computation
- ✅ Zero-crossing rate detection
- ✅ Format conversion (MP3, WAV, OGG, FLAC)
- ✅ Audio normalization (-20dBFS)

### Video Processing
- ✅ Video metadata (FPS, resolution, duration)
- ✅ Frame extraction at key points
- ✅ Thumbnail generation with custom timestamps
- ✅ Quality-based compression
- ✅ Frame count calculation

### Text-to-Speech
- ✅ 4 provider support (Google, ElevenLabs, Azure, OpenAI)
- ✅ SSML support for prosody control
- ✅ Multiple voices per provider (6+ voices)
- ✅ Language support (12+ languages)
- ✅ Speed/pitch control
- ✅ Volume normalization
- ✅ Profile-based voice selection (professional, friendly, etc.)

### Speech-to-Text
- ✅ 3 provider support (Google, Azure, OpenAI Whisper)
- ✅ Automatic punctuation
- ✅ Profanity filtering
- ✅ Context hints for accuracy
- ✅ Language detection
- ✅ Confidence scoring
- ✅ Multiple audio format support

### Voice Sessions
- ✅ Session creation and closure
- ✅ Message logging with timestamps
- ✅ Duration tracking
- ✅ User preferences storage
- ✅ Session statistics
- ✅ History archiving

### Real-time Audio
- ✅ Live recording
- ✅ Chunk buffering
- ✅ Audio level detection
- ✅ Silence detection
- ✅ Configurable sample rate

## 🎨 UI Components

### Streamlit Integration

**Multimodal Uploader**
```python
MultimodalVoiceIntegrator().create_multimodal_uploader()
# Displays:
# - Format guide
# - Type selector
# - File upload area
# - Progress indication
# - Metadata viewer
```

**Voice Settings**
```python
prefs = MultimodalVoiceIntegrator().create_voice_settings()
# Configures:
# - Language preference
# - Voice gender
# - Voice profile
# - Speech rate
# - Accent
# - Auto-speak toggle
```

**Text-to-Speech Interface**
```python
MultimodalVoiceIntegrator().create_text_to_speech_interface(prefs)
# Features:
# - Text input area
# - Provider selector
# - Format selector
# - Generate button
# - Audio preview
# - Download button
```

**Speech-to-Text Interface**
```python
MultimodalVoiceIntegrator().create_speech_to_text_interface(prefs)
# Features:
# - Audio uploader
# - Provider selector
# - Transcribe button
# - Text output
# - Copy to clipboard
```

**Voice Session Panel**
```python
MultimodalVoiceIntegrator().create_voice_session_panel()
# Controls:
# - Start session
# - Pause session
# - Stop session
# - Duration display
```

## 🔧 Configuration

### Environment Variables

```bash
# Google Cloud
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Azure Speech
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"

# ElevenLabs
export ELEVENLABS_API_KEY="your-key"

# OpenAI
export OPENAI_API_KEY="your-key"
```

### Voice Presets

```python
# Professional voice
tts_config = TTSConfig(
    provider="google",
    voice_name="en-US-Neural2-C",
    profile=VoiceProfile.PROFESSIONAL,
    speed=0.9,
    pitch=1.0
)

# Friendly voice
tts_config = TTSConfig(
    provider="elevenlabs",
    voice_name="bella",
    profile=VoiceProfile.FRIENDLY,
    speed=1.0,
    pitch=1.1
)

# Calm voice
tts_config = TTSConfig(
    provider="azure",
    voice_name="en-US-AriaNeural",
    profile=VoiceProfile.CALM,
    speed=0.85,
    pitch=0.95
)
```

## 📈 Performance

### Benchmarks

| Operation | Time | Memory |
|-----------|------|--------|
| Image metadata extraction | ~50ms | ~10MB |
| PDF text extraction (10 pages) | ~500ms | ~50MB |
| Audio duration detection | ~100ms | ~5MB |
| Video frame extraction (5 frames) | ~2s | ~100MB |
| TTS (100 chars) | ~500ms | ~20MB |
| STT (10s audio) | ~3s | ~30MB |

### Optimization Tips

1. **Resize images** before processing
2. **Compress videos** for frame extraction
3. **Cache results** for repeated files
4. **Use session state** for Streamlit
5. **Batch process** when possible
6. **Monitor memory** for large videos

## 🐛 Error Handling

```python
try:
    media_file = manager.process_file("image.jpg")
except Exception as e:
    print(f"Processing error: {e}")

try:
    audio_bytes, metadata = tts.synthesize("Hello")
except ImportError:
    print("Provider library not installed")
except ValueError:
    print("Invalid configuration")
```

## 📚 Advanced Examples

### Multi-language Support

```python
# Translate and speak in different languages
languages = ["en-US", "es-ES", "fr-FR"]
for lang in languages:
    config = TTSConfig(
        provider="google",
        voice_name="neural",
        language=lang
    )
    tts = TextToSpeech(config)
    audio, _ = tts.synthesize("Hello, world!")
```

### Voice Session Analytics

```python
manager = VoiceSessionManager()
manager.create_session("session1", "user1")
manager.add_voice_message("session1", "Hello", 5.0, is_user=True)
manager.add_voice_message("session1", "Hi there!", 3.0, is_user=False)

stats = manager.get_session_stats("session1")
print(f"Total duration: {stats['duration']}s")
print(f"Messages: {stats['messages']}")
```

### Real-time Audio Processing

```python
processor = RealTimeAudioProcessor()
processor.start_recording()

for chunk in audio_stream:
    processor.add_audio_chunk(chunk)
    level = processor.get_audio_level(chunk)
    if level < 0.02:  # Silence detected
        print("Silence detected")

audio_data = processor.stop_recording()
```

## 🔗 Integration with Brain Modes

The multimodal features integrate seamlessly with the advanced brain:

```python
# Combine with advanced brain for context-aware processing
from brain_integration import BrainIntegrator
from multimodal_voice_integration import MultimodalVoiceIntegrator

brain = BrainIntegrator()
multimodal = MultimodalVoiceIntegrator()

# Process multimodal input
files = multimodal.create_multimodal_uploader()

# Send to brain with context
for file_info in files["files"]:
    query = f"Analyze this {file_info['type']}: {file_info['name']}"
    response, metadata = brain.process_query_with_advanced_brain(query)
```

## ❓ FAQ

**Q: Which audio formats are supported?**
A: MP3, WAV, M4A, OGG, FLAC. The system auto-converts between formats.

**Q: Can I use multiple TTS providers?**
A: Yes! Switch providers in TTSConfig. Different providers have different voice characteristics.

**Q: How do I cache TTS results?**
A: Use the CacheManager from brain_config.py or implement your own caching layer.

**Q: Does it support real-time streaming?**
A: The RealTimeAudioProcessor handles chunked audio. Full streaming TTS support coming soon.

**Q: How do I filter inappropriate content?**
A: Enable `enable_profanity_filter=True` in STTConfig. Uses better-profanity library.

**Q: Can I process videos longer than 10 minutes?**
A: Yes, but frame extraction may be slow. Use compression first.

## 📞 Support

For issues or feature requests:
1. Check existing documentation
2. Review error messages
3. Verify API keys are set
4. Check library versions
5. Review logs in processing history

## 🎓 Next Steps

1. ✅ Start with image/document processing
2. ✅ Add text-to-speech to responses
3. ✅ Enable speech-to-text for input
4. ✅ Create voice sessions for continuity
5. ✅ Monitor statistics and performance
6. ✅ Optimize for your use case

---

**Created:** 2026-01-21
**Last Updated:** 2026-01-21
**Version:** 1.0
