Make data merging Pythonic
===============================================================================

**joiner** is a tiny library for merging groups of data in a sql-join-like way.

Example
----------------------------------------------------------------------------

Here is a quick example to get a feeling of **joiner**.

```python

def test():
    hobbys = [
        {'first_name': 'A', 'last_name': 'yao', 'hobby': 'pingpong'},
        {'first_name': 'A', 'last_name': 'bob', 'hobby': 'shopping'},
        {'first_name': 'B', 'last_name': 'bob', 'hobby': 'shopping'},
    ]
    ages = [
        {'first_name': 'A', 'last_name': 'yao', 'age': 18},
        {'first_name': 'A', 'last_name': 'bob', 'age': 20},
    ]
    heights = [
        {'first_name': 'A', 'last_name': 'yao', 'height': 170},
    ]

    hobbys = Group(hobbys)
    ages = Group(ages, cols=Cols('age', age='how old'))
    heights = Group(heights, cols=Cols('height'))
    results = selectfrom(hobbys).leftjoin(ages).on(hobbys.first_name == ages.first_name, hobbys.last_name == ages.last_name)\
        .leftjoin(heights).on(hobbys.first_name == heights.first_name, hobbys.last_name == heights.last_name)\
        .get()
    for result in results:
        print(result)


test()
"""
{'first_name': 'A', 'last_name': 'yao', 'age': 18, 'how old': 18, 'height': 170, 'hobby': 'pingpong'}
{'first_name': 'A', 'last_name': 'bob', 'age': 20, 'how old': 20, 'height': None, 'hobby': 'shopping'}
{'first_name': 'B', 'last_name': 'bob', 'age': None, 'how old': None, 'height': None, 'hobby': 'shopping'}
"""

```

Installation
-------------------------------------------------------------------------------

Use `pip <http://pip-installer.org>` or easy_install::

    pip install joiner-python

Alternatively, you can just drop ``joiner.py`` file into your project—it is
self-contained.
