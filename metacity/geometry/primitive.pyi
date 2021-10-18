from typing import List, Tuple

class MultiLine(Primitive):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_l2(self, arg0: List[float]) -> None: ...
    def push_l3(self, arg0: List[float]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> SimplePrimitive: ...
    @property
    def type(self) -> str: ...

class MultiPoint(Primitive):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_p2(self, arg0: List[float]) -> None: ...
    def push_p3(self, arg0: List[float]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> SimplePrimitive: ...
    @property
    def type(self) -> str: ...

class MultiPolygon(Primitive):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_p2(self, arg0: List[List[float]]) -> None: ...
    def push_p3(self, arg0: List[List[float]]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> SimplePrimitive: ...
    @property
    def type(self) -> str: ...

class Primitive:
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> SimplePrimitive: ...
    @property
    def type(self) -> str: ...

class SimpleMultiLine(SimplePrimitive):
    def __init__(self) -> None: ...
    def copy(self) -> SimplePrimitive: ...
    def slice_to_grid(self, arg0: float) -> List[SimplePrimitive]: ...
    @property
    def type(self) -> str: ...

class SimpleMultiPoint(SimplePrimitive):
    def __init__(self) -> None: ...
    def copy(self) -> SimplePrimitive: ...
    def slice_to_grid(self, arg0: float) -> List[SimplePrimitive]: ...
    @property
    def type(self) -> str: ...

class SimpleMultiPolygon(SimplePrimitive):
    def __init__(self) -> None: ...
    def copy(self) -> SimplePrimitive: ...
    def slice_to_grid(self, arg0: float) -> List[SimplePrimitive]: ...
    @property
    def type(self) -> str: ...

class SimplePrimitive(Primitive):
    def __init__(self) -> None: ...
    def add_attribute(self, arg0: str, arg1: int) -> None: ...
    def copy(self) -> SimplePrimitive: ...
    def deserialize(self, arg0: json) -> None: ...
    def join(self, arg0: SimplePrimitive) -> None: ...
    def serialize(self) -> json: ...
    def slice_to_grid(self, arg0: float) -> List[SimplePrimitive]: ...
    def transform(self) -> SimplePrimitive: ...
    @property
    def centroid(self) -> Tuple[float,float,float]: ...
    @property
    def type(self) -> str: ...