"""
VoiceSynthesizer - Text-to-Speech Engine with Multiple Backend Support

Supports OpenAI TTS, Google TTS, eSpeak, and Festival.
Provides robust error handling and graceful fallback mechanisms.
"""

import configparser
import logging
import subprocess
from typing import Optional
from openai import OpenAI
from core.pushtotalk import PushToTalk


class VoiceSynthesizer(logging.Handler):
    """
    Voice synthesizer with multiple TTS backend support.
    
    Supported synthesizers:
    - openai: OpenAI TTS API (high quality)
    - google: Google TTS API
    - espeak: eSpeak (offline, fast)
    - festival: Festival (offline, natural)
    
    Supports graceful degradation if primary synthesizer fails.
    """
    
    def __init__(self, synthesizer="openai", language="spanish"):
        """
        Initialize voice synthesizer.
        
        Args:
            synthesizer: TTS backend to use (openai, google, espeak, festival)
            language: Language for synthesis (spanish, english)
        """
        self.synthesizer = synthesizer
        self.language = language
        self.language_argument = self._set_language_argument(language)
        self.text_to_speech_argument = self._set_text_to_speech_argument()

        # Fallback synthesizers in order of preference
        self.fallback_order = ['espeak-ng', 'festival']

        self._warmup_audio()

        logging.info(
            f'VoiceSynthesizer initialized: {synthesizer} ({language})'
        )

    def set_synthesizer(self, synthesizer: str):
        """Change the TTS synthesizer."""
        self.synthesizer = synthesizer
        logging.info(f'VoiceSynthesizer changed to: {synthesizer}')

    def set_language(self, language: str):
        """
        Change the synthesis language.
        
        Args:
            language: Language to use (spanish, english)
        """
        self.language = language
        self.language_argument = self._set_language_argument(language)
        self.text_to_speech_argument = self._set_text_to_speech_argument()
        logging.info(f'VoiceSynthesizer language changed to: {language}')

    def _set_language_argument(self, language: str) -> str:
        """
        Get language-specific argument for synthesizer.
        
        Args:
            language: Target language
            
        Returns:
            Language argument string for the synthesizer
        """
        if self.synthesizer == "festival":
            return "--language " + self.language
        elif self.synthesizer == "espeak-ng":
            return "-v en" if language == "english" else "-v es-la"
        elif self.synthesizer == "google":
            return "en" if language == "english" else "es"
        return ""

    def _set_text_to_speech_argument(self) -> str:
        """
        Get TTS-specific argument for synthesizer.
        
        Returns:
            TTS argument string
        """
        if self.synthesizer == "festival":
            return "--tts"
        return ""

    def _warmup_audio(self):
        """Play a silent sound to wake up the audio interface (e.g. USB-C DAC)."""
        if self.synthesizer == 'espeak-ng':
            lang = self.language_argument.split()
            subprocess.run(
                ['espeak-ng'] + lang + ['-a', '0', ' '],
                capture_output=True,
                timeout=5
            )
        else:
            import wave, struct
            silence_path = "/tmp/nuupxe_warmup.wav"
            sample_rate = 24000
            duration_secs = 1
            with wave.open(silence_path, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(struct.pack('<h', 0) * sample_rate * (duration_secs + 1))
            subprocess.run(['aplay', silence_path], capture_output=True, timeout=5)

    def _load_openai_config(self) -> Optional[dict]:
        """
        Load OpenAI configuration from services.config.
        
        Returns:
            Configuration dictionary or None on error
        """
        try:
            services = configparser.ConfigParser()
            path = "configuration/services.config"
            services.read(path)
            
            config = {
                'api_key': services.get("openai", "api_key"),
                'model': services.get("openai", "model_tts", fallback="tts-1"),
                'voice': services.get("openai", "voice_tts", fallback="nova"),
            }
            return config
            
        except Exception as e:
            logging.error(f'Error loading OpenAI config: {e}')
            return None

    def convert_to_audio(self, text: str, output_speech_file: str) -> bool:
        """
        Convert text to audio file using OpenAI TTS.

        Args:
            text: Text to synthesize
            output_speech_file: Path to output audio file

        Returns:
            True on success, False on error
        """
        try:
            config = self._load_openai_config()
            if not config:
                logging.error('OpenAI config not available')
                return False

            client = OpenAI(api_key=config['api_key'])
            response = client.audio.speech.create(
                model=config['model'],
                voice=config['voice'],
                input=text,
                response_format="wav",
            )
            response.stream_to_file(output_speech_file)
            logging.info(f'Audio generated: {output_speech_file}')
            return True

        except Exception as e:
            logging.error(f'OpenAI TTS error: {e}')
            return False

    def _execute_command(self, command: str) -> bool:
        """
        Execute shell command for TTS synthesis.
        
        Args:
            command: Shell command to execute
            
        Returns:
            True on success, False on error
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logging.error(f'Command failed: {result.stderr}')
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            logging.error('TTS command timed out')
            return False
        except Exception as e:
            logging.error(f'Command execution error: {e}')
            return False

    def _try_fallback(self, text: str) -> bool:
        """
        Try fallback synthesizers if primary fails.
        
        Args:
            text: Text to synthesize
            
        Returns:
            True if any fallback succeeded, False otherwise
        """
        for fallback in self.fallback_order:
            logging.info(f'Trying fallback synthesizer: {fallback}')
            original = self.synthesizer
            self.synthesizer = fallback
            
            success = self._synthesize_with_current(text)
            
            self.synthesizer = original
            
            if success:
                return True
        
        return False

    def _synthesize_with_current(self, text: str, raw_text: str = None) -> bool:
        """
        Synthesize with current synthesizer settings.

        Args:
            text: Shell-quoted text for command-based synthesizers
            raw_text: Unquoted text for API-based synthesizers (defaults to text)

        Returns:
            True on success, False on error
        """
        pushtotalk = PushToTalk()

        if self.synthesizer == "openai":
            output_speech_file = "/tmp/audio.wav"
            if self.convert_to_audio(raw_text or text, output_speech_file):
                pushtotalk.message("audio", output_speech_file)
                return True
            return False
            
        elif self.synthesizer == "festival":
            command = f'echo {text} | {self.synthesizer} {self.text_to_speech_argument} {self.language_argument}'
            if self._execute_command(command):
                pushtotalk.message("text", "")
                return True
            return False
            
        elif self.synthesizer == "espeak-ng":
            command = f'espeak-ng {self.language_argument} {text}'
            if self._execute_command(command):
                pushtotalk.message("text", "")
                return True
            return False
            
        elif self.synthesizer == "google":
            command = f'core/google.sh {self.language} {text}'
            if self._execute_command(command):
                pushtotalk.message("text", "")
                return True
            return False
        
        return False

    def speech_it(self, text: str):
        """
        Synthesize and play text with automatic fallback on failure.
        
        Args:
            text: Text to synthesize and speak
        """
        if not text or not text.strip():
            logging.warning('Empty text provided to speech_it')
            return
        
        # Log the text
        logging.info(f'Speaking: {text}')
        
        # Quote text for shell commands (espeak-ng, festival, google)
        quoted_text = "\"" + text + "\""

        # Try primary synthesizer
        success = self._synthesize_with_current(quoted_text, raw_text=text)

        # Try fallbacks if primary failed
        if not success:
            logging.warning(
                f'Primary synthesizer {self.synthesizer} failed, trying fallbacks'
            )
            success = self._try_fallback(quoted_text)
        
        # Log final result
        if not success:
            logging.error(
                f'All synthesizers failed for text: {text[:50]}...'
            )
        else:
            logging.info('Speech synthesis successful')

