
import json

# Product class
class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if quantity < 0:
            print("Stock cannot be negative.\n")
        else:
            self.__stock = quantity
            print("\nStock updated successfully!\n")

    def display_information(self):
        print("ID:", self.__product_id,
              "| Name:", self.__name,
              "| Price: $", format(self.__price, ".2f"),
              "| Stock:", self.__stock)

    def to_dictionary(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


# Inventory class
class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_id()) is not None:
            print("Product ID already exists.\n")
        else:
            self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory\n",
              "------------------------------------\n")
        for product in self.__products:
            product.display_information()
        print("\n------------------------------------\n")

    def get_products(self):
        return self.__products


# Load inventory from JSON file
def load_inventory(inventory):
    file = open("inventory.json", "r")
    saved_products = json.load(file)
    file.close()

    for data in saved_products:
        product = Product(data["id"], data["name"], data["price"], data["stock"])
        inventory.add_product(product)

    print("Inventory loaded successfully.\n")


# Save inventory to JSON file
def save_inventory(inventory):
    saved_products = []

    for product in inventory.get_products():
        saved_products.append(product.to_dictionary())

    file = open("inventory.json", "w")
    json.dump(saved_products, file, indent=4)
    file.close()

    print("Inventory saved successfully to inventory.json.\n")


# Main program
if __name__ == "__main__":
    inventory = Inventory()
    load_inventory(inventory)

print("=============================================\n",
        "INVENTORY MANAGEMENT SYSTEM\n",
        "=============================================\n")
    
print("----------- MENU -----------\n",
              "1. Display All Products\n",
              "2. Add Product\n",
              "3. Update Stock\n",
              "4. Search Product\n",
              "5. Save Inventory\n",
              "6. Exit\n",
              "-----------------------------\n")

while True:

        input_option = input("Enter Option: ")

        # Menu option 1 - Display All Products
        if input_option == "1":
            inventory.display_all()

        # Menu option 2 - Add Product
        elif input_option == "2":
            print("Add New Product")
            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))

            if price < 0 or quantity < 0:
                print("Price and stock cannot be negative.\n")

            elif inventory.search_product(product_id) is not None:
                print("Product ID already exists.\n")

            else:
                new_product = Product(product_id, product_name, price, quantity)
                inventory.add_product(new_product)
                print("Product added successfully!\n")

        # Menu option 3 - Update Stock
        elif input_option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("\nProduct Found:\n",
                      "Name:", product.get_name(), "\n",
                      "Current Stock:", product.get_stock(), "\n")

                new_stock = int(input("New Stock Quantity: "))
                product.update_stock(new_stock)

            else:
                print("Product ID not found.\n")

        # Menu option 4 - Search Product
        elif input_option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("\nProduct Found:\n-----------------------------------")
                product.display_information()
                print("-----------------------------------\n")
            else:
                print("Product not found.\n")

        # Menu option 5 - Save Inventory
        elif input_option == "5":
            save_inventory(inventory)

        # Menu option 6 - Exit
        elif input_option == "6":
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid Option. Please try again.\n")
