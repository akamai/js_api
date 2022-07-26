import random


class MyModel(object):
    """
    This model can do anything. We just do one function as an example
    """

    @staticmethod
    def test_js():
        """

        Mock function that returns a random value:

        """
        complex_compute = 1 + 1
        assert complex_compute <= 3
        proba = random.random()

        return proba
