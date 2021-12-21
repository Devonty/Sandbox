class CircleList(list):

    def __getitem__(self, item):
        item = item % len(self)
        return super().__getitem__(item)
