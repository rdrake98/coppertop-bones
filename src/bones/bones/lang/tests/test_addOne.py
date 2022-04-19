# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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
from bones.kernel.the import kernel
from dm.std import check, equal, first


def test_addOne():
    k = kernel()
    pfn = glob('./bones/addOne.bones', recursive=True) >> first
    with open(pfn) as f:
        # get the kernel to build the source (pass as a stream or unicode string - could be from a db, file, repl etc)
        answer = k.build(f)
    answer >> check >> equal >> 2
    2 >> kernel.addOne.addOne >> check >> equal >> 3   # public interface is as if it has been wrapped with @coppertop



def main():
    test_addOne()


if __name__ == '__main__':
    main()
    print("pass")
