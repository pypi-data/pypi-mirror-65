from __future__ import annotations

import sys
from typing import TextIO, Optional

from stx.action import Action
from stx.compiling.reading.location import Location
from stx.data_notation.values import Value
from stx.document import Document
from stx.utils.files import resolve_sibling


class OutputTarget:

    @staticmethod
    def make(document: Document, target: str) -> OutputTarget:
        # TODO add more targets

        file_path = resolve_sibling(
            document.source_file, target)

        return OutputFile(file_path)

    def dump(self, handler: OutputAction):
        raise NotImplementedError()


class OutputFile(OutputTarget):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def dump(self, handler: OutputAction):
        with open(self.file_path, mode='w') as out:
            handler.dump(out)


class OutputStdOut(OutputTarget):

    def dump(self, handler: OutputAction):
        handler.dump(sys.stdout)


class OutputAction(Action):

    def __init__(
            self,
            document: Document,
            location: Location,
            format_key: str,
            target: OutputTarget,
            options: Value,
            theme: Optional[str]):
        self.document = document
        self.location = location
        self.format_key = format_key
        self.target = target
        self.options = options
        self.theme = theme

    def dump(self, out: TextIO):
        raise NotImplementedError()

    def run(self):
        self.target.dump(self)
