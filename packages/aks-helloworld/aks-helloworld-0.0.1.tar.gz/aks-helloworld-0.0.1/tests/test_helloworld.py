from helloworld import say_hello

def test_helloworld_no_param():
    assert say_hello() == "Hello, World!"


def test_helloworld_with_param():
    assert say_hello('Tokyo') == "Hello, Tokyo!"
