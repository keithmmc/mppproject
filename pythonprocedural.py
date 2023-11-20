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
        return_to_menu()
        

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
                    



    