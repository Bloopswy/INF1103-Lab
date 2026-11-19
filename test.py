
from inventory_manager import (
    Supplier, PhysicalProduct, DigitalProduct,
    ProductFactory, Inventory, Order, OrderLine,
    NoDiscount, PercentageDiscount, BulkDiscount,
    StudentDiscount, load_products, get_positive_float
)


# Create Supplier
supplier = Supplier("S001", "Tech Supplies", "sales@tech.example")


# Part 2: Strategy Pattern
print("=== PART 2: STRATEGY PATTERN ===")

product1 = PhysicalProduct("P001", "Keyboard", 125, 10, 0.7, supplier)

order1 = Order("O001", BulkDiscount(200, 20))
order1.add_order_line(product1, 2)

print("Bulk Discount:")
order1.display_order()

order1.set_discount(PercentageDiscount(10))
print("\n10% Discount:")
order1.display_order()

order1.set_discount(NoDiscount())
print("\nNo Discount:")
order1.display_order()

order1.set_discount(StudentDiscount())
print("\nStudent Discount:")
order1.display_order()


# Part 3: Factory Pattern
print("\n=== PART 3: FACTORY PATTERN ===")

physical = ProductFactory.create(
    "physical", "P002", "Mouse", 25.50, 40, supplier, 0.28
)

digital = ProductFactory.create(
    "digital", "D001", "Software", 200, 5, supplier, 500
)

physical.display_information()
digital.display_information()

print("Is PhysicalProduct?", isinstance(physical, PhysicalProduct))
print("Is DigitalProduct?", isinstance(digital, DigitalProduct))

try:
    ProductFactory.create(
        "service", "S002", "Installation", 50, 10, supplier, 0
    )

except ValueError as error:
    print("Error:", error)


# Part 4: Validation
print("\n=== PART 4: VALIDATION ===")

# Invalid price
try:
    PhysicalProduct("P003", "Laptop", -100, 10, 1.28, supplier)
except ValueError as error:
    print("Invalid Price:", error)

# Zero price
try:
    DigitalProduct("D002", "Editor", 0, 10, 500, supplier)
except ValueError as error:
    print("Zero Price:", error)

# Negative stock
try:
    PhysicalProduct("P004", "Monitor", 200, -5, 3.5, supplier)
except ValueError as error:
    print("Negative Stock:", error)

# Invalid stock update
try:
    physical.update_stock(-10)
except ValueError as error:
    print("Invalid Stock Update:", error)

print("Current Stock:", physical.get_stock())

# Invalid OrderLine quantity
try:
    OrderLine(physical, 0)
except ValueError as error:
    print("Invalid OrderLine:", error)

# Invalid Order quantity
order2 = Order("O002")

try:
    order2.add_order_line(physical, -3)
except ValueError as error:
    print("Invalid Order Quantity:", error)

print("Order Total: $", format(order2.calculate_total(), ".2f"))


# Part 5: Exception Handling
print("\n=== PART 5: EXCEPTION HANDLING ===")

# Test CSV loading
print("\nTest 1: Load products.csv")

inventory = Inventory()
load_products("products.csv", inventory, supplier)

print("\nProducts loaded:")
inventory.display_all()

# Test missing file
print("\nTest 2: Missing CSV file")

inventory2 = Inventory()
load_products("missing_products.csv", inventory2, supplier)

# Test user input
print("\nTest 3: Invalid User Input")

price = get_positive_float("Enter Price: ")
print("Valid Price:", price)
