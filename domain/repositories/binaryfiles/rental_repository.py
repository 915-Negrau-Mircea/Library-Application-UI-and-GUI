import pickle

from domain.repositories.inmemory.rental_repository import RentalRepository


class RentalBinaryRepository(RentalRepository):
    def __init__(self, filename):
        RentalRepository.__init__(self)
        self.__filename = filename
        self.set_next_rental_id()

    def __read_all_from_file(self):
        self._rentals = []
        with open(self.__filename, "rb") as file:
            while True:
                try:
                    rental = pickle.load(file)
                except EOFError:
                    rental = None
                if rental is not None:
                    self._rentals.append(rental)
                else:
                    break

    def __write_all_to_file(self):
        with open(self.__filename, "wb") as file:
            for rental in self._rentals:
                pickle.dump(rental, file)

    def add_rental(self, rental):
        self.__read_all_from_file()
        RentalRepository.add_rental(self, rental)
        self.__write_all_to_file()

    def remove_rental_by_index(self, index):
        self.__read_all_from_file()
        RentalRepository.remove_rental_by_index(self, index)
        self.__write_all_to_file()

    def update_rental_return_by_index(self, index, new_date):
        self.__read_all_from_file()
        RentalRepository.update_rental_return_by_index(self, index, new_date)
        self.__write_all_to_file()

    def get_all_rentals(self):
        self.__read_all_from_file()
        return RentalRepository.get_all_rentals(self)

    def set_next_rental_id(self):
        maximum_id = 0
        for rental in self.get_all_rentals():
            maximum_id = max(maximum_id, rental.id)
        self._last_rental_id = maximum_id