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
    
def read_customer(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 
        


def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

def print_customer(c):
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    
    for item in c.shopping_list:
        print_product(item.product)
        
        print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
        cost = item.quantity * item.product.price
        print(f'The cost to {c.name} will be €{cost}')
        
def print_shop(s):
    print(f'Shop has €{s.cash} in cash')
    for item in s.stock:
        # call print_product to print out each product name, price and quantity
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print('-------------')
        

c = read_customer("customer.csv")
print_customer(c)

def show_menu(): 
    menu = input("press any key to return to the shop")   
    if True:
        show_menu()
        

        
    
def show_menu():
    print("-----------------")
    print("Welcome to the ATU shop")
    print("\t\tSelect 1 for Shop Overview")
    print("\t\tSelect 2 for Batch orders")
    print("\t\tSelect 3 for Live orders")
    print("\t\tSelect 0 to Exit Shop")
    
def clear():
    os.system('clear')
    
    
def live_order(s):
    shopping_list = [] 
    c=Customer()
    c.name=input("please enter your name to place order")
    print(f"You are welcome to the ATU shop")
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
    while True:
        try:
            quantity = int(input(f"Please enter the quantity of {product} you are looking for \t\t"))
            break
        except ValueError:
            print("Please enter the quantity as an integer this time")
    ps = ProductStock(p, quantity)
    print("please wait we are checking this out")
    c.shopping_list.append(ps)
    return c 

def clear():
    os.clear('clear')
 
def main():
    print("shop is open for orders today") 
    s = create_and_stock_shop
    while True: 
        show_menu()
        choice = input("\n Please select one of the options from the menu")
        if(choice == 1):
            print("shop overview")
            print_shop(s)
            show_menu() 
        elif(choice == 2):
            print("batch orders")
            c = read_customer()
            if c:
                print_customer(c,s)
                process_order(c,s)
                show_menu() 
                
                

        

        # if option 3 chosen, create customer by calling the live_order function   
        elif (choice=="3"):            
            print("3:*** LIVE MODE ***")
            print("Please choose from our products listed below")
            print_shop(s)
            c = live_order(s)
            # print customer details
            print_customer(c,s)
            # process the customers order
            process_order(c,s)

        

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
                

     



