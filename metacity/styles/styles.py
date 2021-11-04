from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.datamodel.project import Project
from metacity.filesystem import styles as fs
from typing import Union
from typing import Dict
from lark import Lark, Transformer
from functools import reduce
from typing import  Hashable
import numpy as np



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


class LayerStyler:
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

def parse(raw_styles):
    parser = Lark(STYLEGRAMMAR, start='layer_rule_list', lexer='dynamic_complete')
    tree = parser.parse(raw_styles)
    return TreeToStyle().transform(tree)


def layer_style(layer: Union[Layer, LayerOverlay], parsed_styles):
    name = layer.name
    if name in parsed_styles:
        return LayerStyler(parsed_styles[name])
    else:
        return LayerStyler()


def compute_layer_colors(layer, color_function):
    colors = np.empty((layer.size, 3), dtype=np.uint8)
    for i, metaobject in enumerate(layer.meta):
        colors[i] = color_function(metaobject)
    return colors


def apply_layer_style(style: LayerStyler, style_name: str, project: Project, layer: Layer):
    colors = compute_layer_colors(layer, style.object_color)
    project.styles.add_style(style_name, layer.name, colors)


def apply_overlay_style(style: LayerStyler, style_name: str, project: Project, overlay: LayerOverlay):
    color_source = compute_layer_colors(project.get_layer(overlay.source_layer, load_set=False), style.source_object_color) 
    color_target = compute_layer_colors(project.get_layer(overlay.target_layer, load_set=False), style.target_object_color)
    project.styles.add_overlay_style(style_name, overlay.name, color_source, color_target)


def apply_style(style: LayerStyler, style_name: str, project: Project, layer: Union[Layer, LayerOverlay]):
    if isinstance(layer, Layer):
        apply_layer_style(style, style_name, layer)
    elif isinstance(layer, LayerOverlay):
        apply_overlay_style(style, style_name, project, layer)
    else:
        raise Exception("Unknown layer type")


class Style:
    def __init__(self, project: Project, style_name: str):
        self.project = project
        self.name = style_name
        self.mss_file = fs.style_mss(project.dir, style_name)
        self.parsed = None

    def parse(self):
        styles = self.get_styles()
        self.parsed = parse(styles)

    def apply(self):
        if self.parsed is None:
            self.parse()
            
        for layer in self.project.ilayers:
            style = layer_style(layer, self.parsed)
            apply_style(style, self, self.project, layer)

    def get_styles(self):
        styles = fs.base.read_mss(self.mss_file)
        return styles





 