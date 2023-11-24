from dataclasses import dataclass, field
from typing import List
import csv
import os 
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

def read_customer():
    path = input("you can upload your customer file here to be processed")
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
        print("you have uploaded the wrong customer file.")
        # return the user to the menu
        show_menu()
        

def show_menu(): ## this is a function to show the menu and list the options
    clear() ## this will clear the screen 
    print("-----------------------") 
    print("Welcome to the ATU shop")
    print("please select 1 for the shop overview")
    print("please select 2 for all batch orders")
    print("please select 3 to place a live order for shop")
    print("please select 4 to leave the shop")
    
    
def process_order(c,s): ## this function will process a order for the shop 
    print("--------------------------")
    print("we are processing your order")
    print("---------------------------")
    totalProductCost = 0 
    # creating a loop to go through all the orders in the customers shopping list 
    for item in c.shopping_list:
        #going to check each item against the shops stock 
        for prod in s.stock:
            #checking in the item is in stock in the shop 
            if item.product.name == prod.product.name:
                #checking if the quantity will be enough to fulfill an order 
                if prod.quantity >= item.quantity:
                    totalProductCost = item.quantity * prod.product.price 
                if c.budget >= totalProductCost:
                    s.cash += totalProductCost
                    s.cash -= totalProductCost
                    print(f"€{totalProductCost} will be deducted from your funds for {item.quantity} of {item.product.name}.\n")
                    prod.quantity -= item.quantity
                elif c.budget < totalProductCost:
                     print(f"You have insufficient funds, you only have €{c.budget} but you need €{totalProductCost} to pay for {item.product.name}")
                        # no purchase takes place, pass
                c.budget -= 0 
            elif prod.quantity < item.quantity:
                 print(f"We only have the following {prod.quantity} of {prod.product.name} at the moment. You will be charged only for the products sold.\n")
                 totalProductCost = prod.quantity * prod.product.price
                 if c.budget >= totalProductCost:
                      print(f"€{totalProductCost} will br deducted from your funds for {prod.quantity} unit(s) of {item.product.name}.\n")                 
                 prod.quantity += prod.quantity 
                 s.cash += totalProductCost
                 c.budget -= totalProductCost
            elif c.budget < totalProductCost:
                  print(f"Insufficient funds, Customer has €{c.budget} but €{totalProductCost} required for {item.product.name}\n")
                        # no purchase takes place, pass
            c.budget -= 0
    print(f"UPDATING CASH\n-------------------\nCustomer {c.name} has €{c.budget} left\n.")
    
def print_customer(c,s):
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    print("printing customer order")
    orderCost = [] 
    for item in c.shopping_list:
        print_product(item.product)
        print(f"{c.name} ORDERS  {item.quantity} OF THE ABOVE PRODUCT\n")
    for item in c.shopping_list:
        for prod in s.stock:
            print("We are checking the stock of the shop please wait")
            print("----------------------------------------------------")
            print("the shop has got the following items currently in stock")
            for item in c.shopping_list:
                for prod in s.stock:
                    if item.product.name == prod.product.name: 
                        cost = item.quantity * prod.product.price
                orderCost.append(cost)
                
                print(f"{item.quantity} units of {item.product.name} at €{prod.product.price} per unit for cost of €{item.quantity *prod.product.price }\n")

def live_order(s): ## the following is a function that will complete a live order for shop 
    shopping_list = [] 
    c=Customer()
    c.customerName = input("Can you please enter your name")   
    print("hello and welcome to the ATU shop.{c.name}")      
    while True:
        try:
            c.budget = float(input("please enter your budget  \t"))
            break
        # in case a float is not entered
        except ValueError:
            print("Please enter your budget as an number")
    # get product name from customer and store as a Product 
    product  = input("Please enter the name of the product you are looking for. Please note product name is case sensitive")
    p = Product(product)

    # ask customer for quantity of item, ensure an integer is accepted
    while True:
        try:
            quantity = int(input(f"Please enter the quantity of {product} you are looking for "))
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

def clear():
    os.system('clear')
    
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: €{p.price}')
    
def print_shop(s):
    print(f'Shop has €{s.cash} in cash')
    for item in s.stock:
        # call print_product to print out each product name, price and quantity
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print('-------------')
    
def main():
    clear() 
    print("welcome to the ATU shop")
    s = create_and_stock_shop()
    while True:
        show_menu()
        selection = input("please enter the option your looking for from the menu")
        if (selection =="1"):
            print("1: SHOP OVERVIEW")
            print_shop(s)
            show_menu() 
        elif (selection =="2"):
            print("2 batch orders")
            c = read_customer()
            if c:
                print_customer(c,s)
                process_order(c,s)
            show_menu()
        elif (selection=="3"):            
            print("3:*** LIVE MODE ***")
            print("Please choose from our products listed below")
            print_shop(s)
            c =live_order(s)
            # print customer details
            print_customer(c,s)
            # process the customers order
            process_order(c,s)

            # return to menu
            show_menu() 

        # if user selects 0, this signals they wish to exit the program
        elif (selection == "0"):
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
       



    