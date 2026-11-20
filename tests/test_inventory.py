
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from inventory_manager import (Supplier,Product, PhysicalProduct,DigitalProduct,ProductFactory,Inventory,Order,OrderLine,
    NoDiscount,PercentageDiscount,BulkDiscount, StudentDiscount,get_positive_float,load_products
)

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier(
            "S001", "Tech Supplies", "sales@tech.example")

        self.product1 = PhysicalProduct(
            "P001", "Keyboard", 125, 10, 0.7, self.supplier)

        self.product2 = DigitalProduct(
            "D001", "Software", 200, 5, 500, self.supplier)

    def test_no_discount(self):
        order = Order("O001", NoDiscount())
        order.add_order_line(self.product1, 2)

        self.assertEqual(order.calculate_total(), 250.0)

    def test_percentage_discount(self):
        order = Order("O002", PercentageDiscount(10))
        order.add_order_line(self.product1, 2)

        self.assertEqual(order.calculate_total(), 225.0)

    def test_bulk_discount(self):
        order = Order("O003", BulkDiscount(200, 20))
        order.add_order_line(self.product1, 2)

        self.assertEqual(order.calculate_total(), 230.0)

    def test_student_discount(self):
        order = Order("O004", StudentDiscount())
        order.add_order_line(self.product1, 2)

        self.assertEqual(order.calculate_total(), 237.50)

    def test_change_discount(self):
        order = Order("O005")
        order.add_order_line(self.product1, 2)
        self.assertEqual(order.calculate_total(), 250.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)


    def test_create_physical_product(self):
        product = ProductFactory.create(
            "physical", "P002", "Mouse",
            25.50, 40, self.supplier, 0.28)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_create_digital_product(self):
        product = ProductFactory.create(
            "digital", "D002", "Photo Editor",
            49.90, 100, self.supplier, 500)

        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)

    def test_unknown_product_type(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service", "S002", "Installation",
                30, 5, self.supplier, 0)


    def test_negative_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P003", "Laptop", -100,
                10, 1.28, self.supplier)

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            DigitalProduct(
                "D003", "Software",
                0, 5, 500, self.supplier)

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P004", "Monitor", 200,
                -5, 3.5, self.supplier)

    def test_invalid_stock_update(self):
        with self.assertRaises(ValueError):
            self.product1.update_stock(-10)

        self.assertEqual(self.product1.get_stock(), 10)

    def test_invalid_orderline_quantity(self):
        with self.assertRaises(ValueError):
            OrderLine(self.product1, 0)

    def test_invalid_order_quantity(self):
        order = Order("O006")

        with self.assertRaises(ValueError):
            order.add_order_line(self.product1, -3)

        self.assertEqual(order.calculate_total(), 0.0)
        self.assertEqual(len(order.get_order_lines()), 0)


    def test_positive_float_input(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(StringIO()):
                price = get_positive_float("Enter Price: ")
        self.assertEqual(price, 12.5)


    def test_load_valid_and_invalid_csv(self):
        csv_data = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P010,Desk Lamp,25.00,10\n"
            "digital,D010,Photo Editor,49.90,100\n"
            "service,S010,Installation,30.00,5\n"
            "physical,P011,Office Chair,abc,3\n"
            "physical,P012,Monitor Stand,39.50,7\n")

        inventory = Inventory()

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(csv_data, encoding="utf-8")

            output = StringIO()

            with redirect_stdout(output):
                load_products(str(path), inventory, self.supplier)

        self.assertEqual(len(inventory.get_products()), 3)

        self.assertIsNotNone(inventory.search_product("P010"))
        self.assertIsNotNone(inventory.search_product("D010"))
        self.assertIsNotNone(inventory.search_product("P012"))

        self.assertIsNone(inventory.search_product("S010"))
        self.assertIsNone(inventory.search_product("P011"))

        self.assertIn("3 products loaded.", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_missing_csv_file(self):
        inventory = Inventory()

        with tempfile.TemporaryDirectory() as folder:
            missing_path = Path(folder) / "missing_products.csv"

            output = StringIO()

            with redirect_stdout(output):
                load_products(
                    str(missing_path), inventory, self.supplier
                )

        self.assertEqual(len(inventory.get_products()), 0)

        self.assertIn(
            "Products file not found:",
            output.getvalue()
        )

        self.assertIn(
            "Load attempt finished.",
            output.getvalue()
        )

if __name__ == "__main__":
    unittest.main()
