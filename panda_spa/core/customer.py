class Customer:
    _id_counter: int = 1

    def __init__(self, name: str, species: str):
        self.customer_id = Customer._id_counter
        Customer._id_counter += 1
        self.name = name
        self.species = species
