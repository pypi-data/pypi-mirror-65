__author__ = "jan grant <parsy-extn@ioctl.org>"
__licence__ = "Apache License 2.0"

import parsy


class Noted:
    _aug_cache = {}

    @staticmethod
    def augment(obj):
        if isinstance(obj, Noted):
            return obj

        try:
            return Noted._aug_cache[obj.__class__]
        except KeyError:
            pass

        class Aug(Noted, obj.__class__):
            pass

        Aug.__name__ = type(obj).__name__ + 'WithNotes'

        obj = Aug(obj)
        obj._notes = []
        return obj

    def notes_for(self, index):
        for i in range(len(self._notes) - 1, -1, -1):
            idx, n = self._notes[i]
            if idx <= index:
                self._notes = self._notes[:i + 1]
                return dict(n)
        return {}

    def notes_update(self, index, kv):
        for i in range(len(self._notes) - 1, -1, -1):
            idx, n = self._notes[i]
            if idx == index:
                self._notes[i:] = [(index, kv)]
                return
            elif idx < index:
                self._notes[i + 1:] = [(index, kv)]
                return
        self._notes = [(index, kv)]

    def __repr__(self):
        return "{!r}{!r}".format(super(), self._notes)


@parsy.Parser
def get_notes(stream, index):
    return parsy.Result.success(index, stream.notes_for(index))


def put_note(kv):
    @parsy.Parser
    def put_notes(stream, index):
        return parsy.Result.success(index, stream.notes_update(index, kv))

    return put_notes


def keeps_notes(parser):
    orig_parse = parser.parse

    def parse_(stream):
        return orig_parse(Noted.augment(stream))

    parser.parse = parse_
    return parser


def monkeypatch_parsy():
    orig_parse_partial = parsy.Parser.parse_partial

    def parse_partial(self, stream):
        return orig_parse_partial(self, Noted.augment(stream))

    parsy.Parser.parse_partial = parse_partial

    def undo():
        parsy.Parser.parse_partial = orig_parse_partial

    return undo
