from dataclasses import dataclass, field
from typing import List
import csv
import os 
import time
import itertools

@dataclass
class Product:
    name:str 
    price:float = 0.00
    
    
class ProductStock:
    product:Product 
    quantity:int 
    
@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)
    
    

@dataclass
class Customer:
    name: str = '' 
    budget:float = 0.0 
    shopping_list: List[ProductStock] = field(default_factory=list)
    
    
def clear():
    os.system('clear')
    
def create_and_stock_shop():
    s = Shop()
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="")
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
    return s


def print_Product(p):
    (f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: €{p.price}')
    
def print_shop(s):
     print(f'Shop has €{s.cash} in cash')
     for item in s.stock:
         print_Product(item.product)
         print(f"the shop has the following amount of items in shop")

def menu_return():
    print("-------------------------------")
    menu = input("Press any key to return to shop menu")
    if True:
        menu_return()
         

def show_menu(s):     
    print("Welcome to the ATU shop")
    print("--------")
    print("MENU")
    print("====")
    print("Please select from one of the following")
    print("1  Customer Menu")
    print("2 Live mode")
    print("3 batch mode")
    print("x  Exit application")
    
    
def print_customer(c, s):
    print("-------------\n")
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    print("------------------")
    print("This is your customer order")
    orderCost = [] 
    
def create_order(c, s):
    print("creating your order")
    print("------------------")
    totalProductCost = 0 
    for item in c.shopping_list:
        for prod in s.stock:
            if item.product.name == prod.product.name: 
                if prod >= item.quantity: 
                    totalProductCost = item.quantity * prod.product.price
                    if c.budget >= totalProductCost:
                        s.cash += totalProductCost
                        c.budget -= totalProductCost
                        print(f"€{totalProductCost} deducted from the customer funds for {item.quantity} of {item.product.name}.\n")
                        prod.quantity -= item.quantity
        
    
    
    

     



