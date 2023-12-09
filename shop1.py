import os
from dataclasses import dataclass, field
from typing import List
import csv

'''
# ===== ===== ===== ===== ===== =====
# Definiton of dataclasses
# ===== ===== ===== ===== ===== =====
'''


@dataclass
# This dataclass defines the data structure (blueprint) for products offered in the shop. It consists of two variables, defined inside.
class Product:
    name: str
    price: float = 0.0


@dataclass
# This dataclass defines the blueprint for products offered in the shop.
class ProductStock:
    # dataclass Product, defined above (i.e. nested dataclasses)
    product: Product
    quantity: int


@dataclass
# This dataclass is used to show the stock both shop and customer.
class ProductQuantity:
    product: Product  # nested dataclasses
    quantity: int


@dataclass
# This dataclass defines the shop entity. Consist of the nested dataclass.
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)


@dataclass
# Defines the customer blueprint.
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductQuantity] = field(default_factory=list)


'''
# ===== ===== ===== ===== ===== =====
# Definition of the functions
# ===== ===== ===== ===== ===== =====
'''


# ----- ----- ----- ----- -----
# Create shop - read data from file
# ----- ----- ----- ----- -----
def create_and_stock_shop():
    shop = Shop()  # initialise an instance of the Shop dataclass
    with open('Data/shop_stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        # reads and assigns amount of cash in shop from file
        shop.cash = float(first_row[0])
        for row in csv_reader:
            # initialise instance of Product; assigns product name [0] and price [1]
            p = Product(row[0], float(row[1]))
            # initialise instance of ProductStock; assigns product stock
            ps = ProductStock(p, float(row[2]))
            shop.stock.append(ps)  # add subsequent items to the list
            # print(ps)
    return shop


# ----- ----- ----- ----- -----
# Create customer - read data from file
# ----- ----- ----- ----- -----
def create_customer(file_path):
    # print("inside 'create customer' function")  # for testing - ok
    # initialise an instance of the Customer dataclass - is this line necessary?
    customer = Customer()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        # reads and assigns name [0] and budget [1] from file
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


# ----- ----- ----- ----- -----
# Printing product info
# ----- ----- ----- ----- -----
def print_product(prod):
    # if the price is defined (we are showing the shop stock), then both name and price are shown otherwise(we are showing the customer shopping list) only product name is showm
    if prod.price == 0:
        print(f"Product: {prod.name};")
    else:
        print(f"Product: {prod.name}; \tPrice: €{prod.price:.2f}\t", end="")


# ----- ----- ----- ----- -----
# Show customers details
# ----- ----- ----- ----- -----
def print_customers_details(cust, sh):

    # Values of cust.name and cust.budget are referring to customer's details defined the dataclass instance (within 'Main' method).
    print(f"\nCustomer name: {cust.name}, budget: €{cust.budget:.2f}")
    print(f"---- ---- ----")

    # initialise auxiliary variables
    total_cost = 0

    # show customer's shopping list
    print(f"{cust.name} wants the following products: ")

    # loop over the items in the customer shopping list
    # Iteration of from i=0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
    for cust_item in cust.shopping_list:
        # print(f"{cust_item.product.name} ORDERS {cust_item.quantity} ")  # for testing - ok

        # Show customers details (example of chain-accessing the data in the nested dataclasses)
        print(
            f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")

        # initialise auxiliary variable
        sub_total = 0  # sub total cost for items from the shopping list

        # Calculating sub-total cost of all items of the i-th product in customer's shopping list.

        # check whether the product from customer's shopping list is matches with the shop stock list of products
        match_exist = 0  # initialy set to zero, assuming there is no match
        # assign the i-th product from the customer schopping list as a shorthand
        cust_item_name = cust_item.product.name

        # Iterate through shop stock list to match cust_s from customer's shopping list
        for sh_item in sh.stock:
            # print("Looping through shop's items: ", sh_item.product.name) # for testing - ok
            # assign the j-th product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # check if there is match (customer's item is in stock)
            if (cust_item_name == sh_item_name):
                match_exist += 1  # set to one, meaning there is a matach

                # check if there is enought of the products in the shop stock

                # sufficient amount of the product in the shop stock
                if (cust_item.quantity <= sh_item.quantity):
                    # Prints out cost of all items of the product
                    print(f"\tOK, there is enough in stock and ", end="")

                    # perform the cost of the i-th item from the customer's shopping list(full order for the item is done)
                    sub_total_full = cust_item.quantity * sh_item.product.price  # qty*price
                    # Prints out cost of all items of the product
                    print(f"sub-total cost would be €{sub_total_full:.2f}.")
                    sub_total = sub_total_full  # sub total cost for the i-th item

                else:  # customer wants more than in stock
                    # check how many can be bought
                    partial_order_qty = cust_item.quantity - \
                        (cust_item.quantity -
                         sh_item.quantity)  # will buy all that is in stock

                    # perform the cost of the i-th item from the customer's shopping list
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price  # partial qty * price
                    # Prints out cost of all items of the product
                    print(
                        f"\tHowever only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
                    sub_total = sub_total_partial

                # addition of sub totals
                total_cost = total_cost + sub_total

        # if customer wants a product that is not in the shop
        if (match_exist == 0):  # there is no match of product
            # Prints out cost of all items of the product
            print(
                f"\tThis product is not available. Sub-total cost will be €{sub_total:.2f}.")

    # Prints out cost of all items of the product
    print(f"\nTotal shopping cost would be €{total_cost:.2f}. \n")

    return total_cost


# ----- ----- ----- ----- -----
# update shop stock, shop cash, customer money(shopping list remains unchanged)
# ----- ----- ----- ----- -----
def process_order(cust, sh, total_cost):

    # Check whether the customer can afford the desired items
    if (cust.budget < total_cost):  # customer is short of money
        print(
            f"Unfortunately, the customer does not have enough money for all the desired items - short of €{(total_cost - cust.budget):.2f}. ", end="")
        print(
            f"Shopping aborted. Come back with more money or negotiate your shopping list.\n")

    else:  # customer has enough money
        print(f"Processing...")

        # loop over the items in the customer shopping list
        # Iteration of from i = 0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
        for cust_item in cust.shopping_list:
            # check whether the product from customer's shopping list is matches with the shop stock list of products
            match_exist = 0  # initialy set to zero, assuming there is no match

            # assign the i-th product from the customer schopping list as a shorthand
            cust_item_name = cust_item.product.name

            # Iterate through shop stock list to match items from customer's shopping list
            for sh_item in sh.stock:
                # assign the j-th product from the shop stock list as a shorthand
                sh_item_name = sh_item.product.name

                if (cust_item_name == sh_item_name):  # if both product names are identical
                    match_exist = + 1  # set to one, meaning there is a matach

                    # check products availability
                    # sufficient amount of the product in the shop stock
                    if (cust_item.quantity <= sh_item.quantity):
                        # update the shop stock(full order)
                        sh_item.quantity = sh_item.quantity - cust_item.quantity
                        print(
                            f"Stock quantity of {cust_item.product.name} updated to: {sh_item.quantity:.0f}")

                    else:  # customer wants more than in stock
                        # check how many can be bought
                        partial_order_qty = cust_item.quantity - \
                            (cust_item.quantity - sh_item.quantity)
                        # will buy all that is in stock

                        # perform the cost of the i-th item from the customer's shopping list
                        sub_total_partial = partial_order_qty * \
                            sh_item.product.price  # partial qty * price

                        # print(f"Only quantity of {cust_item.product.name} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ", end="")
                        # Prints out cost of all items of the product

                        # update the shop stock(partial order)
                        sh_item.quantity = sh_item.quantity - partial_order_qty

                        print(
                            f"Stock quantity of {cust_item.product.name} updated to {sh_item.quantity:.0f}.")

            # if customer wants a product that is not in the shop
            if (match_exist == 0):  # there is no match of product
                print(f"\tThis product not available. Sub-total cost will be €0.00.")

        # update the cash in shop
        sh.cash = sh.cash + total_cost

        # update the customer's money
        cust.budget = cust.budget - total_cost

        print(f"\nShop has now €{sh.cash:.2f} in cash. ")
        # updated customer's budget
        print(f"{cust.name}'s remaining money is €{cust.budget:.2f}.")
        print("")

    return


# ----- ----- ----- ----- -----
# interactive(live) mode
# ----- ----- ----- ----- -----
def interactive_mode(sh, budget):

    # print(f"Budget: {budget:.2f}")  # for testing - ok

    # print shops stock
    print(f"\nThe following products are available in shop:")
    print_shop(sh)

    # declare required variables
    product_name = ""
    quantity = 0

    # initialise forever loop until user enter 'x' while typing the product name
    # this is a 'forever' loop, unless interupted (break)
    while product_name != "x":

        print()
        # Request input from the user, assign to the variable
        product_name = input("\nEnter desired product name (x to exit): ")

        # print(f"Test 2: Customer budget: {budget:.2f}, product: {product_name}") # for testing - ok
        # print(f"Test 3: Cash in shop: {sh.cash}") # for testing - ok
        # print(f"Test 4: Product price of index 2: {sh.stock[2].product.price:.2f}") # for testing - ok

        print(f"Searching for: {product_name}")

        # check whether the product from customer's shopping list is matches with the shop stock list of products
        match_exist = 0  # initialy set to zero, assuming there is no match

        # Iterate through shop stock list to match items from customer's shopping list
        for sh_item in sh.stock:

            # initialise auxiliary variable
            sub_total = 0  # sub total cost for items from the shopping list

            # for testing - ok
            # print(f"test 5: item in shop: {sh_item.product.name}") # for testing - ok

            # assign the j-th product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # product found in shop, proceeding...
            if (product_name == sh_item_name):  # true, if both product names are identical

                match_exist += 1  # set to one, meaning there is a matach

                quantity = int(input("Enter desired quantity: "))

                # check products availability
                # sufficient amount of the product in the shop stock
                if (quantity <= sh_item.quantity):

                    # check product price and calculate sub-total cost(price*qty)
                    sub_total = sh_item.product.price * quantity

                    # check if customer can afford it
                    if (budget >= sub_total):

                        # update customer's budget
                        budget = budget - sub_total
                        print(
                            f"Bought! Sub total cost was €{sub_total:.2f}. Budget after buying this item: €{budget:.2f}.")

                        # update the shop stock(full order fulfilled)
                        sh_item.quantity = sh_item.quantity - quantity

                        # update the shop cash
                        sh.cash = sh.cash + sub_total
                        print(
                            f"Stock quantity of {sh_item_name} in shop updated to: {sh_item.quantity:.0f}. Cash in shop now: {sh.cash:.2f}.")

                    else:  # customer cannot afford all
                        print(
                            f"Unfortunately, you do not have enough money for that many - short of €{(sub_total - budget):.2f}. ", end="")
                        print(
                            f"Come back with more money or reduce the quantity.")

                # customer wants more than in stock
                else:
                    # check how many can be bought and buy all that is in stock
                    partial_order_qty = quantity - \
                        (quantity - sh_item.quantity)

                    # perform the sub-total cost for the item
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price  # partial qty * price
                    # Prints out cost of all items of the product
                    print(
                        f"Only {partial_order_qty:.0f} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ")

                    # update customer's budget
                    budget = budget - sub_total_partial
                    print(
                        f"Budget after buying this item: €{budget:.2f}.")

                    # update the shop stock(partial order) and cash
                    sh_item.quantity = sh_item.quantity - partial_order_qty

                    # update the shop cash
                    sh.cash = sh.cash + sub_total_partial
                    print(
                        f"This product is no longer avilable in shop (stock: {sh_item.quantity:.0f}). Cash in shop now: {sh.cash:.2f}.")

        if (match_exist == 0):  # product not available in stock
            print("Product not found in shop.")


# ----- ----- ----- ----- -----
# Print out of the shop details
# ----- ----- ----- ----- -----


def print_shop(sh):  # takes 'shop' dataclass as a parameter
    # Show shop detials
    # print(sh)  # for testing - ok
    print(f"\nShop has {sh.cash:.2f} in cash")
    print("==== ==== ====")
    for item in sh.stock:
        print_product(item.product)
        print(f"Available amount: {item.quantity:.0f}")


# ----- ----- ----- ----- -----
# The shop main menu
# ----- ----- ----- ----- -----

separator = "=" * 15


def display_menu():

    print("")
    print(separator)
    print("Shop Main Menu (Python procedural):")
    print(separator)
    print("1 - Shop status")
    print("2 - Customer A - good case")
    print("3 - Customer B - insufficient funds case")
    print("4 - Customer C - exceeding order case")
    print("5 - Interactive mode")
    print("9 - Exit application\n")
    print("NB: The sequence of the customers being processed might affect the initial case of the customers.")
    print(separator)


# ----- ----- ----- ----- -----
# The main function - start of the program
# ----- ----- ----- ----- -----


def shop_menu(shop):
    '''
    Shop menu
    '''

    # Main menu screen
    display_menu()

    while True:  # this is a 'forever' loop, unless interupted (break)

        # Request input from the user, assign to variable choice
        choice = input("Enter your choice: ")

        if (choice == "1"):
            # print("inside option 1\n") # for testing - ok
            print_shop(shop)
            display_menu()

        elif (choice == "2"):
            # print("inside option 2\n") # for testing - ok

            # create customer A struct (good case)
            customer_A = create_customer(
                "Data/customer_good.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_A, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_A, shop, total_cost)

            display_menu()

        elif (choice == "3"):
            # create customer B struct (good case)
            customer_B = create_customer(
                "Data/customer_insufficient_funds.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_B, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_B, shop, total_cost)

            display_menu()

        elif (choice == "4"):
            # create customer C struct (good case)
            customer_C = create_customer(
                "Data/customer_exceeding_order.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_C, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_C, shop, total_cost)

            display_menu()

        elif (choice == "5"):

            # Welcoming message
            print("\nInteractive shopping mode")
            print("-------------------------")

            # get user's name
            customer_name = input("What's your name, good customer?: ")
            print(f"Welcome, {customer_name}. ")

            # get user's budget
            budget = float(
                input("Enter your budget: "))

            # go to the interactive mode
            interactive_mode(shop, budget)

            display_menu()

        elif (choice == "9"):  # Exit condition
            print("")
            break

        else:
            display_menu()


'''
# ===== ===== ===== ===== ===== =====
# The main function - start of the program
# ===== ===== ===== ===== ===== =====
'''


def main():
    '''
    This is the main function the program. It defines a starting point and controls all other functionality of the program. It is called automatically at the program start.
    '''

    # Clear screen
    os.system("cls")   # for Windows systems
    os.system("clear")  # for Linux systems

    print("\n\n>>> Multi-Paradigm Programming Project by Andrzej Kocielski, 2020 <<<")

    '''
    Create shop only once, upon the program start
    '''
    shop_one = create_and_stock_shop()  # assign data from a file to variable shop_one.
    # print(shop_one) # for testing - ok

    shop_menu(shop_one)  # calls function that displays the shop menu


'''
# ===== ===== ===== ===== ===== =====
# Check dependencies
# ===== ===== ===== ===== ===== =====
'''

if __name__ == "__main__":
    # execute only if run as a script
    main()