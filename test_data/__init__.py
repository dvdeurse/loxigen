#!/usr/bin/python
# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

import os

_test_data_dir = os.path.dirname(os.path.realpath(__file__))

def list_files():
    """
    Return a list of the data files in this directory

    These strings are suitable to be passed to read().
    """

    result = []
    for dirname, dirnames, filenames in os.walk(_test_data_dir):
        dirname = os.path.relpath(dirname, _test_data_dir)
        for filename in filenames:
            if filename.endswith('.data') and not filename.startswith('.'):
                result.append(dirname + '/' + filename)
    return sorted(result)

def exists(name):
    return os.path.exists(os.path.join(_test_data_dir, name))

def read(name):
    """
    Read, parse, and return a test data file

    @param name Filename relative to the test_data directory
    @returns A hash from section to the string contents

    A section named "binary" is treated specially: it's treated
    as a hex dump and parsed into a binary string.
    """

    section_lines = {}
    cur_section = None

    with open(os.path.join(_test_data_dir, name)) as f:
        for line in f:
            line = line.rstrip().partition('#')[0].rstrip()
            if line == '':
                continue
            elif line.startswith('--'):
                cur_section = line[2:].strip()
                if cur_section in section_lines:
                    raise Exception("section %s already exists in the test data file")
                section_lines[cur_section] = []
            elif cur_section:
                section_lines[cur_section].append(line)
    data = { section: '\n'.join(lines) for (section, lines) in section_lines.items() }

    # Special case: convert 'binary' section into binary
    # The string '00 11\n22 33' results in "\x00\x11\x22\x33"
    if 'binary' in data:
        hex_strs = data['binary'].split()
        data['binary'] = ''.join(map(lambda x: chr(int(x, 16)), hex_strs))

    return data
