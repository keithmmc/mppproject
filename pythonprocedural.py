from dataclasses import dataclass, field
from typing import List
import csv
import os


@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    product: Product
    quantity: int

@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)
    
def clear():
    os.system('clear')

def create_and_stock_shop():
    s = Shop()
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s

def create_customer(file_path):
    customer = Customer()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        customer = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            customer.shopping_list.append(ps)
            return customer

def print_customers_details(cust, sh):
    # Values of cust.name and cust.budget are referring to customer's details defined the dataclass instance (within 'Main' method).
    print(f"\nCustomer name: {cust.name}, budget: €{cust.budget:.2f}")
    print(f"---- ---- ----")
def print_product(prod):
    # if the price is defined (we are showing the shop stock), then both name and price are shown otherwise(we are showing the customer shopping list) only product name is showm
    if prod.price == 0:
        print(f"Product: {prod.name};")
    else:
        print(f"Product: {prod.name}; \tPrice: €{prod.price:.2f}\t", end="")
         # initialise auxiliary variables
    total_cost = 0

    # show customer's shopping list
    print(f"{cust.name} wants the following products: ")
    
    for cust_item in cust.shopping_list:
        print(f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")
        sub_total = 0 
        match_exist = 0 
        cust_item_name = cust_item.product_name
        
        for sh_item in sh.stock:
            sh_item = sh_item.product.name 
            if (cust_item_name == sh_item_name):
                match_exist += 1 
                if (cust_item.quantity <= sh_item.quantity):
                    print(f"OK, there is enough in stock and ", end="")
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
                    print(f"\tHowever only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
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


def process_order(cust, sh, total_cost) :
    if (cust.budget < total_cost):
        print('There is enough to make a purchase from shop  short of €{(total_cost - cust.budget):.2f}. ", end="')
    else:
        print("placing your order now please wait while we process your order")
    for cust_item in cust.shopping_list:
        match_exist = 0 
    for sh_item in sh.stock:
        sh_item_name = sh_item.product.name 
        
        
    
 
def display_menu():
    print("")
    print("welcome to the atu shop")
    print("1-shop overview")
    print("2-Customer A- successful")
    print("3-Customer B- no funds")
    print("4-Customer C- Exceeds order")
    print("5-Live mode")
    print("0-To exit this shop")
    
    
    
