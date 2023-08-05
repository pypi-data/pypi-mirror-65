# -*- coding: utf-8 -*-
import json
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from marshmallow import EXCLUDE, Schema, fields, post_dump, post_load

from .models import Category, Field, FieldTypeEnum, Item, Library, LibraryLockStatusEnum
from .. import standardLibraryService_pb2 as s_pb


# Field Define
class JsonStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None or value == "":
            return {}
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None or value == "":
            return '{}'
        return json.dumps(value)


class PbDateTimeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        ct = value.ToDatetime().isoformat()
        return ct if ct != '1970-01-01T00:00:00' else None

    def _deserialize(self, value, attr, data, **kwargs):
        p = Timestamp()
        d = datetime.fromisoformat(value)
        p.FromDatetime(d)
        return p


class FieldTypeEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return int(value) if value is not None else 0

    def _deserialize(self, value, attr, data, **kwargs):
        return FieldTypeEnum(value) if value is not None else FieldTypeEnum.unknown


class LibraryLockStatusEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return int(value) if value is not None else 0

    def _deserialize(self, value, attr, data, **kwargs):
        return LibraryLockStatusEnum(value) if value is not None else LibraryLockStatusEnum.unlocked


# Base Schema
class _BSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    @post_dump
    def clean_missing(self, data, **kwargs):
        ret = data.copy()
        for key in filter(lambda key: data[key] is None, data):
            del ret[key]
        return ret


# Uniq Object Schema
class _UOSchema(_BSchema):
    uuid = fields.Str(default="", missing="")
    operator = fields.Str(default="", missing="")
    create_time = fields.DateTime(default=None, missing=None)
    update_time = fields.DateTime(default=None, missing=None)


# Uniq Pb Schema
class _UPSchema(_UOSchema):
    create_time = PbDateTimeField(default=None, missing=None)
    update_time = PbDateTimeField(default=None, missing=None)


# Item Schema
class ItemObjectSchema(_UOSchema):
    values = fields.List(fields.Dict, default=[], missing=[])

    @post_load
    def make_object(self, data, **kwargs):
        return Item(**data)


class ItemPbSchema(_UPSchema):
    values = fields.List(JsonStringField, default=[], missing=[])

    @post_load
    def make_pb(self, data, **kwargs):
        return s_pb.Item(**data)


# Field Schema
class FieldObjectSchema(_BSchema):
    name = fields.Str(default="", missing="")
    type = fields.Field(default=FieldTypeEnum.unknown, missing=FieldTypeEnum.unknown)
    enum_set = fields.List(fields.String, default=[], missing=[])

    @post_load
    def make_object(self, data, **kwargs):
        return Field(**data)


class FieldPbSchema(_BSchema):
    name = fields.Str(default="", missing="")
    type = FieldTypeEnumField(default=FieldTypeEnum.unknown, missing=0)
    enum_set = fields.List(fields.String, default=[], missing=[])

    @post_load
    def make_pb(self, data, **kwargs):
        return s_pb.Field(**data)


# Library Schema
class LibraryObjectSchema(_UOSchema):
    name = fields.Str(default="", missing="")
    lock = LibraryLockStatusEnumField(default=LibraryLockStatusEnum.unlocked, missing=0)
    fields = fields.List(fields.Nested(FieldObjectSchema), default=[], missing=[])

    @post_load
    def make_object(self, data, **kwargs):
        return Library(**data)


class LibraryPbSchema(_UPSchema):
    name = fields.Str(default="", missing="")
    lock = LibraryLockStatusEnumField(default=LibraryLockStatusEnum.unlocked, missing=0)
    fields = fields.List(fields.Nested(FieldPbSchema), default=[], missing=[])

    @post_load
    def make_pb(self, data, **kwargs):
        return s_pb.Library(**data)


# Category Schema
class CategoryObjectSchema(_UOSchema):
    name = fields.Str(default="", missing="")
    libraries = fields.List(fields.Nested(LibraryObjectSchema), default=[], missing=[])

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryPbmSchema(_UPSchema):
    name = fields.Str(default="", missing="")
    libraries = fields.List(fields.Nested(LibraryPbSchema), default=[], missing=[])

    @post_load
    def make_pb(self, data, **kwargs):
        return s_pb.Category(**data)
