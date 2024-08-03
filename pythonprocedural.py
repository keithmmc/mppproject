from dataclasses import dataclass, field
from typing import List
import csv
import os # need this to clear the screen. Only use if there is an equavalent for C!
import time
import itertools

# Product is a data container here only. 
# This is equivalent to the product Struct in C
@dataclass
class Product:
    name: str
    price: float = 0.0

# This is equivalent to the ProductStock Struct in C
@dataclass 
class ProductStock:
    product: Product
    quantity: int

# A data container for a Shop
@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

# A data container for a Customer
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)


# clear the screen
def clear():
    os.system('clear')

def create_and_stock_shop():
    # Shop is a dataclass with cash (float) and stock (list of productStock)
    s = Shop()
    # read in csv file and get shop cash from first row
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        # iterate through the rows of the csv file creating Product, ProductStock and shop stock using the 
        # data classes defined earlier.
        for row in csv_reader: 
            p = Product(row[0], float(row[1])) 
            # ProductStock            
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
    # return the shop dataclass
    return s

#   read in customer csv file, customer enters file name only
def read_customer():
    path = input("Please upload your customer file name...")
    # create a file name including the file path
    path = "../" + str(path) + ".csv"
    try:
        # open and read the csv file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            # customer name is col 0 of row 0, customer budget is col 1 of row 0
            c = Customer(first_row[0], float(first_row[1]))
            # iterate through the rest of the rows of the file (after the first row)
            for row in csv_reader:
                # product name is the first col
                name = row[0]
                # product quantity is the second column
                quantity = float(row[1])
                # Product is a dataclass with name (str) and price (float)
                p = Product(name)
                # ProductStock is a dataclass with Product (a dataclass with product name and price)
                ps = ProductStock(p, quantity)
                # ps will have Product name, Product price and a quantity
                c.shopping_list.append(ps)
            return c 
    # in case an invalid file name has been entered
    except Exception as err:
        print("Invalid customer file name. ")
        # return the user to the menu
        return_to_menu()
        
# Takes in a product and prints out the price
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: €{p.price}')
    
# This function prints the cash in the shop  and each 
def print_shop(s):
    print(f'Shop has €{s.cash} in cash')
    for item in s.stock:
        # call print_product to print out each product name, price and quantity
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print('-------------')

# define a function to return to menu after a key is pressed
def return_to_menu():
    menu = input("\n Hit any key to return to main menu")
    if True:
        show_menu()

# a function to display the menu options       
def show_menu():
    # clear the screen of previous input
    clear()
    print("\n\n")
    print("\t\tWelcome the atu shop\n")
    print("\t\t----------------------------------")
    print("\t\tSelect 1 for Shop Overview")
    print("\t\tSelect 2 for Batch orders")
    print("\t\tSelect 3 for Live orders")
    print("\t\tSelect 0 to Exit Shop Application")

# a function to actually process the order
def process_order(c,s):  
    print("Processing order...")
    print("-------------------")
    totalProductCost = 0 
    # go through each item in customer shopping list
    for item in c.shopping_list:
        # check against each item in shops stock
        for prod in s.stock:
            # if the item is a shop stock item
            if item.product.name == prod.product.name:
                # check if the quantity in stock is enough to fill the order
                if prod.quantity >= item.quantity:
                    # calculate cost
                    totalProductCost = item.quantity * prod.product.price
                    # check customer has enough cash to cover the cost of this purchase
                    if c.budget >= totalProductCost:
                        # process sale, update shop cash
                        s.cash += totalProductCost
                        # process sale, update customer cash
                        c.budget -= totalProductCost
                        # process sale, decrease stock quantity of sold items
                        print(f"€{totalProductCost} deducted from the customer funds for {item.quantity} of {item.product.name}.\n")
                        prod.quantity -= item.quantity

                    elif c.budget < totalProductCost:
                        print(f"You have insufficient funds, you only have €{c.budget} but you need €{totalProductCost} to pay for {item.product.name}")
                        # no purchase takes place, pass
                        c.budget -=0
                
                # if quantity in stock is less than what the customer wants
                elif prod.quantity < item.quantity:
                    print(f"We only have {prod.quantity} of {prod.product.name} at the moment. You will be charged only for the products sold.\n");
                    # calculate cost based on partial order 
                    totalProductCost = prod.quantity * prod.product.price
                    # check if customer has enough cash to pay
                    if c.budget >= totalProductCost:
                        print(f"€{totalProductCost} deducted from the customer funds for {prod.quantity} unit(s) of {item.product.name}.\n")                 
                        # process sale, decrease stock
                        prod.quantity -= prod.quantity
                        # process sale, increase shop cash as a result of sale
                        s.cash += totalProductCost
                        # deduct sale amount for this item from customer wallet
                        c.budget -= totalProductCost  
                    # if customer does not have enough to pay        
                    elif c.budget < totalProductCost:
                        # You have insufficient funds, you only have €{c.budget} but you need €{self.totalProductCost} to pay for this item"
                        print(f"Insufficient funds, Customer has €{c.budget} but €{totalProductCost} required for {item.product.name}\n")
                        # no purchase takes place, pass
                        c.budget -=0
    print(f"UPDATING CASH\n-------------------\nCustomer {c.name} has €{c.budget} left\n.")


# takes in a customer c read in from the csv file (called from the batch function)
def print_customer(c,s):
    
    # print customer name
    
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    print("-------------\n")
    # goes through the customer's shopping list and calls the print_product function to print the product name and price
    print("CUSTOMER ORDER:")
    orderCost =[]
    # loop through items on customer shopping list
    for item in c.shopping_list:
        # loop through items in shop stock
        print_product(item.product)
        print(f"{c.name} ORDERS  {item.quantity} OF ABOVE PRODUCT\n")
        print("*************************")

    print("Please wait while we check our stock...\n")
    print("-----------------------------------------")
    print("We have the following items in stock:\n")
    for item in c.shopping_list:
        for prod in s.stock:
            # comparing items to see if we have the item in stock
            if item.product.name == prod.product.name:
                # call the print product method to print the price
                #print_product(prod.product)
                cost = item.quantity * prod.product.price
                orderCost.append(cost)
                #print(f" €{prod.product.price} per unit.")
                print(f"{item.quantity} units of {item.product.name} at €{prod.product.price} per unit for cost of €{item.quantity *prod.product.price }\n")


# a function to deal with live customer orders        
def live_order(s):
    # intialise an array to hold the shopping list
    shopping_list = []
    c=Customer()
    
    c.name = input("Please enter your name \t")
    print(f"Welcome to the shop.{c.name}")
    while True:
        try:
            # asks customer for their budget and stores in 
            c.budget = float(input("please enter your budget  \t"))
            break
        # in case a float is not entered
        except ValueError:
            print("Please enter your budget as an number")
    # get product name from customer and store as a Product 
    product  = input("Please enter the name of the product you are looking for. Please note product name is case sensitive\t\t")
    p = Product(product)

    # ask customer for quantity of item, ensure an integer is accepted
    while True:
        try:
            quantity = int(input(f"Please enter the quantity of {product} you are looking for \t\t"))
            break
        # in case an integer is not entered
        except ValueError:
            print("Please enter the quantity as an integer")
    # create a ProductStock using the product and quantity
    ps = ProductStock(p, quantity)    
    print("Please wait while we check")
    # append the items to the customers shopping list
    c.shopping_list.append(ps)
    # return a customer
    return c

# a function to clear the screen for readability
def clear():
    os.system('clear')

# the main program calls the functions above to create the shop, print the shop, create customers from csv and live
# process the customer orders if possible and update the shop stock and cash state

def main():
    # clear screen
    clear()
    print("Setting up the shop for today ...\n")
    # create the shop by calling this function
    s = create_and_stock_shop()
 
    # a forever loop 
    while True:
        # display the user menu
        show_menu()
        # store input as choice
        choice = input("\n Please select option from the main menu:")

        # if option 1 selected, print the current shop state by calling print_shop
        if (choice =="1"):
            print("1: SHOP OVERVIEW")
            print_shop(s)
            return_to_menu()    

        # if option 2 selected, ask user for their customer file
        elif (choice =="2"):    
            
            print("2: BATCH ORDERS")
            # create customer 
            c = read_customer()
            # if a customer has been created, print their order
            if c:
                print_customer(c,s)
                # process the customers order
                process_order(c,s)

            return_to_menu() 

        # if option 3 chosen, create customer by calling the live_order function   
        elif (choice=="3"):            
            print("3:*** LIVE MODE ***")
            print("Please choose from our products listed below")
            print_shop(s)
            c =live_order(s)
            # print customer details
            print_customer(c,s)
            # process the customers order
            process_order(c,s)

            # return to menu
            return_to_menu() 

        # if user selects 0, this signals they wish to exit the program
        elif (choice == "0"):
            # exit clause to break out out of the entire program and back to the command prompt
            print("\nThank you for shopping here. Goodbye.")
            break

    ## for anything else, display the menu
        else: 
            show_menu()

if __name__ == "__main__":
    # only execute if run as a script

    # call the main function above
    main()
       



    