from metacity.datamodel.layer import Layer, LayerOverlay
from typing import Union
from typing import Dict
from lark import Lark, Transformer
from functools import reduce
import collections


STYLEGRAMMAR = r"""
    layer_rule_list: (layer_rules)*
    layer_rules: (string "{" [(rule)*] "}")
    rule: visibility | mapping | meta_rules

    visibility: ("visible" ":" boolean ";")

    mapping: ("mapping" "{" (mapping_rule)* "}")
    mapping_rule: source_rule | target_rule
    source_rule: ("source.meta" "[" name_link "]" "{" [key_style ";"]* "}")
    target_rule: ("target.meta" "[" name_link "]" "{" [key_style ";"]* "}")

    meta_rules: (meta_rule)* 
    meta_rule: ("meta" "[" name_link "]" "{" [key_style ";"]* "}")

    name_link: (string [("." string)*])
    key_style: (string ":" color)
    
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


class TreeToStyle(Transformer):
    def layer_rule_list(self, layer_rule_list_):
        return dict(layer_rule_list_)

    def layer_rules(self, layer_rules_):
        name, *rrules = layer_rules_
        output = {}
        reduce(merge, [output] + [dict(r) for r in rrules])
        return (name, output)

    def rule(self, rule_):
        return rule_

    def visibility(self, v_):
        return ('visible', v_)

    def mapping(self, mapping_):
        output = {
            "source": {},
            "target": {}
        }

        print(mapping_)
        reduce(merge, [output] + [{t: {k: r}} for t, (k, r)  in mapping_])
        return ("mapping", output)

    def source_rule(self, source_rule_):
        key, *styles = source_rule_
        return ("source", (key, dict(styles)))

    def target_rule(self, target_rule_):
        key, *styles = target_rule_
        return ("target", (key, dict(styles)))

    def mapping_rule(self, mapping_rule_):
        return mapping_rule_[0]

    def meta_rules(self, o):
        return ('meta_rules', dict(o))

    def meta_rule(self, meta_rule_):
        key, *styles = meta_rule_
        return (key, dict(styles))

    def name_link(self, name_link_):
        return tuple(name_link_)

    def key_style(self, key_style_):
        return key_style_

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
            self.source = style['mapping']['source']
            self.target = style['mapping']['target']
        else:
            self.meta_rules = {}
            self.source = {}
            self.target = {}

    @property
    def visible(self):
        if 'visible' in self.style:
            return self.style['visible']
        return True

    def source_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.source)

    def target_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.target)

    def object_color(self, object_meta):
        print("rules", self.meta_rules)
        return self.apply_rules(object_meta, self.meta_rules)

    def apply_rules(self, object_meta, rules: Dict):
        print(rules, object_meta)
        for key, value_style in rules.items():
            matched, value = self.get_value(object_meta, key)

            if matched and isinstance(value, collections.Hashable) and value in value_style:
                return value_style[value]
        return (255, 255, 255) # white is default for now

    def get_value(self, meta_subtree, key):
        match = True
        for part in key:
            print("      ", part, " in ", meta_subtree)
            if part in meta_subtree:
                meta_subtree = meta_subtree[part]
            else:
                match = False
                break
        if match:
            return True, meta_subtree # meta_subtree is now value
        return False, None


class Style:
    def __init__(self, styles=""):
        self.parser = Lark(STYLEGRAMMAR, start='layer_rule_list', lexer='dynamic_complete')
        self.raw_styles = styles
        self.tree = self.parser.parse(self.raw_styles)
        print(self.tree.pretty())
        self.styles = TreeToStyle().transform(self.tree)

    def get_layer_style(self, layer):
        if layer in self.styles:
            return LayerStyle(self.styles[layer])
        return LayerStyle()


def style_layer(layer: Union[LayerOverlay, Layer], styles: str):
    styles = Style(styles)

