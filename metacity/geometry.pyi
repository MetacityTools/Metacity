from typing import List, Tuple

from typing import overload

class BaseModel:
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> Model: ...
    @property
    def type(self) -> str: ...

class Interval:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: int, arg1: int) -> None: ...
    def can_contain(self, arg0: MultiTimePoint) -> bool: ...
    def deserialize(self, arg0: json) -> None: ...
    def insert(self, arg0: MultiTimePoint, arg1: int) -> None: ...
    def serialize(self) -> json: ...
    @property
    def start_time(self) -> int: ...

class LegoBuilder:
    def __init__(self) -> None: ...
    def build_heightmap(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: int) -> None: ...
    def insert_model(self, arg0: TriangularMesh) -> None: ...
    def lego_to_png(self, arg0: str) -> None: ...
    def legofy(self, arg0: int) -> json: ...

class Model(BaseModel):
    def __init__(self) -> None: ...
    def add_attribute(self, arg0: str, arg1: int) -> None: ...
    def copy(self) -> Model: ...
    def deserialize(self, arg0: json) -> None: ...
    def join(self, arg0: Model) -> None: ...
    def map(self, arg0: TriangularMesh) -> None: ...
    def serialize(self) -> json: ...
    def serialize_stream(self) -> json: ...
    def shift(self, arg0: float, arg1: float, arg2: float) -> None: ...
    def slice_to_grid(self, arg0: float) -> List[Model]: ...
    def to_obj(self, arg0: str, arg1: int) -> int: ...
    def transform(self) -> Model: ...
    @property
    def bounding_box(self) -> Tuple[Tuple[float,float,float],Tuple[float,float,float]]: ...
    @property
    def centroid(self) -> Tuple[float,float,float]: ...
    @property
    def type(self) -> str: ...

class MultiLine(BaseModel):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_l2(self, arg0: List[float]) -> None: ...
    def push_l3(self, arg0: List[float]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> Model: ...
    @property
    def type(self) -> str: ...

class MultiPoint(BaseModel):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_p2(self, arg0: List[float]) -> None: ...
    def push_p3(self, arg0: List[float]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> Model: ...
    @property
    def type(self) -> str: ...

class MultiPolygon(BaseModel):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def push_p2(self, arg0: List[List[float]]) -> None: ...
    def push_p3(self, arg0: List[List[float]]) -> None: ...
    def serialize(self) -> json: ...
    def transform(self) -> Model: ...
    @property
    def type(self) -> str: ...

class MultiTimePoint(BaseModel):
    def __init__(self) -> None: ...
    def deserialize(self, arg0: json) -> None: ...
    def serialize(self) -> json: ...
    def set_points_from_b64(self, arg0: str) -> None: ...
    def set_start_time(self, arg0: int) -> None: ...
    def transform(self) -> Model: ...
    @property
    def empty(self) -> bool: ...
    @property
    def end_time(self) -> int: ...
    @property
    def start_time(self) -> int: ...
    @property
    def type(self) -> str: ...

class PointCloud(Model):
    def __init__(self) -> None: ...
    def copy(self) -> Model: ...
    def map(self, arg0: TriangularMesh) -> None: ...
    def slice_to_grid(self, arg0: float) -> List[Model]: ...
    def to_obj(self, arg0: str, arg1: int) -> int: ...
    @property
    def type(self) -> str: ...

class SegmentCloud(Model):
    def __init__(self) -> None: ...
    def add_attribute(self, arg0: str, arg1: int) -> None: ...
    def copy(self) -> Model: ...
    def map(self, arg0: TriangularMesh) -> None: ...
    def slice_to_grid(self, arg0: float) -> List[Model]: ...
    def to_obj(self, arg0: str, arg1: int) -> int: ...
    @property
    def type(self) -> str: ...

class TriangularMesh(Model):
    def __init__(self) -> None: ...
    def copy(self) -> Model: ...
    def map(self, arg0: TriangularMesh) -> None: ...
    def slice_to_grid(self, arg0: float) -> List[Model]: ...
    def to_obj(self, arg0: str, arg1: int) -> int: ...
    @property
    def type(self) -> str: ...
