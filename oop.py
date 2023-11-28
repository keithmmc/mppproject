import sys 
import csv 
import os 

##creating a class for product 
class Product:
    def __init__(self, name, price=0):
        self.name = name
        self.price = price 
        
    def __repr__(self):
        return f'PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}'
    
##creating a class for product stock 

class ProductStock:
    def __init__(self, product, quantity):
        self.product = product 
        self.quantity = quantity
    def name(self):
        return self.product.name 
    def unit_price(self):
        return self.unit_price
    def cost(self):
        return self.unit_price() * self.quantity

    def get_quantity(self):
        return self.quantity
    
    
    def set_quantity(self, saleQty):
        self.quantity -= saleQty
        
    def get_product(self):
        return self 
    
    def __repr__(self):
         return "{self.product}\nThe shop has {self.quantity} in stock"
     
class Customer:
    def __init__(self):
        self.shopping_list = []
        self.filename = input("Please enter your name and your customer file")
        self.status = True
        path = " " + str(self.filename) + ".csv"
        
        while self.status:   
            try:
                with open(path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    first_row = next(csv_reader)
                    self.name = first_row[0]
                    self.budget = float(first_row[1])
                    for row in csv_reader:
                        name = row[0]
                        quantity = float(row[1])
                        p = Product(name)
                        ps = ProductStock(p, quantity)
                        self.shopping_list.append(ps)
                    return
            # in case invalid csv file entered
            except Exception as err:
                    print("Invalid customer file name. ") 
                    # should return to the menu here same as pp versions
                    self.status=False
                    
                    return 
                
def costs_calculate(self, price_list):
    for shop_item in price_list:
        for list_item in self.shopping_list:
            if list_item.name() == shop_item():
                list.item.product.price = shop_item.unit_price()
                
def order_cost(self):
    cost = 0 
    for list_item in self.shopping_list:
        cost += list_item.cost()
        return cost

# A repr method returns a state based representation of the class 
    def __repr__(self):
        print(f'CUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: €{self.budget}')
        print("-------------\n")
        for item in self.shopping_list:
            print("item.product")
            print(f"{self.name} ORDERS {item.quantity} OF ABOVE PRODUCT\n*************************")
        # now printing the product with price if we stock the item only
        print("We have the following items in stock:")  
        str = '' 
        for item in self.shopping_list:
            price = item.product.price
            if price !=0:
                str += f"{item.quantity} units of {item.name()} at €{price} per unit for cost of €{item.cost()}\n\n"
                
        return str 
            
class Live(Customer):
    def __init__(self):
        self.shopping_list = []
        self.name = input('Hi can you please your enter your name')
        print("Welcome to the ATU shop {self.name}")
        while True:
            try:
                self.budget = float(input("can you please enter your budget"))
                break
            except ValueError:
                print("Please enter your budget as an number")
        product = input("Please enter the product you are looking for. Please note product name is case sensitive")
        while True:
            try:
                quantity = int(input(f"Please enter the quantity of {product} you are looking for"))
                break

            except ValueError:
                print("Please enter the quantity as an integer")
        
        p = Product(product)
        ps = ProductStock(p, quantity)
        self.shopping_list.append(ps)

class Shop:
    def __init__(self, path):
        self.stock = [] 
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
                
def __repr__(self):
    str = ""
    str += 'Shop has €{self.cash} in cash'
        # loop over the stock items, each item is class ProductStock
    for item in self.stock:
            str += "{item}"
    return str 

def process_order(self,c):
    print("we are processing your order")
    self.totalProduct = 0 
    for list_item in c.shopping_list:
        self.check_stock(list_item) 
        self.update_cash(c)     
        self.update_stock(self.product)
        print("UPDATING CASH\n-------------------")
        print("Customer {c.name} has €{c.budget} left")
        
def update_cash(self,c):
    self.process = False 
    

            
            
def main():
    print("Welcome to the ATU shop ...\n")
    s = Shop("stock.csv")
    s.display_menu()
        
if __name__ == "__main__":
    # clear the screen
    clear()
    # call the main method
    main()
        
        
    