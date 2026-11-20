
from inventory_manager import Supplier, Inventory
from inventory_manager import load_products, get_positive_float


# Create Supplier
supplier = Supplier("S001", "Tech Supplies", "sales@tech.example")


# Test 1: Load products from CSV
print("=== TEST 1: LOAD VALID AND INVALID CSV ROWS ===")

inventory = Inventory()

load_products("products.csv", inventory, supplier)

print("\nProducts loaded into Inventory:")
inventory.display_all()


# Test 2: Missing CSV file
print("\n=== TEST 2: MISSING CSV FILE ===")

inventory2 = Inventory()

load_products("missing_products.csv", inventory2, supplier)


# Test 3: Invalid price input
print("\n=== TEST 3: INVALID USER INPUT ===")

price = get_positive_float("Enter Price: ")

print("Valid Price:", price)
