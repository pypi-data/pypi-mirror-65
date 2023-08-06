suffix_trees
============

|ci| |codecov|

Python implementation of Suffix Trees and Generalized Suffix Trees. Also
provided methods with typcal applications of STrees and GSTrees.

Installation
~~~~~~~~~~~~

.. code:: bash

   pip install suffix-trees

Usage
~~~~~

.. code:: python

   from suffix_trees import STree

   # Suffix-Tree example.
   st = STree.STree("abcdefghab")
   print(st.find("abc")) # 0
   print(st.find_all("ab")) # [0, 8]

   # Generalized Suffix-Tree example.
   a = ["xxxabcxxx", "adsaabc", "ytysabcrew", "qqqabcqw", "aaabc"]
   st = STree.STree(a)
   print(st.lcs()) # "abc"

.. |ci| image:: https://github.com/ptrus/suffix-trees/workflows/ci/badge.svg
.. |codecov| image:: https://codecov.io/gh/ptrus/suffix-trees/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ptrus/suffix-trees
