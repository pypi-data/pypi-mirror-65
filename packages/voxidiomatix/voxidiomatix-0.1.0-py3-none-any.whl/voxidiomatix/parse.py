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

from argparse import ArgumentParser
from train import train
from translate import translate


# FUNCTIONS ===================================================================


def parse():
    """
    This function parses the command line arguments of the Voxidiomatix script.

    Returns
    -------
        'argparse.Namespace' -- The parsed arguments
    """

    parser = ArgumentParser(
        description="Voxidiomatix translates a vocal speech from one language to another while preserving the vocal characteristics of the speaker in the translated speech."
    )

    subparser = parser.add_subparsers(help="Voxidiomatix's modes")

    addTrainParser(subparser)
    addTranslateParser(subparser)

    return parser.parse_args()


def addTrainParser(subparser):
    """
    This function creates the parser for the training mode.

    Arguments
    ---------
        subparser : 'argparse._SubParsersAction'
            Subparser
    """

    train_parser = subparser.add_parser(
        "train",
        help="To train Voxidiomatix using the original speech and its ground truth translation",
    )
    train_parser.add_argument(
        "speech",
        type=str,
        help="Path to the directory of the original speech, containing the audio record ('.wav') and the transcript ('.txt')",
    )
    train_parser.add_argument(
        "translation",
        type=str,
        help="Path to the directory of the ground truth translation, containing the audio record ('.wav') and the transcript ('.txt')",
    )
    train_parser.add_argument(
        "-from",
        "--fromlanguage",
        type=str,
        choices=["auto", "DE", "EN", "FR", "ES", "IT", "NL", "PL"],
        default="auto",
        help="Language of the original speech",
    )
    train_parser.add_argument(
        "-to",
        "--tolanguage",
        type=str,
        choices=["DE", "EN", "FR", "ES", "IT", "NL", "PL"],
        default="EN",
        help="Language into which the speech is to be translated",
    )
    train_parser.set_defaults(func=train)


def addTranslateParser(subparser):
    """
    This function creates the parser for the translation mode.

    Arguments
    ---------
        subparser : 'argparse._SubParsersAction'
            Subparser
    """

    translate_parser = subparser.add_parser(
        "translate", help="To translate a vocal speech"
    )
    translate_parser.add_argument(
        "speech",
        type=str,
        help="Path to the audio record ('.wav') of the speech to translate",
    )
    translate_parser.add_argument(
        "--fromlanguage",
        type=str,
        choices=["auto", "DE", "EN", "FR", "ES", "IT", "NL", "PL"],
        default="auto",
        help="Language of the original speech",
    )
    translate_parser.add_argument(
        "--tolanguage",
        type=str,
        choices=["DE", "EN", "FR", "ES", "IT", "NL", "PL"],
        default="EN",
        help="Language into which the speech is to be translated",
    )
    translate_parser.set_defaults(func=translate)
