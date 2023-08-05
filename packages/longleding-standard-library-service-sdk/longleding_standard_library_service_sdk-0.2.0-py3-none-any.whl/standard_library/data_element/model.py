# -*- coding: utf-8 -*-
from typing import List

import attr

from ..general.models import BaseItem


@attr.s
class DataValueType(BaseItem):
    """
    数据类型
    """
    name_cn: str = attr.ib(default="", metadata={"field": "中文名称"})
    name_en: str = attr.ib(default="", metadata={"field": "英文名称"})


@attr.s
class MeasureUnit(BaseItem):
    """
    单位
    """
    name_cn: str = attr.ib(default="", metadata={"field": "中文名称"})
    name_en: str = attr.ib(default="", metadata={"field": "英文名称"})


@attr.s
class DataElementConcept(BaseItem):
    """
    数据元概念
    """
    name_cn: str = attr.ib(default="", metadata={"field": "中文名称"})
    name_en: str = attr.ib(default="", metadata={"field": "英文名称"})
    definition: str = attr.ib(default="", metadata={"field": "定义"})


@attr.s
class DataElementTerm(BaseItem):
    """
    数据元术语
    """
    name_cn: str = attr.ib(default="", metadata={"field": "中文名称"})
    name_en: str = attr.ib(default="", metadata={"field": "英文名称"})
    concept: DataElementConcept = attr.ib(default=None, metadata={"field": "数据元概念", "type": DataElementConcept})
    type: List = attr.ib(default=[], metadata={"field": "数据类型", "type": DataValueType})
    unit: List = attr.ib(default=[], metadata={"field": "单位", "type": MeasureUnit})
