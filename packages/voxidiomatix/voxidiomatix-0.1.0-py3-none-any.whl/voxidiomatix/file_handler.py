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

import os


# FUNCTIONS ===================================================================


def findAudioRecord(directory: str):
    """
    This function finds the audio record ('.wav') in a given directory.

    Arguments
    ---------
        directory : string
            Path to the directory to search

    Returns
    -------
        string -- The full path to the audio record: path/to/audio/record.wav
    """

    file = findFile(directory, ".wav")
    if file == None:
        print(
            "Error: there is no audio record ('.wav') in the directory: "
            + directory
        )
    return file


def findTranscript(directory: str):
    """
    This function finds the transcript ('.txt') in a given directory.

    Arguments
    ---------
        directory : string
            Path to the directory to search

    Returns
    -------
        string -- The full path to the transcript: path/to/transcript.txt
    """

    file = findFile(directory, ".txt")
    if file == None:
        print(
            "Error: there is no transcript ('.txt') in the directory: "
            + directory
        )
    return file


def findFile(directory: str, extension: str):
    """
    This function finds the file with the given extension in the given directory.

    Warning: There should not be several files with the given extension in the given directory. In this case, this function will return the first file found with the right extension.

    Arguments
    ---------
        directory : string
            Path to the directory to search
        extension : string
            Extension of the file to find

    Returns
    -------
        string -- The full path to the file: path/to/file.extension
    """

    for f in os.listdir(directory):
        if os.path.splitext(f)[1] == extension:
            return os.path.join(directory, f)
    return None
