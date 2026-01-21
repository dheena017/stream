"""
Interactive Demo: Advanced Multimodal & Voice Features
Demonstrates all capabilities of the multimodal and voice systems
"""

from multimodal_advanced import (
    MultimodalManager, ImageProcessor, DocumentProcessor,
    AudioProcessor, VideoProcessor, MediaType
)
from voice_advanced import (
    TextToSpeech, SpeechToText, VoiceSessionManager,
    TTSConfig, STTConfig, VoicePreference, VoiceProfile, VoiceGender, SpeechRate
)
from multimodal_voice_integration import MultimodalVoiceIntegrator
import json
from datetime import datetime


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_image_processing():
    """Demonstrate image processing capabilities"""
    print_section("📸 IMAGE PROCESSING DEMO")
    
    print("Available operations:")
    print("1. Validate image file")
    print("2. Extract metadata (EXIF, dimensions, etc.)")
    print("3. Resize image intelligently")
    print("4. Optimize for AI processing")
    
    print("\nExample image processing flow:")
    print("""
    # Validate image
    is_valid, msg = ImageProcessor.validate_image("photo.jpg")
    
    # Extract metadata
    metadata = ImageProcessor.extract_image_metadata("photo.jpg")
    print(f"Size: {metadata['width']}x{metadata['height']}")
    
    # Optimize for AI
    optimized = ImageProcessor.optimize_for_ai("photo.jpg")
    """)
    
    print("\n✅ Image Processing ready to use!")


def demo_document_processing():
    """Demonstrate document processing capabilities"""
    print_section("📄 DOCUMENT PROCESSING DEMO")
    
    print("Supported formats:")
    print("• PDF - with page numbers and metadata")
    print("• DOCX - preserving structure")
    print("• TXT - with line/word counts")
    print("• CSV - with column analysis")
    print("• JSON - structure validation")
    print("• Markdown - parsing support")
    
    print("\nExample document extraction:")
    print("""
    # Extract from PDF
    text, metadata = DocumentProcessor.extract_text_from_pdf("doc.pdf")
    print(f"Pages: {metadata['pages']}")
    
    # Extract from CSV
    text, data = DocumentProcessor.extract_csv_data("data.csv")
    print(f"Rows: {data['rows']}, Columns: {data['columns']}")
    """)
    
    print("\n✅ Document Processing ready to use!")


def demo_audio_processing():
    """Demonstrate audio processing capabilities"""
    print_section("🔊 AUDIO PROCESSING DEMO")
    
    print("Audio operations available:")
    print("1. Get duration and sample rate")
    print("2. Extract audio features (MFCC, RMS energy)")
    print("3. Convert between formats")
    print("4. Normalize audio levels")
    print("5. Detect silence")
    
    print("\nExample audio analysis:")
    print("""
    # Get duration
    duration = AudioProcessor.get_audio_duration("speech.mp3")
    
    # Extract features
    features = AudioProcessor.extract_audio_features("speech.mp3")
    print(f"Sample rate: {features['sample_rate']}Hz")
    print(f"Energy: {features['rms_energy']:.4f}")
    
    # Normalize
    normalized = AudioProcessor.normalize_audio("speech.mp3")
    """)
    
    print("\n✅ Audio Processing ready to use!")


def demo_video_processing():
    """Demonstrate video processing capabilities"""
    print_section("🎬 VIDEO PROCESSING DEMO")
    
    print("Video operations available:")
    print("1. Extract video metadata (FPS, resolution, duration)")
    print("2. Extract key frames")
    print("3. Generate thumbnails")
    print("4. Compress for processing")
    
    print("\nExample video analysis:")
    print("""
    # Get video info
    info = VideoProcessor.get_video_info("movie.mp4")
    print(f"Resolution: {info['resolution']}")
    print(f"Duration: {info['duration']:.1f}s")
    
    # Extract frames
    frames = VideoProcessor.extract_frames("movie.mp4", num_frames=5)
    
    # Create thumbnail
    thumb = VideoProcessor.create_video_thumbnail("movie.mp4", time_offset=5.0)
    """)
    
    print("\n✅ Video Processing ready to use!")


def demo_text_to_speech():
    """Demonstrate text-to-speech capabilities"""
    print_section("🔊 TEXT-TO-SPEECH DEMO")
    
    print("Available TTS Providers:")
    print("1. 🔵 Google Cloud - Natural neural voices, 30+ languages")
    print("2. 🟡 ElevenLabs - High-quality voices, realistic speech")
    print("3. 🟢 Azure Speech - Enterprise-grade, multilingual")
    print("4. 🔴 OpenAI - Fast, reliable, natural voices")
    
    print("\nVoice Profiles:")
    for profile in VoiceProfile:
        print(f"  • {profile.value.capitalize()}")
    
    print("\nExample TTS configurations:")
    print("""
    # Professional voice
    config = TTSConfig(
        provider="google",
        voice_name="en-US-Neural2-C",
        profile=VoiceProfile.PROFESSIONAL,
        speed=0.95
    )
    
    # Friendly voice
    config = TTSConfig(
        provider="elevenlabs",
        voice_name="bella",
        profile=VoiceProfile.FRIENDLY,
        speed=1.0
    )
    
    # Calm voice
    config = TTSConfig(
        provider="azure",
        voice_name="en-US-AriaNeural",
        profile=VoiceProfile.CALM,
        speed=0.85
    )
    """)
    
    print("\nTTS Features:")
    print("✅ SSML support (prosody, emphasis)")
    print("✅ Speed control (0.5x to 2.0x)")
    print("✅ Pitch adjustment")
    print("✅ Volume normalization")
    print("✅ Multiple output formats (MP3, WAV, OGG)")
    
    print("\n✅ Text-to-Speech ready to use!")


def demo_speech_to_text():
    """Demonstrate speech-to-text capabilities"""
    print_section("🎙️ SPEECH-TO-TEXT DEMO")
    
    print("Available STT Providers:")
    print("1. 🔵 Google Cloud - Streaming, context hints")
    print("2. 🟢 Azure Speech - Enterprise, real-time")
    print("3. 🔴 OpenAI Whisper - Offline capable, accurate")
    
    print("\nSTT Features:")
    print("✅ Automatic punctuation")
    print("✅ Profanity filtering")
    print("✅ Context hints for accuracy")
    print("✅ Multiple language support")
    print("✅ Confidence scoring")
    
    print("\nExample STT usage:")
    print("""
    # OpenAI Whisper (Recommended)
    config = STTConfig(
        provider="openai",
        language="en-US",
        enable_punctuation=True,
        enable_profanity_filter=True
    )
    
    stt = SpeechToText(config)
    text, metadata = stt.transcribe("recording.mp3")
    print(f"Transcribed: {text}")
    """)
    
    print("\n✅ Speech-to-Text ready to use!")


def demo_voice_sessions():
    """Demonstrate voice session management"""
    print_section("🎤 VOICE SESSIONS DEMO")
    
    print("Voice session features:")
    print("• Create sessions with user context")
    print("• Log voice messages with timestamps")
    print("• Track duration and message count")
    print("• Store user preferences")
    print("• Archive session history")
    
    print("\nExample voice session:")
    print("""
    manager = VoiceSessionManager()
    
    # Create session
    manager.create_session("session_001", "user_123")
    
    # Add voice messages
    manager.add_voice_message("session_001", "Hello!", 2.5, is_user=True)
    manager.add_voice_message("session_001", "Hi there!", 2.0, is_user=False)
    
    # Get statistics
    stats = manager.get_session_stats("session_001")
    print(f"Duration: {stats['duration']:.1f}s")
    print(f"Messages: {stats['messages']}")
    
    # Close session
    closed = manager.close_session("session_001")
    """)
    
    print("\n✅ Voice Sessions ready to use!")


def demo_voice_preferences():
    """Demonstrate voice preference management"""
    print_section("🎵 VOICE PREFERENCES DEMO")
    
    print("Customizable voice preferences:")
    print(f"• Language: Multiple options (en-US, es-ES, fr-FR, etc.)")
    print(f"• Gender: {', '.join(g.value for g in VoiceGender)}")
    print(f"• Speed: {', '.join(str(s.value) + 'x' for s in SpeechRate)}")
    print(f"• Profiles: {', '.join(p.value for p in VoiceProfile)}")
    print(f"• Accents: standard, british, indian, australian")
    
    print("\nExample preference configuration:")
    print("""
    preferences = VoicePreference(
        preferred_language="en-US",
        preferred_gender=VoiceGender.FEMALE,
        speech_rate=SpeechRate.NORMAL,
        voice_profile=VoiceProfile.PROFESSIONAL,
        auto_speak_responses=True,
        accent="british"
    )
    
    # Use preferences in TTS
    config = TTSConfig(
        provider="google",
        voice_name="en-US-Neural2-C",
        speed=preferences.speech_rate.value,
        profile=preferences.voice_profile
    )
    """)
    
    print("\n✅ Voice Preferences ready to use!")


def demo_real_time_audio():
    """Demonstrate real-time audio processing"""
    print_section("⏱️ REAL-TIME AUDIO DEMO")
    
    print("Real-time audio capabilities:")
    print("• Live audio recording")
    print("• Chunk-based buffering")
    print("• Real-time audio level detection")
    print("• Silence detection")
    print("• Configurable sample rates")
    
    print("\nExample real-time recording:")
    print("""
    from voice_advanced import RealTimeAudioProcessor
    
    processor = RealTimeAudioProcessor(sample_rate=16000)
    processor.start_recording()
    
    for chunk in audio_stream:
        processor.add_audio_chunk(chunk)
        
        # Check audio level
        level = processor.get_audio_level(chunk)
        print(f"Level: {level:.2%}")
        
        # Detect silence
        if processor.detect_silence(chunk, threshold=0.02):
            print("Silence detected - could auto-stop")
    
    audio_data = processor.stop_recording()
    """)
    
    print("\n✅ Real-Time Audio ready to use!")


def demo_multimodal_manager():
    """Demonstrate multimodal manager"""
    print_section("🎯 MULTIMODAL MANAGER DEMO")
    
    print("MultimodalManager features:")
    print("• Auto-detect file types")
    print("• Process multiple formats")
    print("• Track processing history")
    print("• Generate summary statistics")
    print("• Clear and archive data")
    
    print("\nExample usage:")
    print("""
    from multimodal_advanced import MultimodalManager
    
    manager = MultimodalManager()
    
    # Process file (auto-detects type)
    result = manager.process_file("image.jpg")
    print(f"Type: {result.media_type.value}")
    print(f"Metadata: {result.metadata}")
    
    # Get summary
    summary = manager.get_processing_summary()
    print(f"Total files: {summary['total_files']}")
    print(f"By type: {summary['files_by_type']}")
    print(f"Total size: {summary['total_size']} bytes")
    """)
    
    print("\n✅ Multimodal Manager ready to use!")


def demo_integration_with_streamlit():
    """Demonstrate Streamlit integration"""
    print_section("🎨 STREAMLIT INTEGRATION DEMO")
    
    print("Integration functions available:")
    print("""
    1. add_multimodal_sidebar_section()
       - Adds complete multimodal/voice UI to sidebar
       - Auto-handles file uploads
       - Displays statistics
    
    2. create_multimodal_features_page()
       - Full-page multimodal interface
       - Tabbed layout
       - All features in one place
    
    3. MultimodalVoiceIntegrator class
       - Fine-grained control
       - Custom UI layouts
       - Flexible integration
    """)
    
    print("\nExample Streamlit usage:")
    print("""
    # In your app.py
    import streamlit as st
    from multimodal_voice_integration import add_multimodal_sidebar_section
    
    # Add to sidebar
    add_multimodal_sidebar_section()
    
    # Or create full page
    st.set_page_config(page_title="AI Brain with Multimodal")
    
    pages = {
        "Chat": chat_page,
        "Multimodal": lambda: create_multimodal_features_page(),
        "Settings": settings_page
    }
    
    page = st.sidebar.selectbox("Pages", pages.keys())
    pages[page]()
    """)
    
    print("\n✅ Streamlit Integration ready to use!")


def demo_batch_processing():
    """Demonstrate batch processing"""
    print_section("📦 BATCH PROCESSING DEMO")
    
    print("Example: Process multiple files efficiently")
    print("""
    from multimodal_advanced import MultimodalManager
    import os
    
    manager = MultimodalManager()
    
    # Process directory
    for filename in os.listdir("uploads/"):
        if filename.endswith(('.jpg', '.pdf', '.mp3', '.mp4')):
            try:
                result = manager.process_file(f"uploads/{filename}")
                print(f"✅ {filename}: {result.media_type.value}")
            except Exception as e:
                print(f"❌ {filename}: {e}")
    
    # Get summary
    summary = manager.get_processing_summary()
    print(f"\\nProcessed {summary['total_files']} files")
    print(f"Types: {summary['files_by_type']}")
    print(f"Total size: {summary['total_size'] / 1024:.1f} KB")
    """)
    
    print("\n✅ Batch Processing ready to use!")


def demo_error_handling():
    """Demonstrate error handling"""
    print_section("🛡️ ERROR HANDLING DEMO")
    
    print("Best practices for error handling:")
    print("""
    # Always wrap in try-except
    try:
        manager = MultimodalManager()
        result = manager.process_file("file.jpg")
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Unsupported file format")
    except ImportError:
        print("Required library not installed: pip install <library>")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Check if provider is available
    try:
        from openai import OpenAI
        provider = "openai"
    except ImportError:
        print("OpenAI not installed, using Google Cloud")
        provider = "google"
    
    # Set timeouts for long operations
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Operation took too long")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30)  # 30 second timeout
    
    try:
        result = process_large_video("video.mp4")
    finally:
        signal.alarm(0)  # Cancel alarm
    """)
    
    print("\n✅ Error Handling ready to use!")


def demo_performance_tips():
    """Demonstrate performance optimization"""
    print_section("⚡ PERFORMANCE OPTIMIZATION TIPS")
    
    tips = {
        "Image Processing": [
            "Resize images before analysis (max 2048x2048)",
            "Use JPEG for photos, PNG for graphics",
            "Enable AI optimization for better results"
        ],
        "Document Processing": [
            "Extract text first, analyze second",
            "Use CSV parser for large datasets",
            "Cache metadata for repeated files"
        ],
        "Audio Processing": [
            "Normalize audio before transcription",
            "Use WAV for highest quality",
            "Convert to MP3 for streaming"
        ],
        "Video Processing": [
            "Extract specific frames, not full video",
            "Use compression for initial analysis",
            "Generate thumbnails at low resolution"
        ],
        "Speech Processing": [
            "Batch TTS requests when possible",
            "Cache audio responses",
            "Use streaming for long texts",
            "Choose closest provider region"
        ]
    }
    
    for category, tips_list in tips.items():
        print(f"\n{category}:")
        for tip in tips_list:
            print(f"  • {tip}")
    
    print("\n✅ Performance Optimization ready to use!")


def demo_advanced_features():
    """Demonstrate advanced features"""
    print_section("🚀 ADVANCED FEATURES DEMO")
    
    print("Advanced scenarios you can implement:")
    print("""
    1. Multi-language Support
       - Detect language from audio
       - Translate text before TTS
       - Support for 50+ languages
    
    2. Emotion Detection
       - Extract tone from voice
       - Adjust response accordingly
       - Generate matching voice
    
    3. Real-time Transcription
       - Stream audio while recording
       - Live caption generation
       - Immediate response trigger
    
    4. Document Intelligence
       - Extract key entities
       - Summarize documents
       - Generate Q&A
    
    5. Voice Biometrics
       - Speaker identification
       - Voice authentication
       - Unique voice signatures
    
    6. Custom Voice Profiles
       - Train on custom voice data
       - Clone voice characteristics
       - Maintain consistency
    
    7. Context-Aware Processing
       - Use previous files for context
       - Build knowledge from uploads
       - Improve accuracy over time
    
    8. Accessibility Features
       - Multi-format output
       - Adjustable speech speeds
       - Alternative descriptions
    """)
    
    print("\n✅ Advanced Features ready to use!")


def display_quick_reference():
    """Display quick reference guide"""
    print_section("📚 QUICK REFERENCE")
    
    print("""
    === IMAGE PROCESSING ===
    validate_image(path) → (bool, str)
    extract_image_metadata(path) → Dict
    resize_image(path, max_w, max_h) → bytes
    optimize_for_ai(path) → bytes
    
    === DOCUMENT PROCESSING ===
    extract_text_from_pdf(path) → (str, Dict)
    extract_text_from_docx(path) → (str, Dict)
    extract_text_from_txt(path) → (str, Dict)
    extract_csv_data(path) → (str, Dict)
    
    === AUDIO PROCESSING ===
    get_audio_duration(path) → float
    extract_audio_features(path) → Dict
    convert_audio_format(input, format) → bytes
    normalize_audio(path) → bytes
    
    === VIDEO PROCESSING ===
    get_video_info(path) → Dict
    extract_frames(path, num) → List[bytes]
    create_video_thumbnail(path, offset) → bytes
    
    === TEXT-TO-SPEECH ===
    TTSConfig(provider, voice, language, speed, pitch, profile)
    TextToSpeech(config).synthesize(text, format) → (bytes, Dict)
    
    === SPEECH-TO-TEXT ===
    STTConfig(provider, language, punctuation, filter)
    SpeechToText(config).transcribe(path) → (str, Dict)
    
    === VOICE SESSIONS ===
    VoiceSessionManager.create_session(id, user_id)
    VoiceSessionManager.add_voice_message(id, text, duration, is_user)
    VoiceSessionManager.get_session_stats(id) → Dict
    
    === REAL-TIME AUDIO ===
    RealTimeAudioProcessor.start_recording()
    RealTimeAudioProcessor.add_audio_chunk(chunk)
    RealTimeAudioProcessor.stop_recording() → bytes
    RealTimeAudioProcessor.get_audio_level(chunk) → float
    """)


def main():
    """Main demo entry point"""
    
    print("\n" + "="*60)
    print("  📎 ADVANCED MULTIMODAL & VOICE FEATURES")
    print("  Complete Interactive Demo")
    print("="*60)
    
    demos = [
        ("1", "Image Processing", demo_image_processing),
        ("2", "Document Processing", demo_document_processing),
        ("3", "Audio Processing", demo_audio_processing),
        ("4", "Video Processing", demo_video_processing),
        ("5", "Text-to-Speech", demo_text_to_speech),
        ("6", "Speech-to-Text", demo_speech_to_text),
        ("7", "Voice Sessions", demo_voice_sessions),
        ("8", "Voice Preferences", demo_voice_preferences),
        ("9", "Real-Time Audio", demo_real_time_audio),
        ("10", "Multimodal Manager", demo_multimodal_manager),
        ("11", "Streamlit Integration", demo_integration_with_streamlit),
        ("12", "Batch Processing", demo_batch_processing),
        ("13", "Error Handling", demo_error_handling),
        ("14", "Performance Tips", demo_performance_tips),
        ("15", "Advanced Features", demo_advanced_features),
        ("16", "Quick Reference", display_quick_reference),
        ("0", "Exit", None),
    ]
    
    while True:
        print("\n" + "-"*60)
        print("SELECT A DEMO:")
        print("-"*60)
        
        for key, name, _ in demos:
            if key != "0":
                print(f"{key}. {name}")
            else:
                print(f"\n{key}. Exit Demo")
        
        choice = input("\nEnter choice (0-16): ").strip()
        
        for key, name, func in demos:
            if choice == key:
                if func is None:
                    print("\n👋 Thanks for exploring! Good luck with your implementation!")
                    return
                func()
                input("\nPress Enter to continue...")
                break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
