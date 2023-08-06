import inspect

class Container:

    def __init__(self):
        self.bindings = {}
        self.shared = {}

    @staticmethod
    def ensure_key_string(key):
        allowed = (int, str, bool, float)
        if not isinstance(key, allowed):
            key = key.__module__ + '.' + key.__name__
        return str(key)

    # Bind a resolver in biggu_container
    def bind(self, name, resolver, shared = False):
        self.bindings[name] = {
            'resolver': resolver,
            'shared': shared,
        }

    # Register an instance of class in biggu_container
    def instance(self, name, instance):
        self.shared[self.ensure_key_string(name)] = instance

    def singleton(self, name, resolver):
        self.bind(self.ensure_key_string(name), resolver, True)

    @staticmethod
    def import_class(namespace):
        print("RESOLVE CLASS NAME", namespace)
        class_data = namespace.split(".")
        submodules_list = class_data[0:-1]
        class_name = class_data[-1]

        module = __import__('.'.join(submodules_list), fromlist=[class_name])
        return getattr(module, class_name)

    # Build instances with dependencies
    def build(self, _class, arguments = None):
        _info = inspect.getfullargspec(_class.__init__)
        class_arguments = _info.args[1:]

        if not len(class_arguments):
            return _class()

        if arguments is None:
            arguments = {}

        dependencies = {}
        for key in class_arguments:
            if key in arguments:
                dependencies[key] = arguments[key]
                continue

            if key in _info.annotations and  inspect.isclass(_info.annotations[key]):
                dependencies[key] = self.build(_info.annotations[key])
            else:
                if _info.defaults is None:
                    raise Exception('Provide the value of the parameter [%s]' % key)

                last_required_index = len(class_arguments) - len(_info.defaults)
                defaults = class_arguments[last_required_index:]
                for index in range(len(defaults)):
                    name = defaults[index]
                    dependencies[name] = _info.defaults[index]


        return _class(**dependencies)

    # Make a instance using a key name in biggu_container
    def make(self, name, arguments = None):
        name = self.ensure_key_string(name)
        if name in self.shared:
            return self.shared[name]

        if name in self.bindings:
            resolver = self.bindings[name]['resolver']
            shared = self.bindings[name]['shared']
        else:
            resolver = name
            shared = False

        if callable(resolver):
            _object = resolver(self)
        else:
            if type(resolver) != str:
                _object = resolver
            else:
                _class = Container.import_class(resolver)
                _object = self.build(_class, arguments)

        if shared :
            self.instance(name, _object)

        return _object