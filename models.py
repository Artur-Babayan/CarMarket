import json
from json import JSONEncoder
from datetime import datetime



class Person:
    def __init__(self, first_name, last_name, city):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city

class Buyer(Person):
    def __init__(self, first_name, last_name, city, money):
        super().__init__(first_name, last_name, city)
        self.money = money
        self.spent_money = 0
        self.bought_cars = []

    def buy_car(self, car):
        if car.seller.check_car_availability(car):
            if self.money >= car.price:
                self.money -= car.price
                self.spent_money += car.price
                self.bought_cars.append(car)
                car.seller.sell_car(car, self)
                print(f"Car '{car.model}' bought successfully.")
            else:
                print("Insufficient funds to buy the car.")
        else:
            print("The car is not available in the seller's car park.")

    def return_car(self, car):
        if car in self.bought_cars:
            self.bought_cars.remove(car)
            self.money += car.price
            car.seller.return_car(car, self)
            print(f"Car '{car.model}' returned successfully.")
        else:
            print("You do not own this car.")

    def change_money(self, amount):
        self.money += amount

    def add_bought_cars(self, car):
        self.bought_cars.append(car)

    def print_my_cars(self):
        print(f"Cars owned by {self.first_name} {self.last_name}:")
        for car in self.bought_cars:
            print(f"Model: {car.model}, Seller: {car.seller.first_name} {car.seller.last_name}, Sale Date: {car.sale_date}")

class Seller(Person):
    def __init__(self, first_name, last_name, city):
        super().__init__(first_name, last_name, city)
        self.car_park = []
        self.money = 0
        self.sold_cars = []

    def sell_car(self, car, buyer):
        if car in self.car_park:
            self.car_park.remove(car)
            self.sold_cars.append(car)
            self.money += car.price
            car.buyer = buyer
            car.sale_date = datetime.now().strftime("%Y-%m-%d")
            print(f"Car '{car.model}' sold successfully.")
        else:
            print("The car is not available in the seller's car park.")

    def return_car(self, car, buyer):
        if car in self.sold_cars:
            self.sold_cars.remove(car)
            self.money -= car.price
            car.returned = True
            car.return_info = "Not satisfied"
            buyer.return_car(car)
            print(f"Car '{car.model}' returned successfully.")
        else:
            print("This car was not sold by this seller.")

    def add_car_to_car_park(self, car):
        self.car_park.append(car)

    def check_car_availability(self, car):
        return car in self.car_park

    def get_available_cars(self):
        return self.car_park

class Car:
    def __init__(self, model, price, seller):
        self.model = model
        self.price = price
        self.seller = seller
        self.sale_date = None
        self.returned = False
        self.return_info = None
        self.buyer = None

    def get_sale_date(self):
        return self.sale_date

    def get_discount(self):
        return 0.1 if self.price >= 10000 else 0
