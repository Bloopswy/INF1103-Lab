
from inventory_manager import Supplier, PhysicalProduct, Order
from inventory_manager import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount


# Create Supplier
supplier = Supplier("S001", "Tech Supplies", "sales@tech.example")

# Create Product
product1 = PhysicalProduct("P001", "Keyboard", 125, 10, 0.7, supplier)

# Create Order with BulkDiscount
order1 = Order("O001", BulkDiscount(200, 20))

# Add two keyboards ($125 x 2 = $250)
order1.add_order_line(product1, 2)

# Test BulkDiscount
print("Order with Bulk Discount:")
order1.display_order()

print()

# Change to PercentageDiscount
order1.set_discount(PercentageDiscount(10))

print("Order with 10% Discount:")
order1.display_order()

print()

# Change to NoDiscount
order1.set_discount(NoDiscount())

print("Order with No Discount:")
order1.display_order()

print()

# Change to StudentDiscount
order1.set_discount(StudentDiscount())

print("Order with Student Discount:")
order1.display_order()
