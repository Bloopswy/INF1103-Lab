import json

#def load_inventory():
#   file = open("inventory.json", "a")
 #   file.close()
    
  #  with open("inventory.json", "r") as file:
   #     inventory = file.readlines()
    #    return inventory

#def save_inventory():
 #   print ("Saving inventory before exit...")
  #  file = open('inventory.json', 'w') as f
   #file.close()
   # print("Inventory saved successfully.\n")
#return (inventory)


#Menu option 1
def display_all():
    print ("Current Inventory\n", 
           "------------------------------------\n")
    for product in inventory:
        print("ID:", product["id"],
            " | Name:", product["name"],
            " | Price: $", product["price"],
            " | Stock:", product["stock"])
    print("\n------------------------------------\n")
    
#Menu option 2
def add_product():
    product_ID = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))

    new_product = {
        "id": product_ID,
        "name": product_name,
        "price": price,
        "stock": quantity
    }

    inventory.append(new_product)

    print("Product added successfully!\n")
   
#Menu option 3
def update_stock():
    print ("Update Stock")
    product_ID = input("Enter Product ID: ")
    for product in inventory:
        if product["id"] == product_ID:
            print("\nProduct Found:\n",
                  "Name:", product["name"], "\n",
                  "Current Stock:", product["stock"], "\n")

            new_stock = int(input("New Stock Quantity: "))
            product["stock"] = new_stock
            print("\nStock updated successfully!\n")
            return
    print ("Product ID not found.\n")


#Menu option 4
def search_product():
    print("Search Product")
    product_ID = input("Enter Product ID: ")
    for product in inventory:
        if product["id"] == product_ID:
            print("\nProduct Found:\n",
                  "-----------------------------------",
                  "ID:", product["id"], "\n",
                  "Name:", product["name"], "\n",
                  "Price: $", product["price"], "\n",
                  "Current Stock:", product["stock"], "\n"
                  "-----------------------------------",)
            return
    print("Product not found.")

while True:
    print("=============================================\n",
          "INVENTORY MANAGEMENT SYSTEM\n",
          "=============================================\n")

    #loaded inventory

    print ("----------- MENU -----------\n",
           "1. Display All Products\n",
           "2. Add Product\n",
           "3. Update Stock\n",
           "4. Search Product\n",
           "5. Save Inventory\n",
           "6. Exit\n")
    input_option = input("Enter Option: ")

    if input_option == "1":
        print (display_all())

    elif input_option == "2":
        add_product = add_product()

    elif input_option == "3":
        update_stock = update_stock()

    elif input_option == "4":
        search_product = search_product()

    #elif input_option == "5": #save only
        #save_inventory = save_inventory()

    elif input_option == "6": #save plus quit
        print ("Thank you fro using Inventory Management System.\n Program terminated.")
        break

    else: 
        print ("Invalid Option. Please try again.\n")
    
