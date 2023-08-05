# -*- coding: utf-8 -*-
import inspect
from typing import List
from typing import get_type_hints

import attr

from .grpc_client import StandardLibraryServiceGRPCClient
from .models import Category, Library, FieldTypeEnum, Item, BaseItem

_client: StandardLibraryServiceGRPCClient


def param_check(func):
    def wrapper(*args, **kwargs):
        global _client
        assert _client is not None, "standard library service sdk must be init first"
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        for i, v in enumerate(args):
            p = params[i]
            assert p.annotation is inspect.Parameter.empty or isinstance(v, p.annotation), "{} must be {}.".format(p.name, str(p.annotation))
        return func(*args, **kwargs)

    return wrapper


def init_service(endpoint: str, src: str) -> None:
    global _client
    assert type(endpoint) == str, "endpoint must be a str"
    assert type(src) == str, "src must be a str"
    _client = StandardLibraryServiceGRPCClient(endpoint=endpoint, src=src)


# TODO 更新分类；更新库；更新、删除条目 11个接口尚未实现


@param_check
def get_all_categories_and_libraries() -> List[Category]:
    return _client.get_all_categories_and_libraries()


@param_check
def add_categories(operator: str, categories: List):
    return _client.add_categories(**locals())


@param_check
def order_categories(operator: str, category_uuids: List):
    return _client.order_categories(**locals())


@param_check
def delete_categories(operator: str, uuid_in: List):
    return _client.delete_categories(**locals())


@param_check
def get_libraries(uuid_in: List) -> List[Library]:
    return _client.get_libraries(**locals())


@param_check
def add_libraries(operator: str, category_uuid: str, libraries: List):
    return _client.add_libraries(**locals())


@param_check
def order_libraries(operator: str, category_uuid: str, library_uuids: List):
    return _client.order_libraries(**locals())


@param_check
def move_libraries(operator: str, category_uuid: str, library_uuids: List):
    return _client.move_libraries(**locals())


@param_check
def delete_libraries(operator: str, uuids: List):
    return _client.delete_libraries(**locals())


@param_check
def add_items(operator: str, library_uuid: str, items: List):
    return _client.add_items(**locals())


@param_check
def delete_items(operator: str, library_uuid: str, uuids: List[str]):
    return _client.delete_items(**locals())


def convert_item(item_type: type, items: List[Item]) -> List:
    its = []
    for io in items:
        it = item_type(
            uuid=io.uuid,
            operator=io.operator,
            create_time=io.create_time,
            update_time=io.update_time,
        )
        for k, t in get_type_hints(item_type).items():
            for d in io.values:
                fd_meta = getattr(attr.fields(item_type), k).metadata
                if 'field' in fd_meta and fd_meta['field'] == d['field']:
                    if d["type"] == FieldTypeEnum.items:
                        if len(d['value']) == 0:
                            if not isinstance(t, list):
                                setattr(it, k, None)
                        else:
                            if not isinstance(d['value'][0], BaseItem):
                                setattr(it, k, d['value'])
                            else:
                                mt = fd_meta["type"]
                                objs = convert_item(mt, d['value'])
                                if not isinstance(t, list):
                                    setattr(it, k, objs[0])
                                else:
                                    setattr(it, k, objs)
                    else:
                        setattr(it, k, t(d['value']))
        its.append(it)
    return its


def get_items(item_type: type, library_uuid: str, *, uuid_in: List = [], keyword: str = "", offset: int = 0, limit: int = 10, reverse: bool = False, order_by: str = "uuid", load_refs: bool = False) -> (Library, List, int):
    lo, ios, cnt = _client.get_items(library_uuid=library_uuid, uuid_in=uuid_in, item_keyword=keyword, offset=offset, limit=limit, reverse=reverse, order_by=order_by, load_refs=load_refs)
    its = convert_item(item_type, ios)
    return lo, its, cnt
