import pydash as __ 
from typing import Optional, List, _GenericAlias
from datetime import datetime
from gstorm.helpers.gql import setup_gql
from pprint import pprint
import attr
from dataclasses import dataclass, field
from gstorm.QueryBuilder import QueryBuilder
from gstorm.enums import QueryType
from gstorm.BaseGraphQLType import BaseGraphQLType
from gstorm.helpers.date_helpers import get_local_date, iso8601_to_local_date

def nint(value):
  if value is None:
    return None
  elif type(value) == str:
    return int(value)
  elif type(value) == int:
    return value
  else:
    raise Exception(f"Cannot cast {type(value)} to nullable int")

@attr.s
class GraphQLType(BaseGraphQLType):
  '''Base class for Graphql types,
  has one python's dataclass field per graphql type.
  Plus a __type field with the Type's metadata (opt-out, etc)
  '''
  # __metadata__: str = attr.ib(factory=dict) # attr.ib(default={'opt-out': {}}) # ! MAY BE REQUIRED LATER FOR @opt-out, etc
  __sync__: bool = attr.ib(repr=False, default=False)
  __errors__: List[dict] = attr.ib(repr=False, factory=list)
  id: Optional[int] = attr.ib(default=None, converter=nint, metadata={'unique': {}})
  insertedAt: datetime = attr.ib(repr=False, factory=lambda: get_local_date(datetime.now()), converter=iso8601_to_local_date, metadata={'readonly': True})
  updatedAt: datetime = attr.ib(repr=False, factory=lambda: get_local_date(datetime.now()), converter=iso8601_to_local_date, metadata={'readonly': True})
  
  def __getitem__(self, name):
    return self.__getattribute__(name)
  @classmethod
  def get_field(cls, name):
    return attr.fields_dict(cls).get(name)
  @classmethod
  def get_fields(cls):
    return attr.fields_dict(cls)
  @classmethod
  def get_base_fields(cls):
    list_fields = [
      name
      for name, field in attr.fields_dict(cls).items()
      if not field.type == _GenericAlias # if not type List
        and not GraphQLType in (
        __.get(field, 'type.__mro__')
        or __.get(field, 'type.__dict__.__args__')
        )
        and not name.startswith('_')
    ]
    return list_fields
  @classmethod
  def get_list_fields(cls):
    list_fields = [
      name
      for name, field in attr.fields_dict(cls).items()
      if field.type == _GenericAlias # if not type List
    ]
    return list_fields
  @classmethod
  def get_object_fields(cls):
    obj_fields = [
      name
      for name, field in attr.fields_dict(cls).items()
      if GraphQLType in (
        __.get(field, 'type.__mro__')
        or __.get(field, 'type.__dict__.__args__')
      )
    ]
    return obj_fields
  @classmethod
  def get_unique_fields(cls):
    return [
      name
      for name, field in attr.fields_dict(cls).items()
      if 'unique' in field.metadata
    ]
  @classmethod
  def get_metadata(cls, field_name):
    field = attr.fields_dict(cls)[field_name]
    return field.metadata
  def create(self):
    pass
  def load(self):
    raise NotImplementedError('Child class should implement load method')
  @classmethod
  def query(cls):
    return QueryBuilder(_kind=cls)
  @classmethod
  def query_one(cls):
    return QueryBuilder(cls, QueryType.SINGULAR)
  def is_sync(self):
    return self.__sync__
  def has_errors(self):
    return len(self.__errors__) > 0
  def get_errors(self):
    return self.__errors__
  # ! method aliases
  # query
  q = query
  qm = query
  qp = query # query plural
  # query_one
  q1 = query_one
  qs = query_one # query singular
