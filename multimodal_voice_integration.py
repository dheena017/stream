"""
Multimodal & Voice Features Integration
Seamless integration of advanced multimodal and voice capabilities into Streamlit app
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from multimodal_advanced import MultimodalManager
from voice_advanced import (
    SpeechToText,
    STTConfig,
    TextToSpeech,
    TTSConfig,
    VoiceGender,
    VoicePreference,
    VoiceProfile,
    VoiceSessionManager,
)


class MultimodalVoiceIntegrator:
    """Central integrator for multimodal and voice features"""
    
    def __init__(self):
        self.multimodal_manager = MultimodalManager()
        self.voice_session_manager = VoiceSessionManager()
        self.upload_history: List[Dict] = []
        self.processing_stats = {
            "total_uploads": 0,
            "total_voice_sessions": 0,
            "file_types_processed": {},
            "voice_sessions_duration": 0.0,
        }
    
    def create_multimodal_uploader(self) -> Optional[Dict]:
        """Create multimodal file uploader in Streamlit"""
        st.subheader("📁 Advanced Multimodal Uploader")
        
        with st.expander("Upload Files", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Supported Formats:**")
                st.write("🖼️ Images: PNG, JPEG, GIF, WebP, BMP")
                st.write("📄 Documents: PDF, DOCX, TXT, MD, CSV, JSON")
                st.write("🔊 Audio: MP3, WAV, M4A, OGG, FLAC")
                st.write("🎬 Video: MP4, AVI, MOV, MKV, WebM")
            
            with col2:
                upload_type = st.radio(
                    "Choose Upload Type",
                    ["All Files", "Images", "Documents", "Audio", "Video"]
                )
            
            # File type filters
            accept_mapping = {
                "All Files": None,
                "Images": ["image/png", "image/jpeg", "image/gif", "image/webp"],
                "Documents": ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "text/csv"],
                "Audio": ["audio/mpeg", "audio/wav", "audio/m4a", "audio/ogg", "audio/flac"],
                "Video": ["video/mp4", "video/x-msvideo", "video/quicktime", "video/x-matroska", "video/webm"],
            }
            
            uploaded_files = st.file_uploader(
                "Drag and drop files here",
                accept_multiple_files=True,
                type=accept_mapping.get(upload_type)
            )
            
            if uploaded_files:
                return self._process_uploads(uploaded_files)
        
        return None
    
    def _process_uploads(self, uploaded_files) -> Dict:
        """Process uploaded files"""
        results = {
            "files": [],
            "errors": [],
            "summary": {}
        }
        
        for uploaded_file in uploaded_files:
            try:
                # Save temporary file
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process file
                media_file = self.multimodal_manager.process_file(temp_path)
                
                results["files"].append({
                    "name": media_file.filename,
                    "type": media_file.media_type.value,
                    "size": f"{media_file.file_size / 1024:.2f} KB",
                    "metadata": media_file.metadata
                })
                
                # Update statistics
                self.processing_stats["total_uploads"] += 1
                file_type = media_file.media_type.value
                self.processing_stats["file_types_processed"][file_type] = \
                    self.processing_stats["file_types_processed"].get(file_type, 0) + 1
                
                # Cleanup temp file
                os.remove(temp_path)
                
            except Exception as e:
                results["errors"].append({
                    "file": uploaded_file.name,
                    "error": str(e)
                })
        
        # Display results
        self._display_upload_results(results)
        return results
    
    def _display_upload_results(self, results: Dict):
        """Display upload results in Streamlit"""
        if results["files"]:
            st.success(f"✅ Processed {len(results['files'])} file(s)")
            
            for file_info in results["files"]:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"📄 **{file_info['name']}**")
                    with col2:
                        st.write(f"Type: {file_info['type']}")
                    with col3:
                        st.write(f"Size: {file_info['size']}")
                    
                    if file_info['metadata']:
                        with st.expander("View Metadata"):
                            st.json(file_info['metadata'])
        
        if results["errors"]:
            st.error(f"❌ Failed to process {len(results['errors'])} file(s)")
            for error_info in results["errors"]:
                st.write(f"- **{error_info['file']}**: {error_info['error']}")
    
    def create_voice_settings(self) -> VoicePreference:
        """Create voice settings panel in Streamlit"""
        st.subheader("🎤 Voice Settings")
        
        with st.expander("Configure Voice", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox(
                    "Language",
                    ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN"]
                )
                
                gender = st.radio(
                    "Voice Gender",
                    [g.value for g in VoiceGender]
                )
                
                profile = st.selectbox(
                    "Voice Profile",
                    [p.value for p in VoiceProfile]
                )
            
            with col2:
                speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
                
                accent = st.selectbox(
                    "Accent",
                    ["standard", "british", "indian", "australian"]
                )
                
                auto_speak = st.checkbox("Auto-speak responses", True)
            
            preferences = VoicePreference(
                preferred_language=language,
                preferred_gender=VoiceGender(gender),
                voice_profile=VoiceProfile(profile),
                speech_rate=speed,
                auto_speak_responses=auto_speak,
                accent=accent,
            )
            
            return preferences
        
        return VoicePreference()
    
    def create_text_to_speech_interface(self, preferences: VoicePreference) -> Optional[bytes]:
        """Create text-to-speech interface"""
        st.subheader("🔊 Text-to-Speech")
        
        with st.expander("Convert Text to Speech", expanded=False):
            # Text input
            text_input = st.text_area(
                "Enter text to synthesize",
                height=150,
                placeholder="Type or paste text here..."
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                provider = st.selectbox(
                    "TTS Provider",
                    ["google", "elevenlabs", "azure", "openai"]
                )
            
            with col2:
                format_type = st.selectbox(
                    "Output Format",
                    ["mp3", "wav", "ogg"]
                )
            
            with col3:
                if st.button("🎵 Generate Speech", key="tts_generate"):
                    try:
                        config = TTSConfig(
                            provider=provider,
                            voice_name=f"{preferences.preferred_gender.value}_voice",
                            language=preferences.preferred_language,
                            speed=preferences.speech_rate,
                            profile=preferences.voice_profile,
                        )
                        
                        tts = TextToSpeech(config)
                        audio_bytes, metadata = tts.synthesize(text_input, output_format=format_type)
                        
                        st.success("✅ Speech generated successfully!")
                        st.audio(audio_bytes, format=f"audio/{format_type}")
                        
                        # Download button
                        st.download_button(
                            "⬇️ Download Audio",
                            data=audio_bytes,
                            file_name=f"speech.{format_type}",
                            mime=f"audio/{format_type}"
                        )
                        
                        return audio_bytes
                    
                    except Exception as e:
                        st.error(f"❌ TTS Error: {str(e)}")
        
        return None
    
    def create_speech_to_text_interface(self, preferences: VoicePreference) -> Optional[str]:
        """Create speech-to-text interface"""
        st.subheader("🎙️ Speech-to-Text")
        
        with st.expander("Convert Speech to Text", expanded=False):
            audio_file = st.file_uploader(
                "Upload audio file",
                type=["mp3", "wav", "m4a", "ogg", "flac"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                provider = st.selectbox(
                    "STT Provider",
                    ["google", "azure", "openai"],
                    key="stt_provider"
                )
            
            with col2:
                if st.button("🎧 Transcribe Audio", key="stt_transcribe"):
                    if audio_file:
                        try:
                            # Save temporary file
                            temp_path = f"/tmp/{audio_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(audio_file.getbuffer())
                            
                            config = STTConfig(
                                provider=provider,
                                language=preferences.preferred_language,
                                enable_punctuation=True,
                            )
                            
                            stt = SpeechToText(config)
                            text, metadata = stt.transcribe(temp_path)
                            
                            st.success("✅ Transcription complete!")
                            st.text_area("Transcribed Text", value=text, height=150)
                            
                            # Copy button
                            if st.button("📋 Copy to Clipboard"):
                                st.write("*Copied to clipboard!*")
                            
                            # Cleanup
                            os.remove(temp_path)
                            
                            return text
                        
                        except Exception as e:
                            st.error(f"❌ STT Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please upload an audio file")
        
        return None
    
    def create_voice_session_panel(self) -> Optional[str]:
        """Create voice session control panel"""
        st.subheader("🎙️ Voice Session")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏹️ Start Session", key="voice_start"):
                session_id = f"session_{datetime.now().timestamp()}"
                self.voice_session_manager.create_session(session_id, "user_default")
                st.session_state.voice_session_id = session_id
                st.success(f"Session started: {session_id}")
        
        with col2:
            if st.button("⏸️ Pause Session", key="voice_pause"):
                st.info("Session paused")
        
        with col3:
            if st.button("⏹️ Stop Session", key="voice_stop"):
                if hasattr(st.session_state, 'voice_session_id'):
                    session_data = self.voice_session_manager.close_session(
                        st.session_state.voice_session_id
                    )
                    if session_data:
                        stats = self.voice_session_manager.get_session_stats(
                            st.session_state.voice_session_id
                        )
                        st.info(f"Session ended. Duration: {stats.get('duration', 0):.2f}s")
    
    def display_multimodal_statistics(self):
        """Display multimodal processing statistics"""
        st.subheader("📊 Processing Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Uploads", self.processing_stats["total_uploads"])
        
        with col2:
            st.metric("Voice Sessions", self.processing_stats["total_voice_sessions"])
        
        with col3:
            total_files = sum(self.processing_stats["file_types_processed"].values())
            st.metric("Files Processed", total_files)
        
        with col4:
            duration = self.processing_stats["voice_sessions_duration"]
            st.metric("Voice Duration", f"{duration:.1f}s")
        
        # File type breakdown
        if self.processing_stats["file_types_processed"]:
            st.write("**File Types Processed:**")
            for file_type, count in self.processing_stats["file_types_processed"].items():
                st.write(f"- {file_type.upper()}: {count} file(s)")
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get summary of all multimodal and voice features"""
        return {
            "multimodal_stats": self.multimodal_manager.get_processing_summary(),
            "processing_stats": self.processing_stats,
            "active_voice_sessions": len(self.voice_session_manager.active_sessions),
            "voice_preferences_saved": len(self.voice_session_manager.user_preferences),
        }


# Helper functions for Streamlit app integration

def add_multimodal_sidebar_section():
    """Add multimodal section to Streamlit sidebar"""
    with st.sidebar:
        st.write("---")
        st.subheader("📎 Multimodal & Voice")
        
        if st.checkbox("Enable Multimodal Features"):
            integrator = MultimodalVoiceIntegrator()
            
            feature = st.radio(
                "Select Feature",
                ["Multimodal Uploader", "Voice Settings", "Text-to-Speech", "Speech-to-Text"]
            )
            
            if feature == "Multimodal Uploader":
                integrator.create_multimodal_uploader()
            elif feature == "Voice Settings":
                integrator.create_voice_settings()
            elif feature == "Text-to-Speech":
                prefs = integrator.create_voice_settings()
                integrator.create_text_to_speech_interface(prefs)
            elif feature == "Speech-to-Text":
                prefs = integrator.create_voice_settings()
                integrator.create_speech_to_text_interface(prefs)


def create_multimodal_features_page():
    """Create full multimodal features page"""
    st.title("📎 Multimodal & Voice Features")
    
    integrator = MultimodalVoiceIntegrator()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Upload Files",
        "Voice Settings",
        "Text-to-Speech",
        "Speech-to-Text",
        "Statistics"
    ])
    
    with tab1:
        integrator.create_multimodal_uploader()
    
    with tab2:
        preferences = integrator.create_voice_settings()
    
    with tab3:
        integrator.create_text_to_speech_interface(preferences)
    
    with tab4:
        integrator.create_speech_to_text_interface(preferences)
    
    with tab5:
        integrator.display_multimodal_statistics()


__all__ = [
    "MultimodalVoiceIntegrator",
    "add_multimodal_sidebar_section",
    "create_multimodal_features_page",
]
