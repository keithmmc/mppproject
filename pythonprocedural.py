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
    
    
    

     



