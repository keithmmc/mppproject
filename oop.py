import sys
import csv
import os # to clear screen

# create a Product class, give it a repr method
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f'PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}'
# create a ProductStock 
class ProductStock:

    def __init__(self, product, quantity):
        self.product = product # product is a class
        self.quantity = quantity # quantity is a float - a primitive. Methods cannot be invoked on primitives
    # getter method for getting product name
    def name(self):
        return self.product.name
    # getter method for getting product price
    def unit_price(self):
        return self.product.price

    # method for calculate cost   
    def cost(self):
        return self.unit_price() * self.quantity

    # a getter method to get the quantity of a stock item
    def get_quantity(self):
        return self.quantity

    # a setter method to update the quantity of a product for each quantity of stock sold
    def set_quantity(self, saleQty):
        self.quantity -= saleQty

    # a getter method to access the product
    def get_product(self):
        return self

    # a repr method to print the product, uses the product repr method
    def __repr__(self):

        # self.product is an instance of the product a class 
        return f"{self.product}\nThe shop has {self.quantity} in stock \n-------------"
 
## Define a customer class
class Customer:
    # define the constructor 
    def __init__(self):
        self.shopping_list=[]
        self.filename= input("Please enter the name of the customer file\t")
        self.status = True
        
        path = "../" + str(self.filename) + ".csv"
        
    #try: # same as i am doing in procedural python
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
                    #sys.exit()
            
     # a method to calculate customer costs   
    def calculate_costs(self, price_list):
            # each shop_item is a productStock
        for shop_item in price_list:
            # iterate through the customer shopping list 
            for list_item in self.shopping_list:
                # check if the item name matches a shop item
                if (list_item.name() == shop_item.name()):
                    # if so pull out the price
                    list_item.product.price = shop_item.unit_price()
    # a method for calculating item cost
    def order_cost(self):
        cost = 0
        # going through the customer shopping list of productStocks  and getting out the cost
        for list_item in self.shopping_list:
            # get the cost using the ProductStock cost method
            cost += list_item.cost()
        return cost

# A repr method returns a state based representation of the class 
    def __repr__(self):
        print(f'CUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: €{self.budget}')
        print("-------------\n");

        # just print the actual customer order from the file first
        for item in self.shopping_list:
            print(item.product)
            print(f"{self.name} ORDERS {item.quantity} OF ABOVE PRODUCT\n*************************")
        # now printing the product with price if we stock the item only
        print("We have the following items in stock:")   
        str = ""
        for item in self.shopping_list:
            price = item.product.price
            # don't print for items we don't stock
            if price !=0:
                str += f"{item.quantity} units of {item.name()} at €{price} per unit for cost of €{item.cost()}\n\n"
                
        return str 

# create a subclass of customer so the live customer can use all the customer functionality
class Live(Customer):
    def __init__(self):
        self.shopping_list=[]
        self.name = input("please enter your name\t")
        print(f"Welcome to the shop {self.name}")

        while True:
            try:
                self.budget = float(input("please enter your budget\t"))
                break
            except ValueError:
                print("Please enter your budget as an number\t")
        product = input("Please enter the product you are looking for. Please note product name is case sensitive. \t")

        # capture inappropiate values
        while True:
            try:
                quantity = int(input(f"Please enter the quantity of {product} you are looking for. \t\t"))
                break

            except ValueError:
                print("Please enter the quantity as an integer")
        
        p = Product(product)
        ps = ProductStock(p, quantity)
        self.shopping_list.append(ps)

############## ################## Shop class  ####################  ######################  
#  the shop takes a customers basket, checks stock, calculcates cost, updates stock, updates cash
       
class Shop:
    # 
    def __init__(self, path):
        # set up an array to read in the stock to
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)

    # a representation method for the shop
    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash} in cash\n'
        # loop over the stock items, each item is class ProductStock
        for item in self.stock:
            str += f"{item}\n"
        return str        

      ### def process_order, takes in a customer 
    def process_order(self,c):
        print("PROCESSING ORDER...")
        print("-------------------")
        self.totalProductCost = 0 

        for  list_item in c.shopping_list:
            # call the method to check stock
            self.check_stock(list_item)
            # call the method to update cash or not
            self.update_cash(c)
            # call method to update stock based on quantities in stock as checked by check_stock method
            self.update_stock(self.product)
        print("UPDATING CASH\n-------------------")
        print(f"Customer {c.name} has €{c.budget} left")


    # a method to update the cash of the shop and the customer if the customer has the ability to pay         
    def update_cash(self,c):
        # a boolean used by the method to update stock or not. Stock only updated if customer can pay
        self.process = False
        # checking ability of customer to pay, then update the shop cash and customer cash if they can
        if c.budget >= self.totalProductCost:
            self.cash += self.totalProductCost
            c.budget -= self.totalProductCost
            # only print for actual sale quantities
            if self.saleQty>0:
                print(f"€{self.totalProductCost} deducted from the customer funds for {self.saleQty} unit(s) of {self.product.name()}.\n")
            # to indicate to the update stock method that the stock should be updated to reflect sale          
            self.process = True
            # if customer cannot pay, then sale does not go ahead. 
        elif c.budget < self.totalProductCost:
            print(f"Insufficient funds, Customer has €{c.budget} but €{self.totalProductCost} required for {self.saleQty} unit(s) of {self.product_name}\n")
           
    # a method to check stock, compare customer items to shop stock items
    def check_stock(self,list_item):
        # checking the stock
        for shop_item in self.stock:
            # if the shop does stock the customer item
            if (list_item.name() == shop_item.name()): 
                # assign the 
                self.product_name = shop_item.name()
                #get the product stock detials and return the product for the update stock method to use
                self.product = shop_item.get_product()
                # checking if there is enough stock 
                if list_item.quantity <= shop_item.quantity:
                    # total product cost based on quantity customer wants as we have enough
                    self.totalProductCost = list_item.quantity *shop_item.product.price
                    # store the sale quantity for use later
                    self.saleQty = list_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
                    
                # checking if the customer order quantity is more than we have in stock
                elif (list_item.quantity > shop_item.quantity):
                    print(f"We only have {shop_item.quantity} of {shop_item.name()} at the moment. You will be charged only for the products sold.\n");
                    # total product cost is based on partial order if thats all that is available
                    self.totalProductCost = shop_item.quantity *shop_item.product.price
                    self.saleQty = shop_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
            # if the customer product is not stocked, sale quantity is zero and no cost to customer. Avoid printing out later
            if (list_item.name() != shop_item.name()):
                self.product = list_item
                self.saleQty =0
                self.totalProductCost =0
                
    # a method to update stock
    def update_stock(self, product):
        # only update stock if the customer can pay, otherwise a sale does not take place
        if self.process == True:
            # call ProductStock methods to update the quantity in stock
            product.set_quantity(self.saleQty)
            

    def show_menu(self):
        while True:
    # clear the screen of previous input
    #clear()
            print("\n")
            print("\n")
            print("\t\tWelcome to the atu shop\n")
            print("\t\t----------------------------------")
            print("\t\tSelect 1 for Shop Overview")
            print("\t\tSelect 2 for Batch orders")
            print("\t\tSelect 3 for Live orders")
            print("\t\tSelect 0 to Exit Shop Application")

            self.choice = input("\n Please select option from the main menu:")
            if (self.choice =="1"):
                print("1: SHOP OVERVIEW")
                
                print(self)
                self.return_to_menu()

            elif (self.choice =="2"):    
                    
                print("2: BATCH ORDERS\n")
                # create a customer object 
                c = Customer()
                if c.status == False:
                    self.return_to_menu()

                # call calculate method on the customer with shop stock as input
                c.calculate_costs(self.stock)
                # print the customer
                print(c)
                # process the order using customer object as input
                self.process_order(c)
                self.return_to_menu()

            elif (self.choice=="3"):            
                print("3: *** LIVE MODE ***")
                # create a customer object by calling the live class
                c = Live()
                # call calculate method on the live customer object with shop stock as input
                c.calculate_costs(self.stock)
                print(c)
                # process the order with the customer object as input
                self.process_order(c)
                self.return_to_menu()


            elif(self.choice =="0"):
                print("\nThank you for shopping here. Goodbye")
                # to exit straight out of the program as this is part of the shop class
                sys.exit()
            
            else:
                print("Please choose an option from the menu")
                self.show_menu()
                
    # a method to return to menu
    def return_to_menu(self):
        menu = input("\n Hit any key to return to main menu")
        if True:
            self.show_menu()

def clear():
    os.system('clear')   

# the main method just creates a shop object 
def main():
    print("Setting up the shop for today ...\n")
    s = Shop("stock.csv")
    s.show_menu()
        
if __name__ == "__main__":
    # clear the screen
    clear()
    # call the main method
    main()
        
    