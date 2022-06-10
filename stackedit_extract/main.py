from collections import OrderedDict
from dataclasses import dataclass, field
import json
import logging
from typing import Any, Union
from pathlib import Path

import click

from .util.slugify import slugify

Node = Union['File', 'Dir']

@dataclass
class File:
    json_id: str
    json_name: str
    json_parent_id: str
    fs_name: str
    content: str = ''

@dataclass
class Dir:
    json_id: str = ''
    json_name: str = ''
    json_parent_id: str = ''
    fs_name: str = ''
    children: list[Node] = field(default_factory=list)


@click.command()
@click.option('--output', '-o', 'output_dir', type=click.Path(file_okay=False, path_type=Path))
@click.argument('input_file', type=click.File('r', encoding='utf-8-sig'))
def main(input_file, output_dir):
    input_json: dict[str, Any] = json.load(input_file,  object_pairs_hook=OrderedDict)
    root = Dir()
    lookup: dict[str, Node] = dict()
    # step 1: metadata -> our node
    for json_id, entry in input_json.items():
        if entry['type'] == 'folder':
            lookup[json_id] = Dir(
                json_id=json_id,
                json_name=entry['name'],
                json_parent_id=entry['parentId'],
                fs_name=slugify(entry['name'])
            )
        elif entry['type'] == 'file':
            lookup[json_id] = File(
                json_id=json_id,
                json_name=entry['name'],
                json_parent_id=entry['parentId'],
                fs_name=slugify(entry['name'])
            )

    # step 2: build tree from node
    for json_id, node in lookup.items():
        if node.json_parent_id:
            try:
                lookup[node.json_parent_id].children.append(node)
            except KeyError:
                logging.warn(f'cannot find parent of "{json_id}": "{node.json_parent_id}"')
        else:
            root.children.append(node)

    # step 3: fill in the content for each file
    for json_id, entry in input_json.items():
        if entry['type'] == 'content':
            real_json_id = json_id.removesuffix('/content')
            lookup[real_json_id].content = entry['text']

    # step 4: flush to output dir
    flush(root, output_dir)


def flush(node: Node, path: Path):
    if isinstance(node, File):
        path.with_suffix('.md').write_text(node.content, encoding='utf-8')
        return
    # now it's a dir
    path.mkdir(exist_ok=True)
    for child in node.children:
        flush(child, path / child.fs_name)
