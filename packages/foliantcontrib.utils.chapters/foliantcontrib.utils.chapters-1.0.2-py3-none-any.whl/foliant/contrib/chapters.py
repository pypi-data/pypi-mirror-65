from pathlib import PosixPath, Path


def flatten_seq(seq):
    """convert a sequence of embedded sequences into a plain list"""
    result = []
    vals = seq.values() if type(seq) == dict else seq
    for i in vals:
        if isinstance(i, (dict, list)):
            result.extend(flatten_seq(i))
        elif isinstance(i, str):
            result.append(i)
    return result


class Chapters:
    """
    Helper class converting chapter list of complicated structure
    into a plain list of chapter names or path to actual md files
    in the src dir.
    """

    def __init__(self,
                 chapters: list):
        self._chapters = chapters
        self._flat = flatten_seq(chapters)

    def __len__(self):
        return len(self._flat)

    def __getitem__(self, ind: int):
        return self._flat[ind]

    def __contains__(self, item: str):
        return item in self._flat

    def __iter__(self):
        return iter(self._flat)

    def __repr__(self):
        return f'Chapters({self._chapters})'

    @property
    def chapters(self):
        """Original chapters list"""
        return self._chapters

    @chapters.setter
    def chapters(self, chapters):
        self._chapters = chapters
        self._flat = flatten_seq(chapters)

    @property
    def flat(self):
        """Flat list of chapter file names"""
        return self._flat

    def paths(self, parent_dir: str or PosixPath):
        """
        Returns generator yielding PosixPath object with chapter path, relative
        to parent_dir.
        """

        return (Path(parent_dir) / chap for chap in self.flat)
