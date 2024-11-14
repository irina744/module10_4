from queue import Queue
from threading import Thread
import time
from random import randint

class Table:
    def __init__(self, number):
        self.number = number
        self.is_occupied = False
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables: Table):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            available_table = next((t for t in self.tables if not t.is_occupied), None)
            if available_table:
                available_table.is_occupied = True
                available_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {available_table.number}")
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(t.is_occupied for t in self.tables):
            for table in self.tables:
                if table.is_occupied and not table.guest.is_alive():
                    guest_name = table.guest.name
                    table_number = table.number
                    table.is_occupied = False
                    table.guest = None
                    print(f"{guest_name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table_number} свободен")

                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.is_occupied = True
                        table.guest = new_guest
                        new_guest.start()
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table_number}")




# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()


