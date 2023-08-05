#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .. import Unit
from ...lib.argformats import number

from os.path import isfile
from glob import glob


class fread(Unit):
    """
    Reads files from disk and outputs them individually. Has the ability to
    read large files in chunks.
    """

    @classmethod
    def interface(cls, argp):
        argp.add_argument(
            '-s', '--size',
            metavar='N',
            type=number,
            default=None,
            help=(
                'If specified, files will be read in chunks of size N and each '
                'chunk is emitted as one element in the output list.'
            )
        )
        argp.add_argument(
            'filenames',
            nargs='+',
            metavar='FILEMASK',
            help=(
                'A list of file masks (with wildcard patterns). Each matching '
                'file will be read from disk and emitted.'
            )
        )
        return super().interface(argp)

    def _read_chunks(self, fd):
        while True:
            buffer = fd.read(self.args.size)
            if not buffer:
                break
            yield buffer

    def process(self, data):
        for mask in self.args.filenames:
            for filename in glob(mask, recursive=True):
                if not isfile(filename):
                    continue
                try:
                    with open(filename, 'rb') as stream:
                        if not self.args.size:
                            self.log_info('reading:', filename)
                            yield dict(data=stream.read(), path=filename)
                        else:
                            yield from self._read_chunks(stream)
                except PermissionError:
                    self.log_warn('permission denied:', filename)
                except FileNotFoundError:
                    self.log_warn('file is missing:', filename)
                except Exception:
                    self.log_warn('unknown error while reading:', filename)
