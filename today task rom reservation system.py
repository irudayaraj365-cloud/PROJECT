# Room Reservation System using OOP Concepts

class Room:
    def __init__(self, room_number, room_type, price_per_night, is_available=True):
        self.__room_number = room_number
        self.__room_type = room_type
        self.__price_per_night = price_per_night
        self.__is_available = is_available

    # Getters and Setters
    def get_room_number(self):
        return self.__room_number

    def get_room_type(self):
        return self.__room_type

    def get_price_per_night(self):
        return self.__price_per_night

    def is_room_available(self):
        return self.__is_available

    def set_availability(self, status):
        self.__is_available = status

    # Methods
    def display_details(self):
        print(f"Room {self.__room_number} ({self.__room_type}) - Rs.{self.__price_per_night:.2f}/night - {'Available' if self.__is_available else 'Booked'}")

    def book_room(self):
        if self.__is_available:
            self.__is_available = False
            print("Room booked successfully.")
        else:
            print("Room is already booked.")

    def release_room(self):
        self.__is_available = True
        print("Room is now available.")

    def __str__(self):
        return f"Room {self.__room_number} ({self.__room_type})"


class DeluxeRoom(Room):
    def __init__(self, room_number, price_per_night, amenities):
        super().__init__(room_number, "Deluxe", price_per_night)
        self.__amenities = amenities

    def get_amenities(self):
        return self.__amenities

    def display_details(self):
        super().display_details()
        print("Amenities:", ", ".join(self.__amenities))

    def __str__(self):
        return super().__str__() + f" with amenities: {', '.join(self.__amenities)}"


class StandardRoom(Room):
    def __init__(self, room_number, price_per_night, view):
        super().__init__(room_number, "Standard", price_per_night)
        self.__view = view

    def get_view(self):
        return self.__view

    def display_details(self):
        super().display_details()
        print("View:", self.__view)

    def __str__(self):
        return super().__str__() + f" with view: {self.__view}"


class ReservationSystem:
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        for r in self.rooms:
            if r.get_room_number() == room.get_room_number():
                print("Room with this number already exists.")
                return
        self.rooms.append(room)
        print("Room added successfully.")

    def remove_room(self, room_number):
        self.rooms = [room for room in self.rooms if room.get_room_number() != room_number]
        print("Room removed successfully if it existed.")

    def view_available_rooms(self):
        print("\nAvailable Rooms:")
        for room in self.rooms:
            if room.is_room_available():
                room.display_details()

    def make_reservation(self, room_number):
        for room in self.rooms:
            if room.get_room_number() == room_number:
                room.book_room()
                return
        print("Room not found.")

    def cancel_reservation(self, room_number):
        for room in self.rooms:
            if room.get_room_number() == room_number:
                room.release_room()
                return
        print("Room not found.")

    def display_all_rooms(self):
        print("\nAll Rooms:")
        for room in self.rooms:
            room.display_details()


# Simulated Console-based Menu for Non-interactive Environments
def simulate_menu(system):
    # Simulated operations
    system.add_room(StandardRoom("101", 2500.0, "City"))
    system.add_room(DeluxeRoom("201", 4500.0, ["TV", "WiFi", "Mini Bar"]))
    system.display_all_rooms()
    system.view_available_rooms()
    system.make_reservation("101")
    system.cancel_reservation("101")
    system.remove_room("999")  # Room doesn't exist
    system.remove_room("101")
    system.display_all_rooms()


if __name__ == '__main__':
    system = ReservationSystem()
    simulate_menu(system)
