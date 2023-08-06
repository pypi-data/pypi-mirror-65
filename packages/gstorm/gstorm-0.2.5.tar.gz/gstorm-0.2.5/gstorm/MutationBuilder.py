from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import inflect
from pygqlc import GraphQLClient
from gstorm.BaseGraphQLType import BaseGraphQLType
from gstorm.enums import QueryType
from gstorm.helpers.str_handling import remove_capital, contains_digits
from gstorm.helpers.date_helpers import get_utc_date, get_iso8601_str
from gstorm.helpers.gql import setup_gql

'''

class C(object):
    def __init__(self):
        self._x = None
    @property
    def x(self):
        """I'm the 'x' property."""
        print('Hippity hoppity, someone looked at my property!')
        return self._x
    @x.setter
    def x(self, value):
        print('setting x value!')
        self._x = value
    @x.deleter
    def x(self):
        print('deleted x value!')
        del self._x

CREATE, UPDATE, UPSERT, DELETE
# SIMPLE
mutation {
  createTank(
    name: 'L101'
    type: 'Gobierno'
    capacity: 1000
  ){
    successful
    messages{
      field
      message
    }
    result{
      id
      name
      type
      capacity
      insertedAt
      updatedAt
    }
  }
}
# PARAMS
query {
  tanks (
    filter: {
      capacity: 10
      name: "hola"
      after: {
        attribute: INSERTED_AT
        date: "2020-01-01T00:00:00Z"
      }
    }
    orderBy: {
      desc: ID
    }
    limit: 10
  ){
    id
    name
    capacity
    insertedAt
    updatedAt
  }
}
'''

class MutationBuilder():
  pass