from pathlib import Path

from anytree import Node


class View(Node):
    """A rendered `Template` with data

    * self.value: File contents
    """

    def relative_path(self):
        return self.separator.join([str(node.name) for node in self.path[1:]])

    def _write_contents(self, directory):
        """
        :type directory: `Path`
        """
        path = directory.joinpath(self.relative_path())

        if 'value' in self.__dict__ and isinstance(self.value, bytes):
            f = open(path, 'wb')
        else:
            f = open(path, 'w')

        if 'value' in self.__dict__:
            f.write(self.value)
        f.close()

    def _write_folder(self, directory):
        """
        :type directory: `Path`
        """
        if self.is_root:
            pass
        path = directory.joinpath(self.relative_path())
        if not path.exists():
            path.mkdir()

    def write(self, directory='html'):
        """
        :type directory: `Path` or `str`
        """
        directory = Path(directory)
        if self.is_leaf:
            self._write_contents(directory)
        else:
            self._write_folder(directory)

        for child in self.children:
            child.write(directory)


class CollectionView(View):
    """A collection of `Views` that get rendered directly on parent"""
    pass
