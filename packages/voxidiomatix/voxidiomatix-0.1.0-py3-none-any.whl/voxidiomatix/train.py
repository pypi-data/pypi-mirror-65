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

import pathlib
from scipy.io import wavfile
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from file_handler import findAudioRecord, findTranscript
from speech import Speech
from cascade_translator import CascadeTranslator


# PARAMETERS ==================================================================

OUTPUT_DIR = "voxidiomatix_translation/"


# SCRIPT ======================================================================


def train(args):

    print("==================================================================")
    print("                        Start Voxidiomatix                        ")
    print("------------------------------------------------------------------")
    print("                             Training                             ")
    print("==================================================================")

    # Load Data ---------------------------------------------------------------

    print("\n>>> Load data")

    input = Speech(
        name=pathlib.Path(args.speech).name,
        path=args.speech,
        language=args.fromlanguage,
    )
    input.readAudioRecord()
    input.readTranscript()
    input.computeSpectrogram()

    target = Speech(
        name=pathlib.Path(args.translation).name,
        path=args.translation,
        language=args.tolanguage,
    )
    target.readAudioRecord()
    target.readTranscript()
    target.computeSpectrogram()

    output = Speech(
        name="voxidiomatix_translation",
        path=str(pathlib.Path(args.speech).parent) + "/" + OUTPUT_DIR,
        language=args.tolanguage,
    )

    output.transcript = CascadeTranslator.textToTextTranslate(
        input.transcript, input.language, output.language
    )
    print(output.transcript)

    # plt.pcolormesh(times, frequencies, input.spectrogram)
    # plt.ylabel("Frequency [Hz]")
    # plt.xlabel("Time [sec]")
    # plt.show()
