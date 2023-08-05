from importlib import resources
from pathlib import Path

from anytree import Node
from anytree.resolver import Resolver

from .batch import Batch
from .views import CollectionView, View
from .zpt import PageTemplate


class Template(Node):
    """
    def __init__(self, name, parent=None, children=None, **kwargs):
    self.__dict__.update(kwargs)

    * self.value: File contents
    """
    @classmethod
    def subclass_from_node(cls, node):
        """Return the correct Template class for `node`"""
        subtypes = [NoView, Folder, TalCommand, HtmlPt]
        for subtype in subtypes:
            if subtype.match(node):
                return subtype
        return cls

    @classmethod
    def template_from_tree(cls, node):
        subclass = cls.subclass_from_node(node)
        root = subclass(**node.__dict__)
        for child in node.children:
            cls.template_from_tree(child).parent = root
        return root

    def load_template(self, path):
        template = Resolver('name').get(self, path.strip())
        return PageTemplate(template.value)

    def render(self, data):
        if self.is_root and isinstance(self, Folder):
            # first time
            PageTemplate._loader = self.load_template

        return View(**self.__dict__)


class HtmlPt(Template):
    """
    * self._template
    """
    ext = ('.html', '.htm', '.pt')

    @classmethod
    def match(cls, node):
        ext = Path(node.name).suffix
        return ext in cls.ext

    def chameleon_template(self):
        return PageTemplate(self.value)

    def render(self, data):
        name = self.name
        if name.endswith('.pt'):
            name = Path(name).with_suffix('.html')
        value = self.chameleon_template().render(**data)
        return View(name=name, value=value)


class Folder(Template):

    @classmethod
    def match(cls, node):
        return not node.is_leaf

    def render(self, data):
        root = super().render(data)
        for child in self.children:
            view = child.render(data)
            if view:
                if isinstance(view, CollectionView):
                    for v in view.children:
                        v.parent = root
                else:
                    view.parent = root
        return root


class NoView(Template):
    prefix = '_'

    @classmethod
    def match(cls, node):
        return node.name.startswith(cls.prefix)

    def render(self, data):
        pass


class TalCommand(Template):
    prefix = '.tal_'

#    taldefine = 'tal_define.'
#    talreplace = 'tal_replace.'

    @classmethod
    def match(cls, node):
        return cls.prefix in node.name

    def get_command(self, stem):
        commands = [TalCommandRepeat, TalCommandBatch, TalCommandReplace]

        for command in commands:
            if command.prefix in stem:
                return command
        return None

    def render(self, data):
        """Return `CollectionView` with all rendered subviews"""
        collection = CollectionView(self.name)

        name = Path(self.name)
        stems = name.stem.split('.')
        base_name = stems[0]
        ext = name.suffix

        for stem in stems:
            command = self.get_command(stem)
            if command is not None:
                stems.remove(stem)
                template = HtmlPt(**self.__dict__)
                command = command(collection, template, data, base_name, ext)
                parameters = stem[len(command.prefix):]
                command.execute(parameters)

        return collection


class TalCommandType():
    def __init__(self, collection, template, data, base_name, ext):
        self.collection = collection
        self.template = template
        self.data = data
        self.base_name = base_name
        if ext == '.pt':
            ext = '.html'
        self.ext = ext


class TalCommandRepeat(TalCommandType):
    prefix = 'tal_repeat_'

    def execute(self, parameters):
        items = self.data[parameters]
        for num, item in enumerate(items):
            item['num'] = num
            self.data['item'] = item
            view = self.template.render(self.data)
            view.name = f'{self.base_name}.{num}{self.ext}'
            view.parent = self.collection


class TalCommandBatch(TalCommandType):
    prefix = 'tal_batch_'

    def execute(self, parameters):
        variable, size = parameters.split('_')
        size = int(size)
        items = self.data[variable]
        for page in Batch(items, size, base_name=self.base_name + self.ext):
            self.data[variable] = page
            view = self.template.render(self.data)
            view.name = page.url
            view.parent = self.collection
        self.data[variable] = items


class TalCommandReplace(TalCommandType):
    prefix = 'tal_replace_'

    def execute(self, parameters):
        if parameters == 'talqual_scripts':
            pkg = 'talqual.static'
            transcrypt_js = 'org.transcrypt.__runtime__.js'
            value = resources.read_binary(package=pkg, resource='scripts.js')
            template = Template(f'{self.base_name}{self.ext}', value=value)
            view = template.render(self.data)
            view.parent = self.collection
            value2 = resources.read_binary(package=pkg, resource=transcrypt_js)
            template2 = Template(transcrypt_js, value=value2)
            view2 = template2.render(self.data)
            view2.parent = self.collection
            return
