
class EntityBase(dict):
    def __init__(self, *args, **kwargs):
        super(EntityBase, self).__init__(*args, **kwargs)
        self.__dict__ = self
