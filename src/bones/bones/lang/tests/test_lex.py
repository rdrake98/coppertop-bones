# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
#
# bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from glob import glob

from coppertop.core import *
from bones.lang import lex
from bones.core.sym import SymTable


def test_lex_bones_files():
    for pfn in glob('./bones/*.bones', recursive=True):
        pfn >> PP
        with open(pfn) as f:
            src = f.read()
        st = SymTable()
        tokens, lines = lex.lexBonesSrc(src, st)



def main():
    test_lex_bones_files()


if __name__ == '__main__':
    main()
    print("pass")
