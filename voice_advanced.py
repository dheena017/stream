"""
Advanced Voice & Speech Processing Module
Handles text-to-speech, speech-to-text, voice profiles, and real-time processing
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import io
from datetime import datetime


class VoiceGender(Enum):
    """Voice gender options"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class SpeechRate(Enum):
    """Speech rate options"""
    SLOW = 0.7
    NORMAL = 1.0
    FAST = 1.3


class VoiceProfile(Enum):
    """Predefined voice profiles"""
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    CALM = "calm"
    ENERGETIC = "energetic"
    ROBOTIC = "robotic"
    NATURAL = "natural"


@dataclass
class TTSConfig:
    """Text-to-Speech configuration"""
    provider: str  # "google", "elevenlabs", "azure", "local"
    voice_name: str
    language: str = "en-US"
    speed: float = 1.0
    pitch: float = 1.0
    volume_gain: float = 1.0
    profile: VoiceProfile = VoiceProfile.NATURAL
    use_ssml: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "provider": self.provider,
            "voice_name": self.voice_name,
            "language": self.language,
            "speed": self.speed,
            "pitch": self.pitch,
            "volume_gain": self.volume_gain,
            "profile": self.profile.value,
            "use_ssml": self.use_ssml,
        }


@dataclass
class STTConfig:
    """Speech-to-Text configuration"""
    provider: str  # "google", "azure", "openai", "local"
    language: str = "en-US"
    enable_punctuation: bool = True
    enable_profanity_filter: bool = True
    use_context_hints: bool = True
    context_hints: List[str] = None
    
    def __post_init__(self):
        if self.context_hints is None:
            self.context_hints = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "provider": self.provider,
            "language": self.language,
            "enable_punctuation": self.enable_punctuation,
            "enable_profanity_filter": self.enable_profanity_filter,
            "use_context_hints": self.use_context_hints,
            "context_hints": self.context_hints,
        }


@dataclass
class VoicePreference:
    """User voice preferences"""
    preferred_language: str = "en-US"
    preferred_voice: str = "default"
    preferred_gender: VoiceGender = VoiceGender.NEUTRAL
    speech_rate: SpeechRate = SpeechRate.NORMAL
    auto_speak_responses: bool = True
    voice_profile: VoiceProfile = VoiceProfile.NATURAL
    accent: str = "standard"  # "standard", "british", "indian", "australian"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "preferred_language": self.preferred_language,
            "preferred_voice": self.preferred_voice,
            "preferred_gender": self.preferred_gender.value,
            "speech_rate": self.speech_rate.value,
            "auto_speak_responses": self.auto_speak_responses,
            "voice_profile": self.voice_profile.value,
            "accent": self.accent,
        }


class TextToSpeech:
    """Advanced text-to-speech processing"""
    
    # Supported providers and their voices
    PROVIDER_VOICES = {
        "google": ["en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-E", "en-US-Neural2-F"],
        "elevenlabs": ["bella", "james", "charlotte", "elias", "lily", "josh"],
        "azure": ["en-US-AriaNeural", "en-US-GuyNeural", "en-US-JennyNeural"],
        "openai": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
    }
    
    def __init__(self, config: TTSConfig):
        self.config = config
        self.speech_history: List[Dict] = []
    
    def synthesize(self, text: str, output_format: str = "mp3") -> Tuple[bytes, Dict]:
        """Synthesize speech from text"""
        
        # Apply SSML if enabled
        if self.config.use_ssml:
            text = self._apply_ssml(text)
        
        # Provider-specific synthesis
        if self.config.provider == "google":
            audio, metadata = self._synthesize_google(text, output_format)
        elif self.config.provider == "elevenlabs":
            audio, metadata = self._synthesize_elevenlabs(text, output_format)
        elif self.config.provider == "azure":
            audio, metadata = self._synthesize_azure(text, output_format)
        elif self.config.provider == "openai":
            audio, metadata = self._synthesize_openai(text, output_format)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
        
        # Log to history
        self.speech_history.append({
            "text": text[:100] + "..." if len(text) > 100 else text,
            "provider": self.config.provider,
            "voice": self.config.voice_name,
            "timestamp": datetime.now().isoformat(),
            "output_format": output_format,
        })
        
        return audio, metadata
    
    def _apply_ssml(self, text: str) -> str:
        """Apply SSML formatting"""
        ssml = f"""
        <speak>
            <prosody rate="{self.config.speed}" pitch="{self.config.pitch * 100}%">
                {text}
            </prosody>
        </speak>
        """
        return ssml.strip()
    
    def _synthesize_google(self, text: str, output_format: str) -> Tuple[bytes, Dict]:
        """Synthesize using Google Cloud TTS"""
        try:
            from google.cloud import texttospeech
            
            client = texttospeech.TextToSpeechClient()
            
            input_text = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.config.language,
                name=self.config.voice_name,
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )
            
            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config,
            )
            
            metadata = {
                "provider": "google",
                "language": self.config.language,
                "voice": self.config.voice_name,
                "bytes_length": len(response.audio_content),
            }
            
            return response.audio_content, metadata
        except ImportError:
            raise Exception("google-cloud-texttospeech required")
    
    def _synthesize_elevenlabs(self, text: str, output_format: str) -> Tuple[bytes, Dict]:
        """Synthesize using ElevenLabs"""
        try:
            import requests
            
            api_key = os.environ.get("ELEVENLABS_API_KEY")
            if not api_key:
                raise Exception("ELEVENLABS_API_KEY not set")
            
            voice_id = self._get_elevenlabs_voice_id(self.config.voice_name)
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json",
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            metadata = {
                "provider": "elevenlabs",
                "voice": self.config.voice_name,
                "bytes_length": len(response.content),
            }
            
            return response.content, metadata
        except ImportError:
            raise Exception("requests required")
    
    def _synthesize_azure(self, text: str, output_format: str) -> Tuple[bytes, Dict]:
        """Synthesize using Azure Speech"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=os.environ.get("AZURE_SPEECH_KEY"),
                region=os.environ.get("AZURE_SPEECH_REGION", "eastus")
            )
            speech_config.speech_synthesis_voice_name = self.config.voice_name
            
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            metadata = {
                "provider": "azure",
                "voice": self.config.voice_name,
                "reason": str(result.reason),
            }
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return result.audio_data, metadata
            else:
                raise Exception(f"Azure synthesis failed: {result.reason}")
        except ImportError:
            raise Exception("azure-cognitiveservices-speech required")
    
    def _synthesize_openai(self, text: str, output_format: str) -> Tuple[bytes, Dict]:
        """Synthesize using OpenAI TTS"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice=self.config.voice_name,
                input=text,
            )
            
            metadata = {
                "provider": "openai",
                "model": "tts-1-hd",
                "voice": self.config.voice_name,
                "bytes_length": len(response.content),
            }
            
            return response.content, metadata
        except ImportError:
            raise Exception("openai required")
    
    def _get_elevenlabs_voice_id(self, voice_name: str) -> str:
        """Map voice name to ElevenLabs voice ID"""
        voice_mapping = {
            "bella": "EXAVITQu4vr4xnSDxMaL",
            "james": "pNInz6obpgDQGcFmaJgB",
            "charlotte": "xrX3nzkatUQ5sLU4OToM",
        }
        return voice_mapping.get(voice_name, voice_name)
    
    def get_available_voices(self) -> List[str]:
        """Get available voices for current provider"""
        return self.PROVIDER_VOICES.get(self.config.provider, [])


class SpeechToText:
    """Advanced speech-to-text processing"""
    
    def __init__(self, config: STTConfig):
        self.config = config
        self.transcription_history: List[Dict] = []
    
    def transcribe(self, audio_file: str) -> Tuple[str, Dict]:
        """Transcribe audio file to text"""
        
        # Provider-specific transcription
        if self.config.provider == "google":
            text, metadata = self._transcribe_google(audio_file)
        elif self.config.provider == "azure":
            text, metadata = self._transcribe_azure(audio_file)
        elif self.config.provider == "openai":
            text, metadata = self._transcribe_openai(audio_file)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
        
        # Apply filters
        if self.config.enable_profanity_filter:
            text = self._apply_profanity_filter(text)
        
        if self.config.enable_punctuation:
            text = self._add_punctuation(text)
        
        # Log to history
        self.transcription_history.append({
            "provider": self.config.provider,
            "timestamp": datetime.now().isoformat(),
            "text_length": len(text),
            "language": self.config.language,
        })
        
        return text, metadata
    
    def _transcribe_google(self, audio_file: str) -> Tuple[str, Dict]:
        """Transcribe using Google Cloud Speech"""
        try:
            from google.cloud import speech_v1
            
            client = speech_v1.SpeechClient()
            
            with open(audio_file, "rb") as audio_file_obj:
                content = audio_file_obj.read()
            
            audio = speech_v1.RecognitionAudio(content=content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
                language_code=self.config.language,
                enable_automatic_punctuation=self.config.enable_punctuation,
                model="default",
                use_enhanced=True,
            )
            
            response = client.recognize(config=config, audio=audio)
            
            text = ""
            for result in response.results:
                text += result.alternatives[0].transcript
            
            metadata = {
                "provider": "google",
                "language": self.config.language,
                "confidence": response.results[0].alternatives[0].confidence if response.results else 0,
            }
            
            return text, metadata
        except ImportError:
            raise Exception("google-cloud-speech required")
    
    def _transcribe_azure(self, audio_file: str) -> Tuple[str, Dict]:
        """Transcribe using Azure Speech"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=os.environ.get("AZURE_SPEECH_KEY"),
                region=os.environ.get("AZURE_SPEECH_REGION", "eastus")
            )
            speech_config.speech_recognition_language = self.config.language
            
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = recognizer.recognize_once_async().get()
            
            text = result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else ""
            
            metadata = {
                "provider": "azure",
                "language": self.config.language,
                "reason": str(result.reason),
            }
            
            return text, metadata
        except ImportError:
            raise Exception("azure-cognitiveservices-speech required")
    
    def _transcribe_openai(self, audio_file: str) -> Tuple[str, Dict]:
        """Transcribe using OpenAI Whisper"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            with open(audio_file, "rb") as audio_file_obj:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file_obj,
                    language=self.config.language[:2],  # Use language code
                )
            
            metadata = {
                "provider": "openai",
                "model": "whisper-1",
                "language": self.config.language,
            }
            
            return transcript.text, metadata
        except ImportError:
            raise Exception("openai required")
    
    def _apply_profanity_filter(self, text: str) -> str:
        """Apply profanity filter"""
        try:
            from better_profanity import profanity
            
            if not profanity.is_profane(text):
                return text
            
            return profanity.contains_profanity(text)
        except ImportError:
            return text
    
    def _add_punctuation(self, text: str) -> str:
        """Add punctuation to text"""
        try:
            from punctuator import Punctuator
            
            punctuator = Punctuator()
            return punctuator.punctuate(text)
        except ImportError:
            # Simple fallback
            return text.capitalize() + "." if text else text


class VoiceSessionManager:
    """Manages voice interactions and sessions"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}
        self.user_preferences: Dict[str, VoicePreference] = {}
        self.session_history: List[Dict] = []
    
    def create_session(self, session_id: str, user_id: str, preferences: Optional[VoicePreference] = None):
        """Create a new voice session"""
        if preferences is None:
            preferences = self.user_preferences.get(user_id, VoicePreference())
        
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "preferences": preferences,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "total_duration": 0.0,
        }
    
    def add_voice_message(self, session_id: str, message: str, duration: float, is_user: bool = True):
        """Add voice message to session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["messages"].append({
                "text": message,
                "duration": duration,
                "is_user": is_user,
                "timestamp": datetime.now().isoformat(),
            })
            self.active_sessions[session_id]["total_duration"] += duration
    
    def close_session(self, session_id: str):
        """Close a voice session"""
        if session_id in self.active_sessions:
            session_data = self.active_sessions.pop(session_id)
            self.session_history.append(session_data)
            return session_data
        return None
    
    def set_user_preference(self, user_id: str, preferences: VoicePreference):
        """Set user voice preferences"""
        self.user_preferences[user_id] = preferences
    
    def get_user_preference(self, user_id: str) -> VoicePreference:
        """Get user voice preferences"""
        return self.user_preferences.get(user_id, VoicePreference())
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a voice session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                "user_id": session["user_id"],
                "duration": session["total_duration"],
                "messages": len(session["messages"]),
                "user_messages": len([m for m in session["messages"] if m["is_user"]]),
                "assistant_messages": len([m for m in session["messages"] if not m["is_user"]]),
                "created_at": session["created_at"],
            }
        return {}


class RealTimeAudioProcessor:
    """Processes audio in real-time"""
    
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_buffer = []
        self.is_recording = False
    
    def start_recording(self):
        """Start recording audio"""
        self.audio_buffer = []
        self.is_recording = True
    
    def add_audio_chunk(self, chunk: bytes):
        """Add audio chunk to buffer"""
        if self.is_recording:
            self.audio_buffer.append(chunk)
    
    def stop_recording(self) -> bytes:
        """Stop recording and return audio data"""
        self.is_recording = False
        return b"".join(self.audio_buffer)
    
    def get_audio_level(self, chunk: bytes) -> float:
        """Get audio level (0-1) for current chunk"""
        try:
            import numpy as np
            audio_data = np.frombuffer(chunk, dtype=np.int16)
            rms = np.sqrt(np.mean(audio_data**2))
            level = min(rms / 32768.0, 1.0)
            return level
        except ImportError:
            return 0.5
    
    def detect_silence(self, chunk: bytes, threshold: float = 0.02) -> bool:
        """Detect if chunk contains silence"""
        return self.get_audio_level(chunk) < threshold


import os


# Export
__all__ = [
    "VoiceGender",
    "SpeechRate",
    "VoiceProfile",
    "TTSConfig",
    "STTConfig",
    "VoicePreference",
    "TextToSpeech",
    "SpeechToText",
    "VoiceSessionManager",
    "RealTimeAudioProcessor",
]
