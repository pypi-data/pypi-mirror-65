# from .gstorm import mainClass
from . import cli
from . import helpers
from .GraphQLType import GraphQLType
from .QueryBuilder import QueryBuilder
from .MutationBuilder import MutationBuilder

# * Package name:
name = 'gstorm'
# * required here for pypi upload exceptions:
__version__ = "0.2.5"
