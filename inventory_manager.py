import json
from abc import ABC, abstractmethod

# Supplier class
class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str= supplier_id
        self.__name:str = name
        self.__contact_email: str = contact_email

    def display_information(self):
        print(f"Supplier ID: {self.__supplier_id} | Supplier Name: {self.__name} | Contact Email: {self.__contact_email}")

    def to_dictionary(self):
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email
        }

#product class
class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name:str = name
        self.__price:float =float(price)
        self.__price:float = float(price)
        self.__stock:int = int(stock)
        self.__supplier:Supplier = supplier

    
    def display_supplier_information(self):
        self.__supplier.display_information()

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_stock(self) -> int:
        return self.__stock

    def get_price(self) -> float:
        return self.__price

    def update_stock(self, quantity):
        if quantity < 0:
            print("Stock cannot be negative.\n")
        else:
            self.__stock = quantity
            print("\nStock updated successfully!\n")

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${format(self.__price, '.2f')} | Stock: {self.__stock}")


    def to_dictionary(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dictionary()
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass

#CanBeShipped interface
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# Inheritance class for PhysicalProduct
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight :float= float(weight)

    def display_information(self):
        super().display_information()  # Call the parent class method to display common information
        print(f"Weight: {self.__weight} kg \n")

    def get_fulfilment_info(self) -> str:
            return "Physical product requires shipping."

    def calculate_shipping_cost(self) -> float:
            return self.__weight * 5


    def to_dictionary(self):
        data = super().to_dictionary()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


# Inheritance class for DigitalProduct
class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size :float= float(download_size)


    def display_information(self):
        super().display_information()  # Call the parent class method to display common information
        print(f"Download Size: {self.__download_size} MB \n")

    def get_fulfilment_info(self) -> str:
            return "Digital product is delivered."

    def to_dictionary(self):
        data = super().to_dictionary()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

#ProductFactory class
class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str,
               price: float, stock: int, supplier: Supplier,
               extra: float) -> Product:

        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock, extra, supplier
            )

        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock, extra, supplier
            )

        else:
            raise ValueError(f"Unknown product type: {product_type}")


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product):
        if self.search_product(product.get_id()) is not None:
            print("Product ID already exists.\n")
        else:
            self.__products.append(product)

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_id() == product_id:
             return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        return self.search_product(product_id)

    def remove_product(self, product_id: str):
        product = self.search_product(product_id)

        if product is not None:
            self.__products.remove(product)
            print("Product removed successfully.\n")
        else:
            print("Product ID not found.\n")


    def display_all(self):
        print("Current Inventory\n",
              "------------------------------------\n")
        for product in self.__products:
            product.display_information()
        print("\n------------------------------------\n")

    def get_products(self) -> list[Product]:
        return self.__products

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.__percentage = percentage

    def apply(self, total: float) -> float:
        return total - (total * self.__percentage / 100)

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        else:
            return total

class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95

#orderline class
class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity:int = int(quantity)

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def get_product(self) -> Product:
        return self.__product

# order class
class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy = None):
        self.__order_id:str = order_id
        self.__order_lines: list[OrderLine] = []

        if discount is None:
            self.__discount: DiscountStrategy = NoDiscount()
        else:
            self.__discount: DiscountStrategy = discount

    def add_order_line(self, product: Product, quantity: int):
        if quantity <= 0:
            print("Quantity must be greater than zero.\n")
        else:
            order_line = OrderLine(product, quantity)
            self.__order_lines.append(order_line)

    def set_discount(self, discount: DiscountStrategy):
        self.__discount = discount

    def calculate_total(self) -> float:
        total = 0

        for order_line in self.__order_lines:
            total = total + order_line.calculate_subtotal()

        return self.__discount.apply(total)

    def display_order(self):
        print("Order ID:", self.__order_id)

        for order_line in self.__order_lines:
            print("Subtotal: $",
                  format(order_line.calculate_subtotal(), ".2f"))

        print("Total: $", format(self.calculate_total(), ".2f"))

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def remove_order_line(self, product_id: str):
        for order_line in self.__order_lines:
            if order_line.get_product().get_id() == product_id:
                self.__order_lines.remove(order_line)
                print("Order line removed successfully.\n")
                return

        print("Product not found in order.\n")


# Load inventory from JSON file
def load_inventory(inventory):
    try:
        file = open("inventory.json", "r")
        saved_products = json.load(file)
        file.close()

    except FileNotFoundError:
        print("No existing inventory file found.\n")
        return

    for data in saved_products:
        product_type = data.get("type")
        if product_type is None:
            print("\nOld product record found:", data["name"])
            print("1. Physical Product")
            print("2. Digital Product")

            choice = input("Select Product Type: ")

            if choice == "1":
                product_type = "physical"
                data["weight"] = float(input("Weight (kg): "))
            elif choice == "2":
                product_type = "digital"
                data["download_size"] = float(input("Download Size (MB): "))
            else:
                print("Invalid type. Product skipped.\n")
                continue

        supplier_data = data.get("supplier")

        if supplier_data is None:
            print("\nSupplier information missing for:", data["name"])

            supplier_id = input("Supplier ID: ")
            supplier_name = input("Supplier Name: ")
            contact_email = input("Contact Email: ")

            supplier = Supplier(
                supplier_id, supplier_name, contact_email
            )

        else:
            supplier = Supplier(
                supplier_data["supplier_id"],
                supplier_data["name"],
                supplier_data["contact_email"]
            )


        if product_type == "physical":
            extra = data["weight"]

        elif product_type == "digital":
            extra = data["download_size"]

        else:
            print("Unknown product type. Product skipped.\n")
            continue

        product = ProductFactory.create(
            product_type,
            data["id"],
            data["name"],
            data["price"],
            data["stock"],
            supplier,
            extra)

        inventory.add_product(product)

    else:
        print("Unknown product type. Product skipped.\n")
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
            print("1. Physical Product")
            print("2. Digital Product")
            product_type = input("Select Product Type: ")

            if product_type != "1" and product_type != "2":
                print("Invalid Product Type.\n")
                continue

            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))

            if price < 0 or quantity < 0:
                print("Price and stock cannot be negative.\n")

            elif inventory.search_product(product_id) is not None:
                print("Product ID already exists.\n")

            else:

                print("\nSupplier Information")
                supplier_id = input("Supplier ID: ")
                supplier_name = input("Supplier Name: ")
                contact_email = input("Contact Email: ")

                supplier = Supplier(
                    supplier_id, supplier_name, contact_email
                )

                # Physical Product
            if product_type == "1":
                weight = float(input("Weight (kg): "))

                if weight < 0:
                    print("Weight cannot be negative.\n")
                    continue

                extra = weight
                product_type = "physical"

            # Digital Product
            else:
                download_size = float(input("Download Size (MB): "))

                if download_size < 0:
                    print("Download size cannot be negative.\n")
                    continue

                extra = download_size
                product_type = "digital"

            # Create product using ProductFactory
            new_product = ProductFactory.create(
                product_type,
                product_id,
                product_name,
                price,
                quantity,
                supplier,
                extra
            )

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
