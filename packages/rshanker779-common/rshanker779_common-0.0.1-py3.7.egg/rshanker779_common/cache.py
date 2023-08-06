import logging
from functools import partial
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CachingStrategy:
    def __init__(self, attr_name: str, load_method: Callable[[], Any]):
        """        Holds the information about how to cache an attribute               
        :param attr_name: The name of the attribute that will be created in the class       
        :param load_method: How to retreive the item to be cached"""
        self.attr_name = attr_name
        self.load_method = load_method


class Cache:
    def __init__(self, *strategies: CachingStrategy):
        """Cache implementation for things that are slow to load, e.g. files               
        :param strategies: One or more strategies to implement. Will create an attribute            
            matching the attr_name in the Strategy
        """
        for strategy in strategies:
            attr_name = strategy.attr_name
            hidden_attr_name = "__" + strategy.attr_name
            setattr(self, hidden_attr_name, None)

            def loading_method(
                strategy: CachingStrategy, hidden_attr_name: str, self: Cache
            ) -> Any:
                if getattr(self, hidden_attr_name) is None:
                    loaded_value = strategy.load_method()
                    setattr(self, hidden_attr_name, loaded_value)
                return getattr(self, hidden_attr_name)

            setattr(
                self.__class__,
                attr_name,
                property(partial(loading_method, strategy, hidden_attr_name)),
            )
