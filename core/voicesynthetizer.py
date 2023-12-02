import logging
from core.pushtotalk import PushToTalk

class VoiceSynthetizer(logging.Handler):
    def __init__(self, synthesizer="espeak", language="spanish"):
        self.synthesizer = synthesizer
        self.language = language
        self.language_argument = self._set_language_argument()
        self.text_to_speech_argument = self._set_text_to_speech_argument()

    def set_synthesizer(self, synthesizer):
        self.synthesizer = synthesizer

    def set_language(self, language):
        self.language = language
        self.language_argument = self._set_language_argument()
        self.text_to_speech_argument = self._set_text_to_speech_argument()

    def _set_language_argument(self):
        if self.synthesizer == "festival":
            return "--language " + self.language
        elif self.synthesizer == "espeak":
            return "-v en" if self.language == "english" else "-v es-la"
        elif self.synthesizer == "google":
            return "en" if self.language == "english" else "es"

    def _set_text_to_speech_argument(self):
        if self.synthesizer == "festival":
            return "--tts"
        elif self.synthesizer == "espeak":
            return "--stdout"

    def speech_it(self, text):
        logging.info(text)
        text = "\"" + text + "\""
        pushtotalk = PushToTalk()

        if self.synthesizer == "festival":
            command = f'echo {text} | {self.synthesizer} {self.text_to_speech_argument} {self.language_argument}'
        elif self.synthesizer == "espeak":
            command = f'{self.synthesizer} {self.language_argument} {self.text_to_speech_argument} {text} | aplay'
        elif self.synthesizer == "google":
            command = f'core/google.sh {self.language} {text}'
            # Or use: command = f'core/voicerss.sh {self.language} {text}'

        pushtotalk.message(command)
