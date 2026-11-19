
from inventory_manager import Supplier, PhysicalProduct, DigitalProduct
from inventory_manager import OrderLine, Order


# Create Supplier
supplier = Supplier("S001", "Tech Supplies", "sales@tech.example")


# Test 1: Invalid Product Price
print("=== TEST 1: INVALID PRICE ===")

try:
    product1 = PhysicalProduct(
        "P001", "Laptop", -100, 10, 1.28, supplier
    )
except ValueError as error:
    print("Error:", error)


# Test 2: Zero Product Price
print("\n=== TEST 2: ZERO PRICE ===")

try:
    product2 = DigitalProduct(
        "D001", "Software", 0, 5, 500, supplier
    )
except ValueError as error:
    print("Error:", error)


# Test 3: Negative Stock
print("\n=== TEST 3: NEGATIVE STOCK ===")

try:
    product3 = PhysicalProduct(
        "P002", "Mouse", 25.50, -5, 0.28, supplier
    )
except ValueError as error:
    print("Error:", error)


# Create Valid Product
product4 = PhysicalProduct(
    "P003", "Keyboard", 45, 20, 0.74, supplier
)


# Test 4: Invalid Stock Update
print("\n=== TEST 4: INVALID STOCK UPDATE ===")

try:
    product4.update_stock(-10)
except ValueError as error:
    print("Error:", error)

print("Current Stock:", product4.get_stock())


# Test 5: Invalid OrderLine Quantity
print("\n=== TEST 5: INVALID ORDERLINE QUANTITY ===")

try:
    order_line = OrderLine(product4, 0)
except ValueError as error:
    print("Error:", error)


# Test 6: Invalid Order Quantity
print("\n=== TEST 6: INVALID ORDER QUANTITY ===")

order1 = Order("O001")

try:
    order1.add_order_line(product4, -3)
except ValueError as error:
    print("Error:", error)

print("Order Total: $", format(order1.calculate_total(), ".2f"))


# Test 7: Valid Product and Order
print("\n=== TEST 7: VALID DATA ===")

product5 = PhysicalProduct(
    "P004", "Monitor", 200, 15, 3.5, supplier
)

order2 = Order("O002")
order2.add_order_line(product5, 2)

order2.display_order()
