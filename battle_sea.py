import random
from random import randint


# класс Точки
class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.check = self.checking_value()

    # Вывод значения точки
    def __repr__(self):
        return f'({self.row}, {self.col})'

    # Сравнение значений точки на равенство
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # Сложение значений точки
    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)

    # Вычитание значений точки
    def __sub__(self, other):
        return Point(self.row - other.row, self.col - other.col)

    # Проверка значений точки на вхождений в игровое поле
    def checking_value(self):
        return True if 0 <= self.row <= 5 and 0 <= self.col <= 5 else False


# класс Корабля
class Ship:
    def __init__(self, length=1, align=0):
        self.length = length
        self.align = align
        self.life = self.length
        self.ship_point = self.create_ship_point()
        self.ship_point_around = self.create_ship_point_around()
        self.ship_point_value = []
        self.ship_point_around_value = []

    # Вывод значеник корабля
    def __repr__(self):
        return f'{self.ship_point_value}'

    # Создание списка возможных точек корабля без привязки к игровому полю
    def create_ship_point(self):
        ship_point = []
        if self.align == 0:
            for _ in range(self.length):
                ship_point.append(Point(0, _))
        else:
            for _ in range(self.length):
                ship_point.append(Point(_, 0))
        return ship_point

    # Создание списка возможных точек вокруг коробля без привязки к игровому полю
    def create_ship_point_around(self):
        ship_point_around = []
        if self.align == 0:
            for i in [-1, 1]:
                for j in range(-1, (self.length + 1)):
                    ship_point_around.append(Point(i, j))
            ship_point_around.append(Point(0, -1))
            ship_point_around.append(Point(0, self.length))
        else:
            for i in [-1, 1]:
                for j in range(-1, (self.length + 1)):
                    ship_point_around.append(Point(j, i))
            ship_point_around.append(Point(-1, 0))
            ship_point_around.append(Point(self.length, 0))
        return ship_point_around




# класс Набор кораблей
class Collection:
    def __init__(self, auto=0):
        self.roll = [3, 2, 2, 1, 1, 1, 1]
        self.auto = auto
        self.value = self.create_value()
        self.list_ships = self.create_list_ship()

    # Генератор всех возможных точек на поле
    @staticmethod
    def create_value():
        value = []
        for row in range(6):
            for col in range(6):
                value.append(Point(row, col))
        return value

    # Запрос значения точки, в зависимости от auto в ручном или автоматичеком режиме
    def ask_point(self):
        if self.auto == 0 and len(self.value) != 0:
            point = random.choice(self.value)
            return point
        elif self.auto == 1 and len(self.value) != 0:
            point = Point(int(input('Введите координату "X": ')) - 1, int(input('Введите координату "Y": ')) - 1)
            return point if point in self.value else False
        else:
            return False

    # создаем корабль
    def create_ship(self, length):
        align = randint(0, 1) if self.auto == 0 else int(input('Положение корабля(0 - гор., 1 - вер.): '))
        point = self.ask_point()
        _ = Ship(length, align)
        if point:
            for ship_point in _.ship_point:
                if (point.row <= (6 - length)) and _.align == 1:
                    _.ship_point_value.append(point + ship_point)
                elif not (point.row <= (6 - length)) and _.align == 1:
                    _.ship_point_value.append(point - ship_point)
                elif (point.col <= (6 - length)) and _.align == 0:
                    _.ship_point_value.append(point + ship_point)
                elif not (point.col <= (6 - length)) and _.align == 0:
                    _.ship_point_value.append(point - ship_point)
            if self.check_ship_point_value(_):
                self.create_ship_point_around_value(_)
                return _
            else:
                return False
        else:
            return False

    # Проверка наличия точек в наборе
    def check_ship_point_value(self, ship):
        count = 0
        for value in ship.ship_point_value:
            if value in self.value:
                count += 1
        if count == ship.length:
            for val in ship.ship_point_value:
                self.value.remove(val)
            return True
        else:
            return False

    # создаем значение точек вокруг коробля
    def create_ship_point_around_value(self, ship):
        point = ship.ship_point_value[0]
        length = ship.length
        for ship_point_around in ship.ship_point_around:
            if (point.row <= (6 - length)) and (ship.align == 1) and (point + ship_point_around).checking_value():
                ship.ship_point_around_value.append(point + ship_point_around)
            if (point.row > (6 - length)) and (ship.align == 1) and (point - ship_point_around).checking_value():
                ship.ship_point_around_value.append(point - ship_point_around)
            if (point.col <= (6 - length)) and (ship.align == 0) and (point + ship_point_around).checking_value():
                ship.ship_point_around_value.append(point + ship_point_around)
            if (point.col > (6 - length)) and (ship.align == 0) and (point - ship_point_around).checking_value():
                ship.ship_point_around_value.append(point - ship_point_around)
        for _ in ship.ship_point_around_value:
            if _ in self.value:
                self.value.remove(_)

    # создаем список кораблей
    def create_list_ship(self):
        attempt = 0
        while attempt < 2000:
            list_ships = []
            for length in self.roll:
                _ = self.create_ship(length)
                if _:
                    list_ships.append(_)
            if len(list_ships) == len(self.roll):
                return list_ships
            else:
                self.value = self.create_value()
                attempt += 1
        return []


# класс игрового поля
class BattleField:
    def __init__(self, auto=0):
        self.field = self.create_field()
        self.auto = auto
        self.collection = self.create_collection()
        self.busy = []

    # Начальное поле
    @staticmethod
    def create_field():
        field = []
        for row in range(6):
            field.append([])
            for col in range(6):
                field[row].append('0')
        return field

    # создание коллекци
    def create_collection(self):
        collection = Collection(self.auto)
        if len(collection.list_ships) == len(collection.roll):
            return collection
        else:
            return False

    # расстановка обозначений кораблей на поле
    def ship_to_field(self):
        if self.collection:
            for ship in self.collection.list_ships:
                for point in ship.ship_point_value:
                    self.field[point.row][point.col] = '■'
                    self.busy.append(point)
        return False

    # удар по полю
    def hit_in_field(self, hit):
        if hit not in self.busy:
            print('Мимо!')
            self.field[hit.row][hit.col] = 'T'
            return False
        else:
            for ship in self.collection.list_ships:
                for point in ship.ship_point_value:
                    if hit == point:
                        ship.life -= 1
                        self.field[hit.row][hit.col] = 'X'
                        self.busy.remove(hit)
                        if ship.life != 0:
                            print('Попал!')
                            return 1
                        else:
                            print('Убит!')
                            return 0

    # Временный вывод поля на печать
    def print_field(self):
        print('   ', end='')
        for axis in range(6):
            print(f'{axis:>3}', end='')
        print()
        for row in range(6):
            print(f'{row:^3}|', end='')
            for col in range(6):
                print(f'{self.field[row][col]:^3}', end='')
            print()



# класс Игрока
class Player:
    def __init__(self, auto=0):
        self.name = ''
        self.auto = auto
        self.hits_value = self.create_hits_value()
        self.field = BattleField(self.auto)
        self.state = self.player_state()
        self.around_hit = []

    # Создание списка возможных выстрелов
    @staticmethod
    def create_hits_value():
        hits_value = []
        for i in range(6):
            for j in range(6):
                hits_value.append(Point(i, j))
        return hits_value

    # список выстрелов вокруг
    def create_around_hit(self, hit):
        around = []
        around_hit = []
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                around.append(Point(row, col))
        around.remove(Point(0, 0))
        for point in around:
            _ = hit + point
            if _ in self.hits_value:
                around_hit.append(_)
                self.hits_value.remove(_)
        return around_hit

    # проверка состояния
    def player_state(self):
        if self.field.collection:
            self.field.ship_to_field()
            return True
        else:
            return False

    # выстрел
    def auto_hit(self):
        print(self.around_hit)
        if len(self.around_hit) == 0:
            print('Берем из hits_value')
            hit = random.choice(self.hits_value)
            print(f'Удар по точке: {hit}')
            self.hits_value.remove(hit)
            return hit
        else:
            print('Берем из around_hit')
            hit = random.choice(self.around_hit)
            print(f'Удар по точке: {hit}')
            self.around_hit.remove(hit)
            return hit

    def del_hit(self, other_field, hit):
        for ship in other_field.collection.list_ships:
            if hit in ship.ship_point_value:
                for point in ship.ship_point_around_value:
                    if point in self.hits_value:
                        self.hits_value.remove(point)

    def step_player(self, other_field):
        #hit = Point(int(input('x')), int(input('y')))
        hit = self.auto_hit()
        check_hit = other_field.hit_in_field(hit)
        if check_hit == 0:
            self.hits_value += self.around_hit
            self.del_hit(other_field, hit)
            self.around_hit = []
        if check_hit == 1:
            self.around_hit += self.create_around_hit(hit)
        if not check_hit:
            return False


n1 = Player()
print(n1.hits_value[:18])
print(n1.hits_value[18:])
# n1.field.print_field()
for i in range(20):
    n1.step_player(n1.field)
    print(n1.hits_value[:18])
    print(n1.hits_value[18:])
    print(f'Удары вокруг {n1.around_hit}')
    n1.field.print_field()
    input('Enter')














