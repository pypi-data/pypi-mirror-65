from pathlib import Path


class Batch():
    """Split collection of items over multiple pages"""
    def __init__(self, items, size=5, base_name='item.html'):
        self.items = items
        self.size = size
        self.base_name = base_name

    def total(self):
        """Total number of pages"""
        return -(-len(self.items)//self.size)  # ceil division

    def get_url(self, page=0):
        if page is None:
            return
        if page <= 1:
            # First page without numbering?
            return self.base_name
        path = Path(self.base_name)
        return f'{path.stem}.{page}{path.suffix}'

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        if self.num >= self.total():
            raise StopIteration
        self.num += 1
        page_items = self.items[(self.num-1)*self.size:self.num*self.size]
        return BatchPage(page_items, self.num, batch=self)


class BatchPage(list):
    def __init__(self, items, num, batch=None):
        list.__init__(self, items)
        self.num = num
        self.batch = batch

    @property
    def first(self):
        return 1

    @property
    def prev(self):
        if self.num > self.first:
            return self.num-1

    @property
    def current(self):
        return self.num

    @property
    def next(self):
        if self.num < self.last:
            return self.num+1

    @property
    def last(self):
        return self.batch.total()

    @property
    def url(self):
        return self.get_url(self.num)

    def get_url(self, page):
        return self.batch.get_url(page)
