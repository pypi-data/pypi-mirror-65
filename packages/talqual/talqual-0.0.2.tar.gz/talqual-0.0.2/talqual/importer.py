from pathlib import Path

from anytree import Node


class FileSystemImporter(object):
    """Import Tree from FileSystem"""
    def __init__(self, nodecls=Node):
        self.nodecls = nodecls

    def import_(self, directory):
        """Import tree from `directory`."""
        return self.__import(Path(directory))

    def __import(self, path, parent=None):
        node = self.nodecls(path.name, parent=parent)
        if path.is_dir():
            for child in path.iterdir():
                self.__import(child, parent=node)
        elif path.is_file():
            node.value = path.read_bytes()
        return node
