import os
from dataclasses import dataclass, field
from typing import List
import csv




@dataclass
# This is the dataclass for Product 
class Product:
    name: str
    price: float = 0.0


@dataclass
# This dataclass for product stock
class ProductStock:
    # dataclass Product, 
    product: Product
    quantity: int


@dataclass
# This dataclass is used to show what stock for shop and customer
class ProductQuantity:
    product: Product  
    quantity: int


@dataclass
# This dataclass defines the shop entity. Consist of the nested dataclass.
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)


@dataclass
# customer class
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductQuantity] = field(default_factory=list)






def create_and_stock_shop():
    shop = Shop()  # starting an instance of the shop dataclass 
    with open('Data/shop_stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        # reads in the amount of cash in shop from file and then assigns it
        shop.cash = float(first_row[0])
        for row in csv_reader:
            # starts an instance of Product; then assigns product name [0] and price [1]
            p = Product(row[0], float(row[1]))
            # starting an instance of ProductStock; and assigning the product stock
            ps = ProductStock(p, float(row[2]))
            shop.stock.append(ps)  # this adds subsequent items to the list for shop
            # print(ps)
    return shop



def create_customer(file_path):
    # print("inside 'create customer' function")  # for testing - ok
    # initialise an instance of the Customer dataclass - is this line necessary?
    customer = Customer()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        # reading in the customer file and then assigning name [0] and budget [1] from file that has been read in
        customer = Customer(first_row[0], float(first_row[1]))
        # print(f"1: Printing customer's name: {str(customer.name)} and budget: {customer.budget:.2f}") # for testing - ok
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            customer.shopping_list.append(ps)

        # print(f"Printing customer's shopping list: {customer.shopping_list}") for testing - ok
        # for item in customer.shopping_list:  # for testing - ok
        #     print_product(item.product)

        return customer



def print_product(prod):
    # if the price is defined (we are showing the shop stock), then both name and price are shown otherwise(we are showing the customer shopping list) only product name is shown
    if prod.price == 0:
        print(f"Product: {prod.name};")
    else:
        print(f"Product: {prod.name}; \tPrice: €{prod.price:.2f}\t", end="")



def print_customers_details(cust, sh):

    # printing the Values of cust.name and cust.budget that refer to the customer's details that are defined in the dataclass instance (within 'Main' method).
    print(f"\nCustomer name: {cust.name}, budget: €{cust.budget:.2f}")
    print(f"---- ---- ----")

    # starting the auxiliary variables
    total_cost = 0

    # printing a customer's shopping list
    print(f"{cust.name} wants the following products: ")

    # looping over all the items in the customer shopping list
    # Iteration of from i=0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
    for cust_item in cust.shopping_list:
        # print(f"{cust_item.product.name} ORDERS {cust_item.quantity} ")  # for testing - ok

        # Showing a customers details 
        print(
            f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")

        # starting  auxiliary variable
        sub_total = 0  # showing the sub total cost for items from the shopping list

        # Calculating sub-total cost of all items of the i-th product in customer's shopping list.

        # checking whether the product from customer's shopping list is matches with the shop stock list of products
        match_exist = 0  # initialy set to zero, assuming there is no match
        # assign the i-th product from the customer schopping list as a shorthand
        cust_item_name = cust_item.product.name

        # Iterate through shop stock list to match cust_s from customer's shopping list
        for sh_item in sh.stock:
            # print("Looping through shop's items: ", sh_item.product.name) # for testing - ok
            # assign the j-th product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # checking if there is match and if the customer's item is in stock
            if cust_item_name == sh_item_name:
                match_exist += 1  # set to one, meaning  that there is a match in stock

                # checking if there is enough of the products in the shops stock

                # showing that there sufficient amount of the product in the shop stock
                if cust_item.quantity <= sh_item.quantity:
                    # printing out cost of all items of the product
                    print(f"\tOK, there is enough in stock and ", end="")

                    # perform the cost of the i-th item from the customer's shopping list(full order for the item is done)
                    sub_total_full = cust_item.quantity * sh_item.product.price  # qty*price
                    # Printing out cost of all items of the product
                    print(f"sub-total cost would be €{sub_total_full:.2f}.")
                    sub_total = sub_total_full  # sub total cost for the i-th item

                else:  # if the customer wants more than is in stock
                    # checking how many items can be bought
                    partial_order_qty = cust_item.quantity - \
                        (cust_item.quantity -
                         sh_item.quantity)  # will buy all that there is in the shops stock

                    # performing the cost of the i-th item from the customer's shopping list
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price  # partial qty * price
                    # Printing out the cost of all items of the product
                    print(
                        f"\tHowever only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
                    sub_total = sub_total_partial

                # performing all addition of sub totals
                total_cost = total_cost + sub_total

        # if customer wants a product that is not in the shop
        if match_exist == 0:  # if there is no match of product
            # Printing out cost of all items of the product
            print(
                f"\tThis product is not available. Sub-total cost will be €{sub_total:.2f}.")

    # Printing out cost of all items of the product
    print(f"\nTotal shopping cost would be €{total_cost:.2f}. \n")

    return total_cost



def process_order(cust, sh, total_cost):

    # Checking if the customer can afford the desired items
    if (cust.budget < total_cost):  # if the customer is short of money
        print(
            f"Unfortunately, the customer does not have enough money for all the desired items - short of €{(total_cost - cust.budget):.2f}. ", end="")
        print(
            f"Shopping aborted. Come back with more money or negotiate your shopping list.\n")

    else:  # else the customer has enough money
        print(f"Processing...")

        # loop over the items in the customer shopping list
        # Iteration of from i = 0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
        for cust_item in cust.shopping_list:
            # checking whether the product from customer's shopping list is matches with the shop stock list of products
            match_exist = 0  # initialy set to zero, assuming there is no match

            # assigning the i-th product from the customer schopping list as a shorthand
            cust_item_name = cust_item.product.name

            # Iterate through shop stock list to match items from customer's shopping list
            for sh_item in sh.stock:
                # assign the j-th product from the shop stock list as a shorthand
                sh_item_name = sh_item.product.name

                if cust_item_name == sh_item_name:  # if both product names are identical
                    match_exist = + 1  # set to one, meaning there is a matach

                    # checking for a products availability
                    # if there is sufficient amount of the product in the shop stock
                    if cust_item.quantity <= sh_item.quantity:
                        # updating all the shop stock(full order)
                        sh_item.quantity = sh_item.quantity - cust_item.quantity
                        print(
                            f"Stock quantity of {cust_item.product.name} updated to: {sh_item.quantity:.0f}")

                    else:  # if the customer wants more than in stock
                        # checking how many can be bought
                        partial_order_qty = cust_item.quantity - \
                            (cust_item.quantity - sh_item.quantity)
                        # will buy all that is in stock

                        # performing the cost of the i-th item from the customer's shopping list
                        sub_total_partial = partial_order_qty * \
                            sh_item.product.price  # partial qty * price

                        # print(f"Only quantity of {cust_item.product.name} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ", end="")
                        # Prints out cost of all items of the product

                        # updateing the shop stock(partial order)
                        sh_item.quantity = sh_item.quantity - partial_order_qty

                        print(
                            f"Stock quantity of {cust_item.product.name} updated to {sh_item.quantity:.0f}.")

            # if customer wants a product that is not in the shop
            if match_exist == 0:  # if there is no match of product
                print(f"\tThis product not available. Sub-total cost will be €0.00.")

        # updating the cash in shop
        sh.cash = sh.cash + total_cost

        # updating the customer's money
        cust.budget = cust.budget - total_cost

        print(f"\nShop has now €{sh.cash:.2f} in cash. ")
        # updated customer's budget
        print(f"{cust.name}'s remaining money is €{cust.budget:.2f}.")
        print("")

    return



def interactive_mode(sh, budget):

    # print(f"Budget: {budget:.2f}")  # for testing - ok

    # printing all of the shops stock
    print(f"\nThe following products are available in shop:")
    print_shop(sh)

    # declaring the required variables
    product_name = ""
    quantity = 0

    # initialise forever loop until user enter 'x' while typing the product name
    # this is a 'forever' loop, unless interupted (break)
    while product_name != "x":

        print()
        # Requesting the input from the user, asking them to assign a variable to show selecting choice
        product_name = input("\nEnter desired product name (x to exit): ")

        # print(f"Test 2: Customer budget: {budget:.2f}, product: {product_name}") # for testing - ok
        # print(f"Test 3: Cash in shop: {sh.cash}") # for testing - ok
        # print(f"Test 4: Product price of index 2: {sh.stock[2].product.price:.2f}") # for testing - ok

        print(f"Searching for: {product_name}")

        # checking whether the product from customer's shopping list is matches with the shop stock list of products
        match_exist = 0  # this is set to zero, assuming there is no match

        # Iterate through shop stock list to match items from customer's shopping list
        for sh_item in sh.stock:

            # initialise auxiliary variable
            sub_total = 0  # sub total cost for items from the shopping list

            # for testing - ok
            # print(f"test 5: item in shop: {sh_item.product.name}") # for testing - ok

            # assign the j-th product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # if the product is found in shop, 
            if product_name == sh_item_name:  # true, if both product names are identical

                match_exist += 1  # set to one, meaning there is a matach

                quantity = int(input("Enter desired quantity: "))

                # checking a products availability the shop
                # chceking if there is a sufficient amount of the product in the shop stock
                if (quantity <= sh_item.quantity):

                    # checking the product price and calculating the sub-total cost(price*qty)
                    sub_total = sh_item.product.price * quantity

                    # checking if the customer can afford it
                    if (budget >= sub_total):

                        # updating the customer's budget
                        budget = budget - sub_total
                        print(
                            f"Bought! Sub total cost was €{sub_total:.2f}. Budget after buying this item: €{budget:.2f}.")

                        # updating the shops stock(full order fulfilled)
                        sh_item.quantity = sh_item.quantity - quantity

                        # updating the shops cash
                        sh.cash = sh.cash + sub_total
                        print(
                            f"Stock quantity of {sh_item_name} in shop updated to: {sh_item.quantity:.0f}. Cash in shop now: {sh.cash:.2f}.")

                    else:  # The customer cannot afford all for order
                        print(
                            f"Unfortunately, you do not have enough money for that many - short of €{(sub_total - budget):.2f}. ", end="")
                        print(
                            f"Come back with more money or reduce the quantity.")

                # if the customer wants more than in stock
                else:
                    # checking how many items can be bought and buy all that is in stock
                    partial_order_qty = quantity - \
                        (quantity - sh_item.quantity)

                    # performing the sub-total cost for the item
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price  # partial qty * price
                    # Printing out the cost of all items of the product
                    print(
                        f"Only {partial_order_qty:.0f} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ")

                    # updating the customer's budget
                    budget = budget - sub_total_partial
                    print(
                        f"Budget after buying this item: €{budget:.2f}.")

                    # updating the shop's stock(partial order) and cash
                    sh_item.quantity = sh_item.quantity - partial_order_qty

                    # updating the shop's cash
                    sh.cash = sh.cash + sub_total_partial
                    print(
                        f"This product is no longer avilable in shop (stock: {sh_item.quantity:.0f}). Cash in shop now: {sh.cash:.2f}.")

        if (match_exist == 0):  # if the product is not available in stock
            print("Product not found in shop.")




def print_shop(sh):  # takeing in the shop's dataclass as a parameter
    # Showing the shop info
    # print(sh)  # for testing - ok
    print(f"\nShop has {sh.cash:.2f} in cash")
    print("==== ==== ====")
    for item in sh.stock:
        print_product(item.product)
        print(f"Available amount: {item.quantity:.0f}")




separator = "=" * 15


def display_menu():#displaying the shop menu with all options for choice

    
    print("1 - Shop status")
    print("2 - Customer A - good case")
    print("3 - Customer B - insufficient funds case")
    print("4 - Customer C - exceeding order case")
    print("5 - Interactive mode")
    print("9 - Exit application\n")
    print("NB: The sequence of the customers being processed might affect the initial case of the customers.")
    print(separator)



def shop_menu(shop): #main function for shop
   

    # Main menu screen
    display_menu()

    while True:  # this is be a loop that is forver, unless if it is broken

        # Requesting the input from a user, assigning to the variable choice
        choice = input("Enter your choice: ")

        if (choice == "1"):
            # print("inside option 1\n") # for testing - ok
            print_shop(shop)
            display_menu()

        elif (choice == "2"):
            # print("inside option 2\n") # for testing - ok

            # create customer A struct (good case)
            customer_A = create_customer(
                "Data/customer_good.csv")  # reading data from a file

            # printing the customer details and the shopping list
            total_cost = print_customers_details(customer_A, shop)

            # showing the customer's shopping list and then calling the relevant method
            process_order(customer_A, shop, total_cost)

            display_menu()

        elif (choice == "3"):
            # creating customer B choice (good case)
            customer_B = create_customer(
                "Data/customer_insufficient_funds.csv")  # reading the data from a file

            # printing all of the customer details and shopping list
            total_cost = print_customers_details(customer_B, shop)

            # showing all of the customer's shopping list and calling relevant method
            process_order(customer_B, shop, total_cost)

            display_menu()

        elif (choice == "4"):
            # create customer C choice 
            customer_C = create_customer(
                "Data/customer_exceeding_order.csv")  # reading the data from a file

            # printing the customer details and their shopping list
            total_cost = print_customers_details(customer_C, shop)

            # showing the customer's shopping list and calling the relevant method
            process_order(customer_C, shop, total_cost)

            display_menu()

        elif (choice == "5"):

            # Welcome message
            print("\nInteractive shopping mode")
            print("-------------------------")

            # getting the user's name
            customer_name = input("What's your name ")
            print(f"Welcome, {customer_name}. ")

            # getting the user's budget
            budget = float(
                input("Enter your budget: "))

            # going back to the interactive mode
            interactive_mode(shop, budget)

            display_menu()

        elif (choice == "9"):  # Exit the shop 
            print("")
            break

        else:
            display_menu()



def main():
  

    # Clear screen
    os.system("cls")   # for Windows systems
    os.system("clear")  # for Linux systems

  

  
    shop_one = create_and_stock_shop()  # assigning the data from a file to variable shop_one.
    # printing(shop_one) # for testing - ok

    shop_menu(shop_one)  # calls function that displays the shop menu



if __name__ == "__main__":
    # execute only if run as a script
    main()