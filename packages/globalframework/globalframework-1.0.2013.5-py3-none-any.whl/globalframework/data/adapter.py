class ConnectionAdapter:
    _initialised = False

    def __init__(self, entity, **adapting_methods):
        self.entity = entity

        for key, value in adapting_methods.items():
            func = getattr(self.entity, value)
            self.__setattr__(key, func)
        self._initialised = True


    def __getattr__(self, attr):
        return getattr(self.entity, attr)


    def __setattr__(self, key, value):
        # Set attributes during initialisation
        if not self._initialised:
            super().__setattr__(key, value)
        else:
        # Set attributes on entity after initialisation
            setattr(self.entity, key, value)
