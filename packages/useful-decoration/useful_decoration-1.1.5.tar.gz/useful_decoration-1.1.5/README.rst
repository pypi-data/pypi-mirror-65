Useful-decoration
===================
Description
-----------

I wrote some decorators that are commonly used in my daily work. And I gave an example if the decorator is often used.

Installing
-----------

Install and update using `pip`_:


.. code:: python

    pip install  useful-decoration

Simples
________

.. code-block:: python


    from useful_decoration.decorations import element_mapping


    class Person:

        def __init__(self, name):
            self.name = name

        @element_mapping(factor_name="factor")
        def calculate(self):
            return 10


    if __name__ == '__main__':
        p = Person(name='frank')

        print(p.calculate())  # {'factor': 10}


Contributes
___________

Welcome, you can join this repo to  enhance this repo  together. you can pull request to me.
please don't  hesitate to contact with  me if you have any questions .


Links
_____

* pypi address https://pypi.org/project/useful-decoration/

* Documentation: https://useful-decoration.readthedocs.io/en/latest/


.. _pip: https://pip.pypa.io/en/stable/quickstart/
