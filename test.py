
from inventory_manager import Supplier, ProductFactory
from inventory_manager import PhysicalProduct, DigitalProduct


# Create Supplier
supplier = Supplier("S001", "Tech Supplies", "sales@tech.example")


# Test PhysicalProduct using Factory
print("=== Physical Product ===")

product1 = ProductFactory.create(
    "physical", "P001", "Laptop", 1200, 15, supplier, 1.28
)

product1.display_information()
print(product1.get_fulfilment_info())
print("Is PhysicalProduct?", isinstance(product1, PhysicalProduct))

print()


# Test DigitalProduct using Factory
print("=== Digital Product ===")

product2 = ProductFactory.create(
    "digital", "D001", "Software", 200, 5, supplier, 500
)

product2.display_information()
print(product2.get_fulfilment_info())
print("Is DigitalProduct?", isinstance(product2, DigitalProduct))

print()


# Test unknown product type
print("=== Unknown Product Type ===")

try:
    product3 = ProductFactory.create(
        "service", "S001", "Installation", 50, 10, supplier, 0
    )

except ValueError as error:
    print("Error:", error)
