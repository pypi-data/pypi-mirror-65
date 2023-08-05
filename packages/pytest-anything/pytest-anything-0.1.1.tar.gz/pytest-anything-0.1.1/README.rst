Anything and Something fixtures for pytest
==========================================

If you ever had to ignore a certain part of an assertion, you would end up with
this.

.. code-block:: python

    import pytest


    @pytest.mark.parametrize("obj", ["string", 123, 123.1, True, False, None, object()])
    def test_anything(obj, Anything):
        assert obj == Anything


    @pytest.mark.parametrize("obj", ["string", 123, 123.1, True, False, object()])
    def test_something(obj, Something):
        assert obj == Something


    def test_nothing(Something):
        obj = None
        assert obj != Something


    def test_anything_repr(Anything):
        assert repr(Anything) == "Anything"


    def test_something_repr(Something):
        assert repr(Something) == "Something"
