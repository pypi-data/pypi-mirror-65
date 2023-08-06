import unittest
from biggu_container import Container


class FooBar:
    pass

class Foo:
    pass

class Bar:
    def __init__(self, foo: Foo):
        self.foo = foo

class Baz:
    def __init__(self, bar: Bar, foobar: FooBar):
        self.bar = bar
        self.foobar = foobar

class Dummy:
    def __init__(self, client_id, key):
        self.client_id = client_id
        self.key = key
        pass

class Defaults:
    def __init__(self, client_id, key = None, text = 'text'):
        self.client_id = client_id
        self.key = key
        self.text = text
        pass


class ContainerTest(unittest.TestCase):
    def test_ensure_key_name_as_string(self):
        container = Container()
        self.assertEqual(container.ensure_key_string(Foo), 'test.test_container.Foo')
        self.assertEqual(container.ensure_key_string("key"), 'key')
        self.assertEqual(container.ensure_key_string(1), '1')
        self.assertEqual(container.ensure_key_string(2.5), '2.5')

    def test_bind_from_lambda(self):
        container = Container()
        container.bind('key', lambda cont: 'Object')
        self.assertEqual('Object', container.make('key'))

    def test_bind_instance(self):
        container = Container()
        mock = Foo()
        container.instance('key', mock)
        self.assertEqual(mock, container.make('key'))

    def test_import_class(self):
        self.assertEqual(Container.import_class('test.test_container.Foo'), Foo)

    def test_bind_for_class_name(self):
        container = Container()
        container.bind('key', 'test.test_container.Foo')
        self.assertIsInstance(container.make('key'), Foo)

    def test_bind_for_class_name_with_dependencies(self):
        container = Container()
        container.bind('key', 'test.test_container.Baz')
        self.assertIsInstance(container.make('key'), Baz)

    def test_bind_for_class_name_with_arguments(self):
        container = Container()
        self.assertIsInstance(container.make('test.test_container.Dummy', {"client_id": "1", "key": "QWERTY1"}), Dummy)

    def test_bind_for_class_name_with_default_arguments(self):
        container = Container()
        self.assertIsInstance(container.make('test.test_container.Defaults', {"client_id": "1"}), Defaults)


    def test_singleton_instance(self):
        container = Container()
        container.singleton('singleton', 'test.test_container.Foo')
        container.singleton('singleton2', 'test.test_container.FooBar')
        self.assertEqual(container.make('singleton'), container.make('singleton'))
        self.assertEqual(container.make('singleton2'), container.make('singleton2'))

    def test_register_instance_using_class_types(self):
        container = Container()
        container.instance(Foo, Foo())
        container.instance(FooBar, FooBar())
        self.assertIsInstance(container.make('test.test_container.Foo'), Foo)
        self.assertIsInstance(container.make('test.test_container.FooBar'), FooBar)

    def test_register_singleton_using_class_types(self):
        container = Container()
        container.singleton(Foo, Foo())
        container.singleton(FooBar, FooBar())
        self.assertEqual(container.make('test.test_container.Foo'), container.make('test.test_container.Foo'))
        self.assertEqual(container.make('test.test_container.FooBar'), container.make('test.test_container.FooBar'))


if __name__ == '__main__':
    unittest.main()
