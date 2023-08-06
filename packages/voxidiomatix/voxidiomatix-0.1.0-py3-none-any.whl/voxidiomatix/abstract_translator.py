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

from abc import ABCMeta, abstractmethod
from speech import Speech


# CLASS =======================================================================


class AbstractTranslator(ABCMeta):
    """
    This abstract class defines the interface of a Speech-to-Speech Multilangual Vocal Translator.
    """

    @abstractmethod
    def translate(self, speech: Speech, to_language: str):
        """
        This function translates a speech from one language to another.

        Arguments
        ---------
            speech : Speech
                Speech to translate
            to_language : string
                Language into which the speech has to be translated

        Returns
        -------
            Speech -- The translated speech into the desired language
        """
        raise NotImplementedError()
