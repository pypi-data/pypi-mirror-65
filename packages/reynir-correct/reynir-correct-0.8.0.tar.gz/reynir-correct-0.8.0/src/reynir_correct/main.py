#!/usr/bin/env python
"""

    Greynir: Natural language processing for Icelandic

    Spelling and grammar checking module

    Copyright (C) 2020 Miðeind ehf.

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


    This is an executable program wrapper (main module) for the ReynirCorrect
    package. It can be used to invoke the corrector from the command line,
    or via fork() or exec(), with the command 'correct'. The main() function
    of this module is registered as a console_script entry point in setup.py.

"""

import sys
import argparse
import json
from functools import partial

from tokenizer import detokenize, normalized_text_from_tokens
from .errtokenizer import TOK, tokenize


# File types for UTF-8 encoded text files
ReadFile = argparse.FileType('r', encoding="utf-8")
WriteFile = argparse.FileType('w', encoding="utf-8")

# Define the command line arguments

parser = argparse.ArgumentParser(description="Corrects Icelandic text")

parser.add_argument(
    'infile',
    nargs='?',
    type=ReadFile,
    default=sys.stdin,
    help="UTF-8 text file to correct",
)
parser.add_argument(
    'outfile',
    nargs='?',
    type=WriteFile,
    default=sys.stdout,
    help="UTF-8 output text file"
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--csv",
    help="Output one token per line in CSV format", action="store_true"
)
group.add_argument(
    "--json",
    help="Output one token per line in JSON format", action="store_true"
)
group.add_argument(
    "--spaced",
    help="Separate tokens with spaces", action="store_true"
)


def main():
    """ Main function, called when the tokenize command is invoked """

    args = parser.parse_args()

    # By default, no options apply
    options = {}
    if not (args.csv or args.json):
        # If executing a plain ('shallow') correct,
        # apply most suggestions to the text
        options["apply_suggestions"] = True

    def quote(s):
        """ Return the string s within double quotes, and with any contained
            backslashes and double quotes escaped with a backslash """
        if not s:
            return "\"\""
        return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

    def gen(f):
        """ Generate the lines of text in the input file """
        yield from f

    def val(t, quote_word=False):
        """ Return the value part of the token t """
        if t.val is None:
            return None
        if t.kind in {TOK.WORD, TOK.PERSON, TOK.ENTITY}:
            # No need to return list of meanings
            return None
        if t.kind in {TOK.PERCENT, TOK.NUMBER, TOK.CURRENCY}:
            return t.val[0]
        if t.kind == TOK.AMOUNT:
            if quote_word:
                # Format as "1234.56|USD"
                return "\"{0}|{1}\"".format(t.val[0], t.val[1])
            return t.val[0], t.val[1]
        if t.kind == TOK.S_BEGIN:
            return None
        if t.kind == TOK.PUNCTUATION:
            return quote(t.val[1]) if quote_word else t.val[1]
        if quote_word and t.kind in {
            TOK.DATE, TOK.TIME, TOK.DATEABS, TOK.DATEREL, TOK.TIMESTAMP,
            TOK.TIMESTAMPABS, TOK.TIMESTAMPREL, TOK.TELNO, TOK.NUMWLETTER,
            TOK.MEASUREMENT
        }:
            # Return a |-delimited list of numbers
            return quote("|".join(str(v) for v in t.val))
        if quote_word and isinstance(t.val, str):
            return quote(t.val)
        return t.val

    # Function to convert a token list to output text
    if args.spaced:
        to_text = normalized_text_from_tokens
    else:
        to_text = partial(detokenize, normalize=True)

    # Configure our JSON dump function
    json_dumps = partial(json.dumps, ensure_ascii=False, separators=(',', ':'))

    # Initialize sentence accumulator list
    curr_sent = []

    for t in tokenize(gen(args.infile), **options):
        if args.csv:
            # Output the tokens in CSV format, one line per token
            if t.txt:
                print(
                    "{0},{1},{2},{3}"
                    .format(
                        t.kind,
                        quote(t.txt),
                        val(t, quote_word=True) or "\"\"",
                        quote(str(t.error) if t.error else None)
                    ),
                    file=args.outfile
                )
            elif t.kind == TOK.S_END:
                # Indicate end of sentence
                print("0,\"\",\"\"", file=args.outfile)
        elif args.json:
            # Output the tokens in JSON format, one line per token
            d = dict(k=TOK.descr[t.kind])
            if t.txt is not None:
                d["t"] = t.txt
            v = val(t)
            if t.kind not in {TOK.WORD, TOK.PERSON, TOK.ENTITY} and v is not None:
                d["v"] = v
            if t.error is not None:
                d["e"] = t.error.to_dict()
            print(json_dumps(d), file=args.outfile)
        else:
            # Normal shallow parse, one line per sentence,
            # tokens separated by spaces
            if t.kind in TOK.END:
                # End of sentence/paragraph
                if curr_sent:
                    print(to_text(curr_sent), file=args.outfile)
                    curr_sent = []
            else:
                curr_sent.append(t)

    if curr_sent:
        print(to_text(curr_sent), file=args.outfile)


if __name__ == "__main__":
    main()
