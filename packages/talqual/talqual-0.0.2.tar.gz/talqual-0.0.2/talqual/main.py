import logging

import yaml
from anytree import RenderTree

from .importer import FileSystemImporter
from .templates import Template


log = logging.getLogger('talqual')


def build(src, dst, data):
    # Read src directory
    importer = FileSystemImporter()
    log.debug(f'Reading templates from {src}')
    root = importer.import_(src)

    # Read data
    log.debug(f'Reading data from {data}')
    with open(data, 'r') as stream:
        data = yaml.safe_load(stream)

    # Make template tree
    templates = Template.template_from_tree(root)
    log.debug(f'Template Tree\n{RenderTree(templates).by_attr("name")}')

    # Render templates
    view = templates.render(data)
    log.debug(f'View Tree\n{RenderTree(view).by_attr("name")}')

    # Write views to dst directory
    log.debug(f'Writing to {dst}')
    view.write(dst)
    log.debug(f'Done. Output built at {dst}')
