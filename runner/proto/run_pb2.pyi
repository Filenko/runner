from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadInfo(_message.Message):
    __slots__ = ["free_containers", "cpu_load"]
    FREE_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    CPU_LOAD_FIELD_NUMBER: _ClassVar[int]
    free_containers: int
    cpu_load: int
    def __init__(self, free_containers: _Optional[int] = ..., cpu_load: _Optional[int] = ...) -> None: ...

class CodeWithTests(_message.Message):
    __slots__ = ["id", "program_code", "tests"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_CODE_FIELD_NUMBER: _ClassVar[int]
    TESTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    program_code: bytes
    tests: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., program_code: _Optional[bytes] = ..., tests: _Optional[_Iterable[str]] = ...) -> None: ...

class CheckResults(_message.Message):
    __slots__ = ["id", "result", "load_info"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LOAD_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    result: _containers.RepeatedScalarFieldContainer[str]
    load_info: LoadInfo
    def __init__(self, id: _Optional[str] = ..., result: _Optional[_Iterable[str]] = ..., load_info: _Optional[_Union[LoadInfo, _Mapping]] = ...) -> None: ...
