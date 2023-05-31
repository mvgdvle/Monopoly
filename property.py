from field import Field


class Property(Field):
    def __init__(self, name, position, owner=None, price_field=0, tax=0):
        super().__init__(name, position)
        self.owner = owner
        self.price_field = price_field
        self.tax = tax

    def change_owner(self, new_owner):
        self.owner = new_owner

    def get_owner(self):
        return self.owner

    def get_price_field(self):
        return self.price_field
