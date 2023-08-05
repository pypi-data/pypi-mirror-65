from functools import partial

import chameleon


class PageTemplate(chameleon.PageTemplate):
    """`PageTemplate` with loader from `Templates`"""

    expression_types = chameleon.PageTemplate.expression_types.copy()
    expression_types['load'] = partial(chameleon.tales.ProxyExpr, '__loader')

    def _builtins(self):
        d = super()._builtins()
        d['__loader'] = self._loader
        return d

    def _loader(self, path):
        raise NotImplementedError()
