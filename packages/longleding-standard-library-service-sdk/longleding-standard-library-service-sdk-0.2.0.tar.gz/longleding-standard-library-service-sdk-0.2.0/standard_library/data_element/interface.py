# -*- coding: utf-8 -*-
from typing import List

from .model import DataElementConcept, DataElementTerm
from ..general.interface import param_check, get_items
from ..general.models import Library


@param_check
def get_data_element_concept(*, uuid_in: List = [], keyword: str = "", offset: int = 0, limit: int = 10, reverse: bool = False, order_by: str = "uuid") -> (Library, List[DataElementConcept], int):
    return get_items(DataElementConcept, "YL.LIBRARY.DATA_ELEMENT_CONCEPT", uuid_in=uuid_in, keyword=keyword, offset=offset, limit=limit, reverse=reverse, order_by=order_by)


@param_check
def get_data_element_term(*, uuid_in: List = [], keyword: str = "", offset: int = 0, limit: int = 10, reverse: bool = False, order_by: str = "uuid", load_refs: bool = False) -> (Library, List[DataElementTerm], int):
    lo, ios, cnt = get_items(DataElementTerm, "YL.LIBRARY.DATA_ELEMENT_TERM", **locals())
    return lo, ios, cnt
