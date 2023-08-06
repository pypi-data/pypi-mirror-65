#!/usr/bin/python3
# =============================================================================
#
#   Voxidiomatix | Speech-to-Speech Multilangual Vocal Translator
#
#   Copyright (c) Clement HUBER
#
#   MIT License
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to
#   deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#   sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
#   For more information, please refer to [https://opensource.org/licenses/MIT]
#
# =============================================================================

# IMPORTS =====================================================================

import numpy as np
import pydeepl
from speech import Speech
from abstract_translator import AbstractTranslator


# CLASS =======================================================================


class CascadeTranslator(AbstractTranslator):
    """
    This class implements a cascaded speech-to-speech translator.

    The translation is broken down into three steps:
    -   Automatic Speech Recognition (ASR)
    -   Text-to-Text Machine Translation (TTMT)
    -   Text-to-Speech Synthesis (TTS)
    """

    def __init__(self):
        """
        This function initializes a CascadeTranslator object
        """
        super(CascadeTranslator, self).__init__()

    def translate(self, speech: Speech, to_language: str):
        translation = Speech()
        speech.transcript = self.transcriptVocalSpeech(speech.audio)
        translation.transcript = self.textToTextTranslate(
            speech.transcript, speech.language, to_language
        )
        translation.audio = self.synthesizeVocalSpeech(translation.transcript)

        return translation

    @staticmethod
    def transcriptVocalSpeech(audio: np.ndarray):
        """
        This function performs an automatic speech recognition.

        Arguments
        ---------
            audio : np.ndarray
                Vocal speech

        Returns
        -------
            string -- The transcripted speech
        """
        transcript = None
        return transcript

    @staticmethod
    def textToTextTranslate(
        transcript: str, from_language: str, to_language: str
    ):
        """
        This function performs the tex-to-text machine translation.

        Arguments
        ---------
            transcript : string
                Speech transcription to translate
            from_language : string
                Language of the transcript to translate
            to_language : string
                Language into which the transcript has to be translated

        Returns
        -------
            string -- The translated transcript
        """
        translation = pydeepl.translate(
            transcript, to_language, from_lang=from_language
        )
        return translation

    @staticmethod
    def synthesizeVocalSpeech(transcript: str):
        """
        This function performs the text-to-speech synthesis.

        Arguments
        ---------
            transcript : string
                Transcript of the speech

        Returns
        -------
            np.ndarray -- The vocal speech
        """
        audio = None
        return audio
