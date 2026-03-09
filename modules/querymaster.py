#!/usr/bin/python
"""
QueryMaster - Enhanced AI Query Module with Context-Aware Conversations

This module provides intelligent Q&A capabilities using OpenAI's GPT models
with conversation history and ham radio domain expertise.
"""

import configparser
import json
import logging
from typing import List, Dict, Optional, Any

from openai import OpenAI

from core.alive import alive
from core.emailx import Emailx
from core.twitterc import TwitterC
from core.voicerecognition import VoiceRecognition


class QueryMaster:
    """
    Enhanced query master with context-aware conversations and ham radio expertise.
    
    Features:
    - Conversation history tracking
    - Ham radio specialized system prompt
    - Configurable models and parameters
    - Token usage tracking
    - Error handling and graceful degradation
    """

    # Ham radio specialized system prompt
    SYSTEM_PROMPT = """You are a helpful AI assistant specialized in amateur radio (ham radio).
You provide clear, concise, and accurate information about:
- Amateur radio operations, regulations, and licensing
- Radio equipment, antennas, and propagation
- Q-codes, phonetics, and operating procedures
- Emergency communications and public service
- Technical topics like modulation, frequencies, and bands
- General questions from ham radio operators

Keep your responses brief and suitable for text-to-speech output.
Typical response length should be 2-3 sentences, maximum 150 words.
Be friendly and use amateur radio terminology appropriately.
Always sign off with "73" (best regards in ham radio)."""

    def __init__(self, voicesynthesizer):
        """
        Initialize QueryMaster with voice synthesizer.
        
        Args:
            voicesynthesizer: Voice synthesizer instance for TTS output
        """
        self.modulename = 'QueryMaster'
        self.voicesynthesizer = voicesynthesizer
        self.emailx = Emailx()
        self.twitterc = TwitterC('twython')
        self.voicerecognition = VoiceRecognition(self.voicesynthesizer)
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10  # Keep last 10 exchanges
        
        # Configuration
        self.config = self._load_config()
        self.client = OpenAI(api_key=self.config['api_key'])
        
        # Statistics
        self.total_queries = 0
        self.total_tokens_used = 0
        
        self.setup()

    def __del__(self):
        """Cleanup on deletion."""
        if self.total_queries > 0:
            logging.info(
                f'QueryMaster Stats: {self.total_queries} queries, '
                f'{self.total_tokens_used} tokens used'
            )

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from services.config file.
        
        Returns:
            Dictionary with configuration parameters
        """
        services = configparser.ConfigParser()
        path = "configuration/services.config"
        services.read(path)
        
        try:
            config = {
                'api_key': services.get("openai", "api_key"),
                'model_chat': services.get("openai", "model_chat", 
                                          fallback="gpt-4-turbo-preview"),
                'max_tokens': services.getint("openai", "max_tokens", 
                                             fallback=150),
                'temperature': services.getfloat("openai", "temperature", 
                                                fallback=0.7),
            }
            logging.info(f'QueryMaster config loaded: model={config["model_chat"]}')
            return config
        except Exception as e:
            logging.error(f'Error loading QueryMaster config: {e}')
            # Return defaults
            return {
                'api_key': services.get("openai", "api_key"),
                'model_chat': 'gpt-3.5-turbo',
                'max_tokens': 150,
                'temperature': 0.7,
            }

    def setup(self):
        """Setup voice recognition and synthesizer."""
        logging.info('QueryMaster Setup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthesizer._set_language_argument("spanish")

    def cleanup(self):
        """Cleanup voice recognition and synthesizer."""
        logging.info('QueryMaster Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthesizer._set_language_argument("spanish")

    def query(self, message: str) -> Optional[str]:
        """
        Query GPT without context (legacy single-turn method).
        
        Args:
            message: User's question
            
        Returns:
            AI response as string, or None on error
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": message}
                ],
                model=self.config['model_chat'],
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature'],
            )
            
            # Track usage
            self.total_queries += 1
            if hasattr(response, 'usage'):
                self.total_tokens_used += response.usage.total_tokens
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f'QueryMaster query error: {e}')
            return None

    def query_with_context(self, message: str) -> Optional[str]:
        """
        Query GPT with conversation history for context-aware responses.
        
        Args:
            message: User's question
            
        Returns:
            AI response as string, or None on error
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Build message list with system prompt and history
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT}
            ] + self.conversation_history[-self.max_history:]
            
            # Query OpenAI
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.config['model_chat'],
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature'],
            )
            
            # Extract answer
            answer = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            # Track usage
            self.total_queries += 1
            if hasattr(response, 'usage'):
                self.total_tokens_used += response.usage.total_tokens
                logging.info(
                    f'QueryMaster: {response.usage.total_tokens} tokens used '
                    f'(history: {len(self.conversation_history)} messages)'
                )
            
            return answer
            
        except Exception as e:
            logging.error(f'QueryMaster query_with_context error: {e}')
            return None

    def clear_context(self):
        """Clear conversation history."""
        self.conversation_history = []
        logging.info('QueryMaster: Conversation history cleared')

    def get_context_summary(self) -> str:
        """
        Get summary of current conversation context.
        
        Returns:
            Human-readable summary string
        """
        msg_count = len(self.conversation_history)
        if msg_count == 0:
            return "No conversation history"
        
        user_msgs = len([m for m in self.conversation_history if m['role'] == 'user'])
        return f"{msg_count} messages ({user_msgs} from user)"

    def listen(self):
        """
        Listen for voice input and provide AI response with context.
        
        This is the main interactive method that:
        1. Announces readiness
        2. Records audio question
        3. Recognizes speech
        4. Queries AI with context
        5. Speaks the answer
        """
        logging.info('QueryMaster Listen (with context)')
        
        try:
            # Announce
            self.voicesynthesizer.speech_it('Hola! Cual es tu pregunta?')
            
            # Record and recognize
            self.voicerecognition.record()
            question = self.voicerecognition.recognize('False')
            
            if not question:
                self.voicesynthesizer.speech_it('No pude escuchar tu pregunta. Intenta de nuevo.')
                return
            
            logging.info(f'QueryMaster question: {question}')
            
            # Query with context
            answer = self.query_with_context(question)
            
            if answer:
                logging.info(f'QueryMaster answer: {answer}')
                self.voicesynthesizer.speech_it(answer)
            else:
                self.voicesynthesizer.speech_it(
                    'Lo siento, tuve un problema al procesar tu pregunta. '
                    'Intenta de nuevo mas tarde.'
                )
                
        except Exception as e:
            logging.error(f'QueryMaster listen error: {e}')
            self.voicesynthesizer.speech_it(
                'Error inesperado. Por favor intenta de nuevo.'
            )

    def interactive_session(self):
        """
        Run an interactive session with multiple questions.
        
        Continues until user says 'adios', 'salir', or 'terminar'.
        """
        logging.info('QueryMaster: Starting interactive session')
        self.clear_context()
        
        self.voicesynthesizer.speech_it(
            'Hola! Soy tu asistente de radio aficionado. '
            'Puedes hacerme varias preguntas. '
            'Di "adios" cuando termines.'
        )
        
        while True:
            try:
                # Record question
                self.voicerecognition.record()
                question = self.voicerecognition.recognize('False')
                
                if not question:
                    continue
                
                # Check for exit commands
                question_lower = question.lower()
                if any(word in question_lower for word in ['adios', 'salir', 'terminar', 'hasta luego']):
                    self.voicesynthesizer.speech_it('Hasta pronto! 73!')
                    break
                
                # Query and respond
                answer = self.query_with_context(question)
                if answer:
                    self.voicesynthesizer.speech_it(answer)
                else:
                    self.voicesynthesizer.speech_it('Lo siento, no pude procesar esa pregunta.')
                    
            except KeyboardInterrupt:
                logging.info('QueryMaster: Interactive session interrupted')
                self.voicesynthesizer.speech_it('Sesion terminada. 73!')
                break
            except Exception as e:
                logging.error(f'QueryMaster interactive session error: {e}')
                continue


# End of File
