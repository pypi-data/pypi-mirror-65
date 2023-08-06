from .mixins import BaseNestedSets as BaseNestedSets
from typing import Callable
from sqlalchemy.orm.session import sessionmaker

mptt_sessionmaker: Callable[[sessionmaker], sessionmaker]
