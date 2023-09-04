from models import *
from utils import CarMarketEncoder


class CarMarket:
    def __init__(self):
        self.buyers = []
        self.sellers = []
        self.cars = []

    def create_buyers(self):
        while True:
            first_name = input("Enter buyer's first name: ")
            last_name = input("Enter buyer's last name: ")
            city = input("Enter buyer's city: ")
            money = int(input("Enter buyer's money: "))

            buyer = Buyer(first_name, last_name, city, money)
            self.buyers.append(buyer)

            create_more = input("Create more buyers? (Y/n) ")
            if create_more.lower() != "y":
                break

    def create_sellers(self):
        while True:
            first_name = input("Enter seller's first name: ")
            last_name = input("Enter seller's last name: ")
            city = input("Enter seller's city: ")

            seller = Seller(first_name, last_name, city)
            self.sellers.append(seller)

            create_more = input("Create more sellers? (Y/n) ")
            if create_more.lower() != "y":
                break

    def create_cars(self):
        for seller in self.sellers:
            while True:
                model = input("Enter car's model: ")
                price = int(input("Enter car's price: "))

                car = Car(model, price, seller)
                self.cars.append(car)
                seller.add_car_to_car_park(car)
                print(f"Added car '{car.model}' for seller {seller.first_name} {seller.last_name}")
                create_more = input("Create more cars for this seller? (Y/n) ")
                if create_more.lower() != "y":
                    break

    def print_available_cars(self):
        for seller in self.sellers:
            print(f"Available cars for {seller.first_name} {seller.last_name}:\n")
            for car in seller.get_available_cars():
                print(f"Model: {car.model}, Price: ${car.price}")

    def purchase_cars(self):
        for buyer in self.buyers:
            while True:
                print(f"Buyer: {buyer.first_name} {buyer.last_name}")
                cars_index_list = [x for x in range(len(self.cars))]
                print("Choose car index -> {}".format(cars_index_list))
                car_index = int(input("Enter the index of the car you want to buy: "))
                car = self.cars[car_index]
                buyer.buy_car(car)

                create_more = input("Buy more cars? (Y/n) ")
                if create_more.lower() != "y":
                    break

    def print_cars_owned_by_buyers(self):
        for buyer in self.buyers:
            buyer.print_my_cars()

    def print_sold_cars_by_sellers(self):
        for seller in self.sellers:
            print(f"Sold cars by {seller.first_name} {seller.last_name}:")
            for car in seller.sold_cars:
                print(f"Model: {car.model}, Buyer: {car.buyer}, Sale Date: {car.sale_date}")


    def return_car(self):
        print("Return Car:")

        # Display available buyer names
        print("Available Buyers:")
        for buyer in self.buyers:
            print(buyer.first_name + " " + buyer.last_name)

        buyer_name = input("Enter the buyer's name: ")

        # Find the buyer by name
        selected_buyer = None
        for buyer in self.buyers:
            if buyer.first_name + " " + buyer.last_name == buyer_name:
                selected_buyer = buyer
                break

        if selected_buyer:
            # Display available car models for the selected buyer
            print(f"Available Car Models for {buyer_name}:")
            for car in selected_buyer.bought_cars:
                print(car.model)

            car_model = input("Enter the car's model: ")

            # Find the car by model for the selected buyer
            selected_car = None
            for car in selected_buyer.bought_cars:
                if car.model == car_model:
                    selected_car = car
                    break

            if selected_car:
                # Check if the car has already been returned
                if not selected_car.returned:
                    selected_car.returned = True
                    return_info = input("Enter return information: ")
                    selected_car.return_info = return_info

                    # Remove the car from the buyer's list of owned cars
                    selected_buyer.bought_cars.remove(selected_car)

                    # Update seller and transaction details
                    selected_car.seller.return_car(selected_car, selected_buyer)

                    print(f"Car '{car_model}' returned successfully.")
                else:
                    print("This car has already been returned.")
            else:
                print("Car not found for the selected buyer.")
        else:
            print("Buyer not found.")

    def serialize_market_data(self):
        market_data = {
            "cars": [car for car in self.cars],
            "buyers": [buyer for buyer in self.buyers],
            "sellers": [seller for seller in self.sellers]
        }

        json_data = json.dumps(market_data, indent=4, cls=CarMarketEncoder)

        # Save the JSON data to a file
        with open("market_data.json", "a") as file:
            file.write(json_data)

        print("Market data saved to market_data.json")


    def run(self):
        while True:
            print("\nMain Menu:")
            print("1. Create buyers")
            print("2. Create sellers")
            print("3. Create cars")
            print("4. Print available cars for each seller")
            print("5. Buy cars")
            print("6. Print cars owned by each buyer")
            print("7. Print sold cars by each seller")
            print("8. Manage Cars")
            print("9. Exit")

            choice = input("Enter your choice (1-9): ")

            if choice == "1":
                self.create_buyers()
            elif choice == "2":
                self.create_sellers()
            elif choice == "3":
                self.create_cars()
            elif choice == "4":
                self.print_available_cars()
            elif choice == "5":
                if not self.buyers or not self.cars:
                    print("Please create buyers and cars first.")
                else:
                    self.purchase_cars()
            elif choice == "6":
                if not self.buyers:
                    print("Please create buyers first.")
                else:
                    self.print_cars_owned_by_buyers()
            elif choice == "7":
                if not self.sellers:
                    print("Please create sellers first.")
                else:
                    self.print_sold_cars_by_sellers()
            elif choice == "8":
                self.manage_cars_submenu()  # Enter the sub-menu for car management
            elif choice == "9":
                break
            else:
                print("Invalid choice. Please enter a valid option (1-9).")

    def manage_cars_submenu(self):
        while True:
            print("\nManage Cars Menu:")
            print("1. Return Car")
            print("2. Save market data to JSON")
            print("3. Back to Main Menu")

            car_choice = input("Enter your choice (1-3): ")

            if car_choice == "1":
                self.return_car()
            elif car_choice == "2":
                self.serialize_market_data()
            elif car_choice == "3":
                break
            else:
                print("Invalid choice. Please enter a valid option (1-3).")
