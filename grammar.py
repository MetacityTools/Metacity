import sys
from typing import Dict, Hashable
from lark import Lark, Transformer
from functools import reduce
from pprint import pprint


STYLEGRAMMAR = r"""
    layer_rule_list: (layer_rules)*
    layer_rules: ("@layer(" string ")" "{" [(rule)*] "}")
    rule: visibility | layer_color | mapping | meta_rules

    visibility: ("@visible" ":" boolean ";")

    layer_color: ("@color" ":" color ";")

    mapping: source | target
    source: ("@source" "{" [ (meta_rule)* ] "}")
    target: ("@target" "{" [ (meta_rule)* ] "}")

    meta_rules: (meta_rule)* 
    meta_rule: ("@meta" "(" name_link ")" "{" [key_style ";"]* "}")

    name_link: (string [("." string)*])
    key_style: (key ":" color)
    
    key: string | any

    any: "@default"
    boolean: "true" -> true | "false" -> false
    string: NAME | ESCAPED_STRING
    color: COLOR
    NAME: (/\w/+)
    COLOR: ("#" HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT)

    %import common.HEXDIGIT
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    """

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key] #take the latter value
        else:
            a[key] = b[key]
    return a

ANYKEY = "@default"

class TreeToStyle(Transformer):
    def layer_rule_list(self, layer_rule_list_):
        return dict(layer_rule_list_)

    def layer_rules(self, layer_rules_):
        name, *rrules = layer_rules_
        output = {}
        reduce(merge, [output] + [r[0] for r in rrules])
        return (name, output)

    def rule(self, rule_):
        return rule_

    def visibility(self, v_):
        return {"visible": v_[0]}

    def layer_color(self, layer_color_):
        return {"color": layer_color_[0]}

    def mapping(self, mapping_):
        output = {
            "source": {},
            "target": {}
        }

        reduce(merge, [output, mapping_[0]])
        return output

    def source(self, source_rule_):
        _, *styles = source_rule_
        return {"source": dict(styles)}

    def target(self, target_rule_):
        _, *styles = target_rule_
        return {"target": dict(styles)}

    def meta_rules(self, o):
        return {'meta_rules': dict(o)}

    def meta_rule(self, meta_rule_):
        key, *styles = meta_rule_
        return (key, dict(styles))

    def name_link(self, name_link_):
        return tuple(name_link_)

    def key_style(self, key_style_):
        return key_style_

    def key(self, key_):
        return key_[0]

    def any(self, any_):
        return ANYKEY

    def NAME(self, name_):
        return str(name_)

    def ESCAPED_STRING(self, escaped_string_):
        return str(escaped_string_[1:-1])
    
    def string(self, string_):
        return string_[0]

    def number(self, number_):
        return float(number_[0])

    def color(self, color_):
        (color_,) = color_
        return int(color_[1:3], 16), int(color_[3:5], 16), int(color_[5:7], 16)

    true = lambda self, _: True
    false = lambda self, _: False


class LayerStyle:
    def __init__(self, style = None):
        self.style = style if style is not None else {}
        if style is not None:
            self.meta_rules = style['meta_rules']
            self.source = style['source']
            self.target = style['target']
        else:
            self.meta_rules = {}
            self.source = {}
            self.target = {}

    @property
    def visible(self):
        if 'visible' in self.style:
            return self.style['visible']
        return True

    @property
    def default_color(self):
        if 'color' in self.style:
            return self.style['color']
        return 255, 255, 255

    def source_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.source)

    def target_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.target)

    def object_color(self, object_meta):
        return self.apply_rules(object_meta, self.meta_rules)

    def apply_rules(self, object_meta, rules: Dict):
        for key, value_style in rules.items():
            matched, meta_subtree = self.get_value(object_meta, key)
            if matched:
                if (isinstance(meta_subtree, Hashable) and meta_subtree in value_style):
                    return value_style[meta_subtree]
                if ANYKEY in value_style:
                    return value_style[ANYKEY]

        return self.default_color

    def get_value(self, meta_subtree, key):
        match = True
        for part in key:
            if part in meta_subtree:
                meta_subtree = meta_subtree[part]
            else:
                match = False
                break
        if match:
            return True, meta_subtree # meta_subtree is now value in metadata
        return False, None


class Style:
    def __init__(self, styles=""):
        self.parser = Lark(STYLEGRAMMAR, start='layer_rule_list', lexer='dynamic_complete')
        self.raw_styles = styles
        self.tree = self.parser.parse(self.raw_styles)
        self.styles = TreeToStyle().transform(self.tree)

    def get_layer_style(self, layer):
        if layer in self.styles:
            return LayerStyle(self.styles[layer])
        return LayerStyle()


if __name__ == '__main__':
    styles = """
@layer(buildings) {
    @visible: true;
    @color: #555555;

    @meta(data.type) {
        building: #000000;
        bridge: #888888;
        terrain: #90FF00;
    }

    @meta(usage) {
        @default: #000000;
        school: #888888;
        museum: #90FF00;
    }

    @meta(floors) {
        zerotofive: #000000;
        fivetoten: #888888;
        tenandmore: #90FF00;
    }

    @source {
        @meta(test) {
            building: #000000;
            bridge: #888888;
            terrain: #90FF00;
        }

        @meta(test2.type) {
            building: #000000;
            bridge: #888888;
            terrain: #90FF00;
        }
    }

    @target {
        @meta(test) {
            building: #000000;
            bridge: #888888;
            terrain: #90FF00;
        }
    }
}

    """

    s = Style(styles)
    pprint(s.styles)

    style = s.get_layer_style("buildings")
    print(style.object_color({
        "data": {
            "type": "bridge"
        }
    }))

    print(style.source_object_color({
        "test2":  {
            "type": "terrain"
        }
    }))





