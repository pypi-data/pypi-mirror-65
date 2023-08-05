# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipromise', 'ipromise.test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipromise',
    'version': '1.7',
    'description': 'A Python base class that provides various decorators for specifying promises relating to inheritance.',
    'long_description': '=========\nI Promise\n=========\n.. image:: https://badge.fury.io/py/ipromise.svg\n    :target: https://badge.fury.io/py/ipromise\n\nThis repository provides a Python base class, and various decorators for specifying promises relating to inheritance.\nIt provides three inheritance patterns:\n\n* implementing,\n* overriding, and\n* augmenting.\n\nBase class\n==========\nChecking promises depends on inheritance from the base class ``AbstractBaseClass``.  Unlike the standard library\'s similar class ``abc.ABCMeta``, ``AbstractBaseClass`` does not bring in any metaclasses.  This is thanks to Python 3.6\'s PEP 487, which added ``__init_subclass__``.\n\nImplementing\n============\n*Implementing* is the pattern whereby an inheriting class\'s method implements an abstract method from a base class method.\nIt is declared using the decorators:\n\n* ``abc.abstractmethod`` from the standard library, and\n* ``implements``, which indicates that a method implements an abstract method in a base class\n\nFor example:\n\n.. code-block:: python\n\n    class HasAbstractMethod(AbstractBaseClass):\n\n        @abstractmethod\n        def f(self):\n            raise NotImplementedError\n\n\n    class ImplementsAbstractMethod(HasAbstractMethod):\n\n        @implements(HasAbstractMethod)\n        def f(self):\n            return 0\n\nOverriding\n==========\n*Overriding* is the pattern whereby an inheriting class\'s method replaces the implementation of a base class method.\nIt is declared using the decorator ``overrides``, which marks the overriding method.\n\nAn overriding method could call super, but does not have to:\n\n.. code-block:: python\n\n    class HasRegularMethod(AbstractBaseClass):\n\n        def f(self):\n            return 1\n\n\n    class OverridesRegularMethod(HasRegularMethod):\n\n        @overrides(HasRegularMethod)\n        def f(self):\n            return 2\n\nAugmenting\n==========\n*Augmenting* is a special case of *overriding* whereby the inheriting class\'s method not only *overrides* the base class method, but *extends* its functionality.\nThis means that it must delegate to *super* in all code paths.\nThis pattern is typical in multiple inheritance.\n\nWe hope that Python linters will be able to check for the super call.\n\nAugmenting is declared using two decorators:\n\n* ``augments`` indicates that this method must call super within its definition and thus augments the behavior of the base class method, and\n* ``must_agugment`` indicates that child classes that define this method must decorate their method overriddes with ``augments``.\n\nFor example:\n\n.. code-block:: python\n\n    class HasMustAugmentMethod(AbstractBaseClass):\n\n        @must_augment\n        def f(self):\n            # must_augment prevents this behavior from being lost.\n            self.times_f_called += 1\n            return 0\n\n\n    class AugmentsMethod(HasMustAugmentMethod):\n\n        @augments(HasMustAugmentMethod)\n        def f(self, extra=0, **kwargs):\n            return super().f(**kwargs) + extra\n\n\n    class AugmentsMethodFurther(AugmentsMethod):\n\n        @augments(HasMustAugmentMethod)\n        def f(self, **kwargs):\n            print("f has been called")\n            return super().f(**kwargs)\n',
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NeilGirdhar/ipromise',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
