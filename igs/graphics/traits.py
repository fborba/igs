import copy


class Clonable:
    def clone(self):
        return copy.deepcopy(self)


class Drawable:
    def draw(self, painter):
        NotImplemented
