Welcome to The ArcadePlus Library!
===================================

ArcadePlus is an easy-to-learn Python library for creating 2D video games.
It is ideal for beginning programmers, or programmers who want to create
2D games without learning a complex framework.

ArcadePlus is built on top of Pyglet and OpenGL.

The ArcadePlus Python library is made by George Shao.
ArcadePlus was forked from Arcade, a Python library made by Paul Vincent Craven.
ArcadePlus is a simpler, more performant Python graphics library than Arcade.

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat
    :target: http://makeapullrequest.com
    :alt: Pull Requests Welcome

.. image:: https://pepy.tech/badge/arcadeplus
    :target: https://pepy.tech/project/arcadeplus
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/arcadeplus
    :alt: PyPI - License

How to Install
##############

Type ``pip install arcadeplus`` into your terminal.


Performance Comparison
######################

As seen in the graph below, the ArcadePlus Python library has much better performance than the Arcade Python library.

.. image:: https://github.com/GeorgeShao/arcadeplus/blob/master/arcadeplus/examples/perf_test/stress_test_comparison_results.svg
    :alt: ArcadePlus vs Arcade - Python Library Performance Comparison Chart


How to Convert Existing Arcade Code to ArcadePlus Code
######################################################
1. Replace any imports such as ``import arcade`` with ``import arcadeplus``
2. Use your IDE's built-in find function to replace all instances of ``arcade.`` with ``arcadeplus.``
