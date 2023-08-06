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

from scipy.io import wavfile
from scipy.signal import spectrogram
from file_handler import findAudioRecord, findTranscript


# CLASS =======================================================================


class Speech:
    """
    This class stores all relevant data related to a speech.

    Attributes
    ----------
        name : string
            Name of the speech
        path : string
            Path to the data
        language : string
            Language of the speech
        audio : numpy.ndarray
            Audio sample of the speech
        rate : int
            Sampling rate of the audio sample [sample/s]
        spectrogram : numpy.ndarray
            Spectrogram of the audio sample
        frequencies : numpy.ndarray
            Frequencies of the audio sample
        timestamps : numpy.ndarray
            Timestamps of the audio sample
        transcript : string
            Transcription of the speech
        voice :
            Tone of the speaker's voice, which is independent from the language
        prosody :
            Suprasegmentals and paralinguistic characteristics that are specific
            to the language
    """

    def __init__(
        self,
        name=None,
        path=None,
        language=None,
        audio=None,
        rate=None,
        spectrogram=None,
        frequencies=None,
        timestamps=None,
        transcript=None,
        voice=None,
        prosody=None,
    ):
        """
        This function initializes an Speech object
        """

        self.name = name
        self.path = path
        self.language = language
        self.audio = audio
        self.rate = rate
        self.spectrogram = spectrogram
        self.frequencies = frequencies
        self.timestamps = timestamps
        self.transcript = transcript
        self.voice = voice
        self.prosody = prosody

    def readAudioRecord(self):
        """
        This function reads an audio record ('.wav').
        """
        self.rate, self.audio = wavfile.read(findAudioRecord(self.path))

    def readTranscript(self):
        """
        This function reads a transcript ('.txt').
        """
        self.transcript = open(findTranscript(self.path), "r").read()

    def computeSpectrogram(self):
        """
        This function computes the spectrogram of an audio sample.
        """
        self.frequencies, self.timestamps, self.spectrogram = spectrogram(
            self.audio, self.rate
        )
