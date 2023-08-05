# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: descarteslabs/common/proto/typespec/typespec.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='descarteslabs/common/proto/typespec/typespec.proto',
  package='descarteslabs.workflows',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n2descarteslabs/common/proto/typespec/typespec.proto\x12\x17\x64\x65scarteslabs.workflows\"\xac\x02\n\x08Typespec\x12\x36\n\x04prim\x18\x01 \x01(\x0b\x32\".descarteslabs.workflows.PrimitiveR\x04prim\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type\x12.\n\x03map\x18\x03 \x01(\x0b\x32\x1c.descarteslabs.workflows.MapR\x03map\x12:\n\x04\x63omp\x18\x04 \x01(\x0b\x32&.descarteslabs.workflows.CompositeTypeR\x04\x63omp\x12\x19\n\x08has_prim\x18\x05 \x01(\x08R\x07hasPrim\x12\x19\n\x08has_type\x18\x06 \x01(\x08R\x07hasType\x12\x17\n\x07has_map\x18\x07 \x01(\x08R\x06hasMap\x12\x19\n\x08has_comp\x18\x08 \x01(\x08R\x07hasComp\"\xd3\x01\n\tPrimitive\x12\x11\n\x04int_\x18\x01 \x01(\x05R\x03int\x12\x15\n\x06\x66loat_\x18\x02 \x01(\x02R\x05\x66loat\x12\x13\n\x05\x62ool_\x18\x03 \x01(\x08R\x04\x62ool\x12\x17\n\x07string_\x18\x04 \x01(\tR\x06string\x12\x17\n\x07has_int\x18\x05 \x01(\x08R\x06hasInt\x12\x1b\n\thas_float\x18\x06 \x01(\x08R\x08hasFloat\x12\x19\n\x08has_bool\x18\x07 \x01(\x08R\x07hasBool\x12\x1d\n\nhas_string\x18\x08 \x01(\x08R\thasString\"y\n\rMapFieldEntry\x12\x33\n\x03key\x18\x01 \x01(\x0b\x32!.descarteslabs.workflows.TypespecR\x03key\x12\x33\n\x03val\x18\x02 \x01(\x0b\x32!.descarteslabs.workflows.TypespecR\x03val\"C\n\x03Map\x12<\n\x05items\x18\x01 \x03(\x0b\x32&.descarteslabs.workflows.MapFieldEntryR\x05items\"^\n\rCompositeType\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x39\n\x06params\x18\x02 \x03(\x0b\x32!.descarteslabs.workflows.TypespecR\x06paramsb\x06proto3'
)




_TYPESPEC = _descriptor.Descriptor(
  name='Typespec',
  full_name='descarteslabs.workflows.Typespec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='prim', full_name='descarteslabs.workflows.Typespec.prim', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='prim', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='descarteslabs.workflows.Typespec.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='type', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map', full_name='descarteslabs.workflows.Typespec.map', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='map', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='comp', full_name='descarteslabs.workflows.Typespec.comp', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='comp', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_prim', full_name='descarteslabs.workflows.Typespec.has_prim', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasPrim', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_type', full_name='descarteslabs.workflows.Typespec.has_type', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasType', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_map', full_name='descarteslabs.workflows.Typespec.has_map', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasMap', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_comp', full_name='descarteslabs.workflows.Typespec.has_comp', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasComp', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=380,
)


_PRIMITIVE = _descriptor.Descriptor(
  name='Primitive',
  full_name='descarteslabs.workflows.Primitive',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int_', full_name='descarteslabs.workflows.Primitive.int_', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='int', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_', full_name='descarteslabs.workflows.Primitive.float_', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='float', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_', full_name='descarteslabs.workflows.Primitive.bool_', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='bool', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_', full_name='descarteslabs.workflows.Primitive.string_', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='string', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_int', full_name='descarteslabs.workflows.Primitive.has_int', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasInt', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_float', full_name='descarteslabs.workflows.Primitive.has_float', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasFloat', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_bool', full_name='descarteslabs.workflows.Primitive.has_bool', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasBool', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_string', full_name='descarteslabs.workflows.Primitive.has_string', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hasString', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=383,
  serialized_end=594,
)


_MAPFIELDENTRY = _descriptor.Descriptor(
  name='MapFieldEntry',
  full_name='descarteslabs.workflows.MapFieldEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='descarteslabs.workflows.MapFieldEntry.key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='val', full_name='descarteslabs.workflows.MapFieldEntry.val', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='val', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=596,
  serialized_end=717,
)


_MAP = _descriptor.Descriptor(
  name='Map',
  full_name='descarteslabs.workflows.Map',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='descarteslabs.workflows.Map.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='items', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=719,
  serialized_end=786,
)


_COMPOSITETYPE = _descriptor.Descriptor(
  name='CompositeType',
  full_name='descarteslabs.workflows.CompositeType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='descarteslabs.workflows.CompositeType.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='type', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='descarteslabs.workflows.CompositeType.params', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='params', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=788,
  serialized_end=882,
)

_TYPESPEC.fields_by_name['prim'].message_type = _PRIMITIVE
_TYPESPEC.fields_by_name['map'].message_type = _MAP
_TYPESPEC.fields_by_name['comp'].message_type = _COMPOSITETYPE
_MAPFIELDENTRY.fields_by_name['key'].message_type = _TYPESPEC
_MAPFIELDENTRY.fields_by_name['val'].message_type = _TYPESPEC
_MAP.fields_by_name['items'].message_type = _MAPFIELDENTRY
_COMPOSITETYPE.fields_by_name['params'].message_type = _TYPESPEC
DESCRIPTOR.message_types_by_name['Typespec'] = _TYPESPEC
DESCRIPTOR.message_types_by_name['Primitive'] = _PRIMITIVE
DESCRIPTOR.message_types_by_name['MapFieldEntry'] = _MAPFIELDENTRY
DESCRIPTOR.message_types_by_name['Map'] = _MAP
DESCRIPTOR.message_types_by_name['CompositeType'] = _COMPOSITETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Typespec = _reflection.GeneratedProtocolMessageType('Typespec', (_message.Message,), {
  'DESCRIPTOR' : _TYPESPEC,
  '__module__' : 'descarteslabs.common.proto.typespec.typespec_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Typespec)
  })
_sym_db.RegisterMessage(Typespec)

Primitive = _reflection.GeneratedProtocolMessageType('Primitive', (_message.Message,), {
  'DESCRIPTOR' : _PRIMITIVE,
  '__module__' : 'descarteslabs.common.proto.typespec.typespec_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Primitive)
  })
_sym_db.RegisterMessage(Primitive)

MapFieldEntry = _reflection.GeneratedProtocolMessageType('MapFieldEntry', (_message.Message,), {
  'DESCRIPTOR' : _MAPFIELDENTRY,
  '__module__' : 'descarteslabs.common.proto.typespec.typespec_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.MapFieldEntry)
  })
_sym_db.RegisterMessage(MapFieldEntry)

Map = _reflection.GeneratedProtocolMessageType('Map', (_message.Message,), {
  'DESCRIPTOR' : _MAP,
  '__module__' : 'descarteslabs.common.proto.typespec.typespec_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Map)
  })
_sym_db.RegisterMessage(Map)

CompositeType = _reflection.GeneratedProtocolMessageType('CompositeType', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITETYPE,
  '__module__' : 'descarteslabs.common.proto.typespec.typespec_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.CompositeType)
  })
_sym_db.RegisterMessage(CompositeType)


# @@protoc_insertion_point(module_scope)
