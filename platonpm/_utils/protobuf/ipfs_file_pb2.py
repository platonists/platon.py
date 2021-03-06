# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file.proto

import sys

from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pb2,
    message as _message,
    reflection as _reflection,
    symbol_database as _symbol_database,
)

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="file.proto",
    package="",
    syntax="proto2",
    serialized_pb=_b(
        '\n\nfile.proto"\xa1\x01\n\x04\x44\x61ta\x12\x1c\n\x04Type\x18\x01 \x02(\x0e\x32\x0e.Data.DataType\x12\x0c\n\x04\x44\x61ta\x18\x02 \x01(\x0c\x12\x10\n\x08\x66ilesize\x18\x03 \x01(\x04\x12\x12\n\nblocksizes\x18\x04 \x03(\x04"G\n\x08\x44\x61taType\x12\x07\n\x03Raw\x10\x00\x12\r\n\tDirectory\x10\x01\x12\x08\n\x04\x46ile\x10\x02\x12\x0c\n\x08Metadata\x10\x03\x12\x0b\n\x07Symlink\x10\x04"3\n\x06PBLink\x12\x0c\n\x04Hash\x18\x01 \x01(\x0c\x12\x0c\n\x04Name\x18\x02 \x01(\t\x12\r\n\x05Tsize\x18\x03 \x01(\x04".\n\x06PBNode\x12\x16\n\x05Links\x18\x02 \x03(\x0b\x32\x07.PBLink\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\x0c'
    ),
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


_DATA_DATATYPE = _descriptor.EnumDescriptor(
    name="DataType",
    full_name="Data.DataType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="Raw", index=0, number=0, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="Directory", index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="File", index=2, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="Metadata", index=3, number=3, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="Symlink", index=4, number=4, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=105,
    serialized_end=176,
)
_sym_db.RegisterEnumDescriptor(_DATA_DATATYPE)


_DATA = _descriptor.Descriptor(
    name="Data",
    full_name="Data",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="Type",
            full_name="Data.Type",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=2,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="Data",
            full_name="Data.Data",
            index=1,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="filesize",
            full_name="Data.filesize",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="blocksizes",
            full_name="Data.blocksizes",
            index=3,
            number=4,
            type=4,
            cpp_type=4,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_DATA_DATATYPE],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=15,
    serialized_end=176,
)


_PBLINK = _descriptor.Descriptor(
    name="PBLink",
    full_name="PBLink",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="Hash",
            full_name="PBLink.Hash",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="Name",
            full_name="PBLink.Name",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="Tsize",
            full_name="PBLink.Tsize",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=178,
    serialized_end=229,
)


_PBNODE = _descriptor.Descriptor(
    name="PBNode",
    full_name="PBNode",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="Links",
            full_name="PBNode.Links",
            index=0,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="Data",
            full_name="PBNode.Data",
            index=1,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=231,
    serialized_end=277,
)

_DATA.fields_by_name["Type"].enum_type = _DATA_DATATYPE
_DATA_DATATYPE.containing_type = _DATA
_PBNODE.fields_by_name["Links"].message_type = _PBLINK
DESCRIPTOR.message_types_by_name["Data"] = _DATA
DESCRIPTOR.message_types_by_name["PBLink"] = _PBLINK
DESCRIPTOR.message_types_by_name["PBNode"] = _PBNODE

Data = _reflection.GeneratedProtocolMessageType(
    "Data",
    (_message.Message,),
    dict(
        DESCRIPTOR=_DATA,
        __module__="file_pb2"
        # @@protoc_insertion_point(class_scope:Data)
    ),
)
_sym_db.RegisterMessage(Data)

PBLink = _reflection.GeneratedProtocolMessageType(
    "PBLink",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PBLINK,
        __module__="file_pb2"
        # @@protoc_insertion_point(class_scope:PBLink)
    ),
)
_sym_db.RegisterMessage(PBLink)

PBNode = _reflection.GeneratedProtocolMessageType(
    "PBNode",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PBNODE,
        __module__="file_pb2"
        # @@protoc_insertion_point(class_scope:PBNode)
    ),
)
_sym_db.RegisterMessage(PBNode)


# @@protoc_insertion_point(module_scope)
