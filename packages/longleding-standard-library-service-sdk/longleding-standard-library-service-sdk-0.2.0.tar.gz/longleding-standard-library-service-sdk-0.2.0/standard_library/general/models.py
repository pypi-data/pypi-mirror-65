# -*- coding: utf-8 -*-
import enum
from datetime import datetime
from typing import Any, Dict, List, Optional

import attr


class StandardLibraryException(Exception):
    pass


class FieldTypeEnum(enum.IntEnum):
    unknown = 0
    string = 1
    boolean = 2
    integer = 3
    float = 4
    enum = 5
    text = 6
    libraries = 7
    items = 8
    # TODO Range类型


class LibraryLockStatusEnum(enum.IntEnum):
    unlocked = 0
    schema_locked = 1
    data_locked = 2


@attr.s
class BaseItem(object):
    uuid: str = attr.ib(default="")
    operator: str = attr.ib(default="")
    create_time: Optional[datetime] = attr.ib(default=None)
    update_time: Optional[datetime] = attr.ib(default=None)


@attr.s
class Item(BaseItem):
    """
    Sample values
    [
      {
        "field": "数据集名称",
        "type": FieldTypeEnum.string
        "value": "入院记录"
      },
      ...
    ]
    """
    values: List[Dict[str, Any]] = attr.ib(default=[])


@attr.s
class Field(object):
    name: str = attr.ib(default="")
    type: FieldTypeEnum = attr.ib(default=FieldTypeEnum.unknown)
    enum_set: List[str] = attr.ib(default=[])


@attr.s
class Library(BaseItem):
    name: str = attr.ib(default="")
    lock: LibraryLockStatusEnum = attr.ib(default=LibraryLockStatusEnum.unlocked)
    fields: Optional[List[Field]] = attr.ib(default=[])


@attr.s
class Category(BaseItem):
    name: str = attr.ib(default="")
    libraries: Optional[List[Library]] = attr.ib(default=[])
