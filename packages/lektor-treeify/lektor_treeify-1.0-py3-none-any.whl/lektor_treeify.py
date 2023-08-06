# -*- coding: utf-8 -*-
from more_itertools import split_before
from simplejson import JSONEncoder

from lektor.pluginsystem import Plugin
from lektor.types.flow import FlowBlock


def treeify(flat_list, level_attr='level'):
    if not flat_list:
        return []
    level = min(map(lambda l: l[level_attr], flat_list))
    chunks = split_before(flat_list, lambda r: r[level_attr] == level)
    for chunk in chunks:
        current = chunk.pop(0)
        yield {
            'name': current['caption'],
            'path': current['link'],
            'child': list(treeify(chunk, level_attr))
        }


def jsonify(structure):
    class JSONLeveledListEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, FlowBlock):
                return {x: obj[x] for x in obj._data.keys()}
            else:
                raise TypeError('not a flowblock')
    return JSONLeveledListEncoder().encode(structure)


class TreeifyPlugin(Plugin):
    name = 'Treeify'
    description = u'Plugin generate tree data structure from your flat menu model'

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters['treeify'] = treeify
        self.env.jinja_env.filters['jsonify'] = jsonify
