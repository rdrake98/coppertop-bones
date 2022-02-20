# **********************************************************************************************************************
#
#                             Copyright (c) 2011-2012 David Briant. All rights reserved.
#
# This file is part of bones.
#
# bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************


import sys
sys._TRACE_IMPORTS = True


from coppertop.testing import HookStdOutErrToLines, assertRaises


def testStdoutHooker():
    with HookStdOutErrToLines() as outerr:
        lines = outerr[0]
        print("hello")
        assert len(lines) == 1, lines
        assert lines[0] == "hello", lines
        print()
        print("there", "is", "\n", "another line\nagain")
        print()
        assert len(lines) == 6, lines
        assert lines[2] == "there is ", lines
        assert lines[3] == " another line", lines
        assert lines[4] == "again", lines
        assert lines[5] == "", lines


def testAssertRaises():
    
    # test correct error
    with assertRaises(NotImplementedError) as e:
        raise NotImplementedError()
    assert e.exceptionType == NotImplementedError, (e.type, e.e)
    
    # test correct error
    with assertRaises(NotImplementedError) as e:
        raise NotImplementedError
    assert e.exceptionType == NotImplementedError, (e.type, e.e)
    
    # test no error
    try:
        with assertRaises(NotImplementedError) as e:
            pass
    except AssertionError:
        assert e.exceptionType == None, (e.type, e.e)
    except Exception as e:
        assert False, e
    
    # test wrong error
    class Fred(Exception): pass
    try:
        with assertRaises(NotImplementedError) as e:
            raise Fred
    except AssertionError:
        assert e.exceptionType == Fred, (e.exceptionType, e.e)
    except Exception as e:
        assert False, e


def main():
    testStdoutHooker()
    testAssertRaises()


if __name__ == '__main__':
    main()
    print('pass')

