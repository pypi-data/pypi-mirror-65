# -*- coding: utf-8 -*-
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import grpc
from google.protobuf.any_pb2 import Any as pbAny

from .models import Category, Item, Library, StandardLibraryException, FieldTypeEnum
from .schema import CategoryObjectSchema as COSch
from .schema import CategoryPbmSchema as CPSch
from .schema import ItemObjectSchema as IOSch
from .schema import ItemPbSchema as IPSch
from .schema import LibraryObjectSchema as LOSch
from .schema import LibraryPbSchema as LPSch
from .. import common_pb2 as c_pb
from .. import standardLibraryService_pb2 as s_pb
from .. import standardLibraryService_pb2_grpc as s_grpc


class StandardLibraryServiceGRPCClient(object):

    def __init__(self, endpoint: str, src: str):
        self._endpoint = endpoint
        self._src = src

    @contextmanager
    def _stub(self):
        with grpc.insecure_channel(self._endpoint) as channel:
            stub = s_grpc.StandardLibraryServiceStub(channel)
            try:
                yield stub
            except grpc.RpcError as e:
                raise StandardLibraryException(str(e))

    def _pack(self, request: Any) -> c_pb.RequestMessage:
        data = pbAny()
        data.Pack(request)
        return c_pb.RequestMessage(src=self._src, data=data)

    def _unpack(self, response: c_pb.ResponseMessage, data_type: Optional[type]) -> Any:
        if response.code != 0:
            raise StandardLibraryException("{} {}".format(str(response.code), response.msg))
        if data_type is None:
            return None
        msg = data_type()
        response.data.Unpack(msg)
        return msg

    def get_all_categories_and_libraries(self) -> List[Category]:
        with self._stub() as stub:
            response = stub.GetAllLibraries(self._pack(c_pb.Empty()))
            cps = self._unpack(response, s_pb.GetAllLibrariesResponse).categories
            cos = COSch(many=True).load(CPSch(many=True).dump(cps))
            return cos

    def add_categories(self, operator: str, categories: List[Category]):
        with self._stub() as stub:
            cps = CPSch(many=True).load(COSch(many=True).dump(categories))
            response = stub.AddCategories(self._pack(s_pb.AddCategoriesRequest(operator=operator, categories=cps)))
            self._unpack(response, None)

    def order_categories(self, operator: str, category_uuids: List[str]):
        with self._stub() as stub:
            response = stub.OrderCategories(self._pack(s_pb.OrderCategoriesRequest(operator=operator, category_uuids=category_uuids)))
            self._unpack(response, None)

    # TODO SDK更新分类
    def update_categories(self, operator: str, category_changes: Dict[str, Category]):
        raise NotImplementedError("update_categories not implemented yet.")

    def delete_categories(self, operator: str, uuid_in: List[str]):
        with self._stub() as stub:
            response = stub.DeleteCategories(self._pack(s_pb.DeleteCategoriesRequest(operator=operator, uuids=uuid_in)))
            self._unpack(response, None)

    def get_libraries(self, uuid_in: List[str]) -> List[Library]:
        with self._stub() as stub:
            response = stub.GetLibraries(self._pack(s_pb.GetLibrariesRequest(uuid_in=uuid_in)))
            lps = self._unpack(response, s_pb.GetLibrariesResponse).libraries
            los = LOSch(many=True).load(LPSch(many=True).dump(lps))
            return los

    def add_libraries(self, operator: str, category_uuid: str, libraries: List[Library]):
        with self._stub() as stub:
            lps = LPSch(many=True).load(LOSch(many=True).dump(libraries))
            response = stub.AddLibraries(self._pack(s_pb.AddLibrariesRequest(operator=operator, category_uuid=category_uuid, libraries=lps)))
            self._unpack(response, None)

    def order_libraries(self, operator: str, category_uuid: str, library_uuids: List[str]):
        with self._stub() as stub:
            response = stub.OrderLibraries(self._pack(s_pb.OrderLibrariesRequest(operator=operator, category_uuid=category_uuid, library_uuids=library_uuids)))
            self._unpack(response, None)

    def move_libraries(self, operator: str, category_uuid: str, library_uuids: List[str]):
        with self._stub() as stub:
            response = stub.MoverLibraries(self._pack(s_pb.MoveLibrariesRequest(operator=operator, category_uuid=category_uuid, library_uuids=library_uuids)))
            self._unpack(response, None)

    # TODO SDK更新库
    def update_libraries(self, operator: str, library_changes: Dict[str, Library]):
        raise NotImplementedError("update_libraries not implemented yet.")

    def delete_libraries(self, operator: str, uuids: List[str]):
        with self._stub() as stub:
            response = stub.DeleteLibraries(self._pack(s_pb.DeleteLibrariesRequest(operator=operator, uuids=uuids)))
            self._unpack(response, None)

    def get_items(self, library_uuid: str, uuid_in: List[str] = [], item_keyword: str = "", offset: int = 0, limit: int = 10, reverse: bool = False, order_by: str = "uuid", load_refs: bool = False) -> (Library, List[Item], int):
        with self._stub() as stub:
            response = stub.GetItems(self._pack(s_pb.GetItemsRequest(library_uuid=library_uuid, uuid_in=uuid_in, keyword=item_keyword, offset=offset, limit=limit, reverse=reverse, order_by=order_by, load_refs=load_refs)))
            msg = self._unpack(response, s_pb.GetItemsResponse)
            lp = msg.library
            ips = msg.items
            lo = LOSch().load(LPSch().dump(lp))
            ios = IOSch(many=True, unknown="exclude").load(IPSch(many=True).dump(ips))
            if load_refs:
                for io in ios:
                    for val in io.values:
                        if val["type"] == FieldTypeEnum.items:
                            for idx in range(len(val["value"])):
                                item = s_pb.Item()
                                item.ParseFromString(bytes.fromhex(val["value"][idx]))
                                val["value"][idx] = IOSch(unknown="exclude").load(IPSch().dump(item))
            cnt = msg.total
            return lo, ios, cnt

    def add_items(self, operator: str, library_uuid: str, items: List[Item]):
        with self._stub() as stub:
            ips = IPSch(many=True).load(IOSch(many=True).dump(items))
            response = stub.AddItems(self._pack(s_pb.AddItemsRequest(operator=operator, library_uuid=library_uuid, items=ips)))
            self._unpack(response, None)

    # TODO SDK更新条目
    def update_items(self, operator: str, library_uuid: str, item_changes: Dict[str, Library]):
        raise NotImplementedError("update_items not implemented yet.")

    def delete_items(self, operator: str, library_uuid: str, uuids: List[str]):
        with self._stub() as stub:
            response = stub.DeleteItems(self._pack(s_pb.DeleteItemsRequest(operator=operator, library_uuid=library_uuid, uuids=uuids)))
            self._unpack(response, None)
