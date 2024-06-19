# -*- coding:utf-8 -*-
import dataclasses
from typing import Optional, Any, Callable
from .types import optional, number
from .utils import _recursive_repr, _format_type
from .validator import Validator


class Field:
    """字段"""

    """字段名"""
    name: str

    """JsonSchema标题"""
    title: optional[str]

    """注解"""
    annotation: optional[type[Any]]

    """验证器"""
    validator: optional[Validator]

    """默认值"""
    default: Any

    """默认工厂"""
    default_factory: optional[Callable]

    """是否必填"""
    required: optional[bool]

    """是否初始化"""
    init: optional[bool]

    """是否显示"""
    repr: optional[bool]

    """别名"""
    alias: optional[str]

    """验证别名"""
    val_alias: optional[str]

    """序列化别名"""
    ser_alias: optional[str]

    """最小"""
    min: optional[number]

    """最大"""
    max: optional[number]

    """最短"""
    min_length: optional[int]

    """最长"""
    max_length: optional[int]

    """描述"""
    description: optional[str]

    """排除序列化"""
    exclude: optional[bool]

    """是否抛弃"""
    deprecated: optional[bool]

    """是否冻结"""
    frozen: optional[bool]

    """"""
    init_var: optional[bool]

    """验证器参数"""
    val_extra: optional[dict]

    """序列化器参数"""
    ser_extra: optional[dict]

    __slots__ = (
        'name',
        'title',
        'annotation',
        'validator',
        'default',
        'default_factory',
        'required',
        'init',
        'repr',
        'alias',
        'val_alias',
        'ser_alias',
        'min',
        'max',
        'min_length',
        'max_length',
        'description',
        'exclude',
        'deprecated',
        'frozen',
        'init_var',
        'val_extra',
        'ser_extra',
        '_field_type'
    )

    def __init__(self, **kwargs):
        self.init = True
        self.repr = True
        [self.__setattr__(k, v) for k, v in kwargs.items() if k in self.__slots__]

        if self.default is dataclasses.MISSING:
            self.default = None

        if self.default is not None and self.default_factory is not None:
            raise ValueError(f'不能同时指定 default 和 default_factory')

    def set_annotation(self, annotation):
        if annotation is Optional:
            raise RuntimeError("Optional 必须添加内部类型")
        self.annotation = annotation

    @_recursive_repr
    def __repr__(self):
        return (f"Field(name={self.name!r}, "
                f"annotation={_format_type(self.annotation)}, "
                f"default={self.default!r}, "
                f"default_factory={self.default_factory!r}, "
                f"required={self.required!r}, "
                f"init={self.init!r}, "
                f"repr={self.repr!r}, "
                f"description={self.description!r})")

    def get_default_value(self):
        for d in dir(self):
            print(getattr(self, d))
        # value = None if self.default is None else self.default
        # if value is None:
        #     value = self.default_factory() if self.default_factory is not None else value
        # return value


# This function is used instead of exposing Field creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
def field(*, default=None, default_factory=None, required=False, **kwargs) -> Field:
    """Return an object to identify dataclass fields.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a field's value.  If init
    is True, the field will be a parameter to the class's __init__()
    function.  If repr is True, the field will be included in the
    object's repr().  If hash is True, the field will be included in
    the object's hash().  If compare is True, the field will be used
    in comparison functions.  metadata, if specified, must be a
    mapping which is stored but not otherwise examined by dataclass.

    It is an error to specify both default and default_factory.
    """
    return Field(default=default, default_factory=default_factory, required=required, **kwargs)
