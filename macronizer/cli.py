# Copyright 2015-2021 Johan Winge
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import codecs
import sys
import typing as t
import unicodedata

from macronizer.cgi import SCANSIONS
from macronizer.lib import Macronizer, evaluate


def parser(args: t.Sequence[str] | None = None):
    parser = argparse.ArgumentParser()
    infile_group = parser.add_mutually_exclusive_group()
    infile_group.add_argument("-i", "--infile", help="file to read from; otherwise stdin")
    parser.add_argument("-o", "--outfile", help="file to write to; otherwise stdout")
    parser.add_argument(
        "-v", "--utov", action="store_true", help="convert u to v where appropriate"
    )
    parser.add_argument("-j", "--itoj", action="store_true", help="similarly convert i to j")
    parser.add_argument("-s", "--scan", help="try to scan using metre SCAN")
    parser.add_argument("--listscans", action="store_true", help="list available metres")
    macrons_group = parser.add_mutually_exclusive_group()
    macrons_group.add_argument("--nomacrons", action="store_true", help="don't mark long vowels")
    macrons_group.add_argument(
        "--maius", action="store_true", help="do mark vowels also in māius and such"
    )
    infile_group.add_argument(
        "--test", action="store_true", help="mark vowels in a short example text"
    )
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="reset the database (only necessary once)",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="test accuracy against input gold standard",
    )
    parsed = parser.parse_args(args)

    if parsed.initialize:
        try:
            macronizer = Macronizer()
            macronizer.wordlist.reinitializedatabase()
        except Exception as e:
            print(e)
            exit(1)
        exit(0)

    if parsed.listscans:
        for i, [description, _] in enumerate(SCANSIONS):
            print("%i: %s" % (i, description))
        exit(0)

    macronizer = Macronizer()
    if parsed.test:
        texttomacronize = "O orbis terrarum te saluto!\n"
    else:
        if parsed.infile is None:
            if sys.version_info[0] < 3:
                infile = codecs.getreader("utf-8")(sys.stdin)
            else:
                infile = sys.stdin
        else:
            infile = codecs.open(parsed.infile, "r", "utf8")
        texttomacronize = infile.read()

    texttomacronize = unicodedata.normalize("NFC", texttomacronize)
    macronizer.settext(texttomacronize)
    try:
        scan = int(parsed.scan)
    except (TypeError, ValueError):
        scan = 0
    if scan > 0:
        macronizer.scan(SCANSIONS[scan][1])
    macronizedtext = macronizer.gettext(
        not parsed.nomacrons, parsed.maius, parsed.utov, parsed.itoj, markambigs=False
    )
    if parsed.evaluate:
        (accuracy, _) = evaluate(texttomacronize, macronizedtext)
        print("Accuracy: %f" % (accuracy * 100))
    else:
        if parsed.outfile is None:
            if sys.version_info[0] < 3:
                outfile = codecs.getwriter("utf8")(sys.stdout)
            else:
                outfile = sys.stdout
        else:
            outfile = codecs.open(parsed.outfile, "w", "utf8")
        outfile.write(macronizedtext)


if __name__ == "__main__":
    parser()
