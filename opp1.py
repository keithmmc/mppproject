import os
import csv




class Product: # setting up the product class

    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product: {self.name}; \tPrice: {self.price:.2f}"




class Product_stock: # setting up the product stock class 

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    
    def name(self): # the self method for this class
        return self.product.name

    def unit_price(self): # unit price
        return self.product.price

    def cost(self): # getting the cost of the project
        return self.unit_price() * self.quantity

    def __repr__(self):
        # self.product below is an instance of a class 
        return f"{self.product} \tAvailable amount: {self.quantity:.0f}"




class Customer: # customer class The below code reads in the customer CSV file

    def __init__(self, path):
        self.shopping_list = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = Product_stock(p, quantity)
                self.shopping_list.append(ps)

    def get_costs(self, price_list): # getting costs of product
        total_cost = 0
        for list_item in self.shopping_list:
            for shop_item in price_list:
                if (list_item.name() == shop_item.name()):  # if the product is in stock
                    list_item.product.price = shop_item.unit_price()
                    sub_total = list_item.quantity * list_item.product.price
                    total_cost = + sub_total
                    return print(
                        f"(test: {list_item.name()}) OK, there is enough of the product and sub-total would be €{sub_total}")
                else:
                    # print("not in stock, aaaa")
                    pass

    def check_quantity(self, stock_list):
        pass

    def order_cost(self):
        cost = 0

        for list_item in self.shopping_list:
            cost += list_item.cost()

        return cost

    
    def evaluate_order(self, sh): # evaluating the customers order
        
        # Show customers details
        print(f"\nCustomer name: {self.name}, budget: €{self.budget:.2f}")
        print("---- ---- ----")

        print(f"{self.name} wants the following products: ")

        # initialise return variables
        self.total_cost = 0
        self.total_order_list = []  # a new list of items good for making order

        # loop over the items in customer shopping list
        for cust_item in self.shopping_list:
            # print(f"{cust_item.product.name} ORDERS {cust_item.quantity} ")  # for testing - ok

            # Show customers details (example of chain-accessing the data in the nested dataclasses)
            print(
                f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")

            # initialise auxiliary variable
            sub_total = 0  # sub total cost for items from the shopping list

            # control the messages about the customer
            customer_stock_state = 0  # stock check - assume item not available

            # loop shop stock
            for shop_item in sh.stock:

                # check if match exists (the product is in stock)
                if (cust_item.name() == shop_item.name()) and (cust_item.quantity <= shop_item.quantity):

                    # get the product price form shop
                    cust_item.product.price = shop_item.unit_price()
                    sub_total_full = cust_item.quantity * cust_item.product.price  # qty*price

                    # update total cost with the current item
                    sub_total = + sub_total_full

                    # update list of items that are making it for purchasing
                    n = cust_item.name()  # name of product
                    q = cust_item.quantity  # quantity of product
                    p = Product(n)  # a new instance of Product Class
                    sub_order = Product_stock(p, q)  # a new instance
                    self.total_order_list.append(
                        sub_order)  # append the current item

                    # adjust the controller about the customer state
                    customer_stock_state = 1  # stock check - all quantity can satisfied

                # customer wants more than in stock
                elif (cust_item.name() == shop_item.name()) and (cust_item.quantity > shop_item.quantity):

                    # check how many can be bought
                    partial_order_qty = cust_item.quantity - \
                        (cust_item.quantity -
                         shop_item.quantity)  # will buy all that is in stock

                    # perform the cost of the i-th item from the customer's shopping list
                    sub_total_partial = partial_order_qty * \
                        shop_item.product.price  # partial qty * price

                    # update total cost with the current item
                    sub_total = + sub_total_partial

                    # update list of items that are making it for purchasing
                    n = cust_item.name()  # name of product
                    q = partial_order_qty  # quantity of product
                    p = Product(n)  # a new instance of Product Class
                    sub_order = Product_stock(p, q)  # a new instance
                    self.total_order_list.append(
                        sub_order)  # append the current item

                    # Prints out cost of all items of the product
                    customer_stock_state = 2  # stock check - partial quantity can satisfied

                # none in stock
                elif ((cust_item.name() == shop_item.name()) and (shop_item.quantity <= 0)):
                    # Prints out cost of all items of the product
                    customer_stock_state = 0  # stock check - none in stock

                # else:
                    # customer_stock_state = 0  # stock check - none in stock

            # addition of sub totals
            self.total_cost = self.total_cost + sub_total

            if customer_stock_state == 1:
                # stock check - all quantity can satisfied
                print(
                    f"\tOK, there is enough in stock and sub-total cost would be €{sub_total_full:.2f}")
            elif customer_stock_state == 2:
                # stock check - partial quantity can satisfied
                print(
                    f"\tHowever only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
            elif customer_stock_state == 0:
                # stock check - item not available
                print(
                    f"\tThis product is not available. Sub-total cost will be €{sub_total:.2f}.")

        print(
            f"\nTotal shopping cost would be: €{self.total_cost:.2f}. \n")

        # for testing - OK
        # print(f"\nThe following items will be purchased: ", end="")
        # for item in self.total_order_list:
        #     print(f"{item.product.name}, qty: {int(item.quantity)}; ", end="")

        self.total_cost
        self.total_order_list

    def __repr__(self):

        for item in self.shopping_list:
            cost = item.cost()
            str += f"\n{item}"
            if (cost == 0):
                str += f" {self.name} doesn't know how much that costs :("
            else:
                str += f" COST: {cost:.2f}"

        str += f"\nThe cost would be: {self.order_cost():.2f}, he would have {self.budget - self.order_cost():.2f} left"

        return str




class Shop:

    def __init__(self, path):
       
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = Product_stock(p, float(row[2]))
                self.stock.append(ps)

   

    def process_order(self, cust, sh, total_cost, total_order_list):

        # Check whether the customer can afford the desired items
        if (cust.budget < total_cost):  # customer is short of money
            print(
                f"Unfortunately, the customer does not have enough money for all the desired items - short of €{(total_cost - cust.budget):.2f}. ", end="")
            print(
                f"Shopping aborted. Come back with more money or negotiate your shopping list. \n")
        else:  # customer has enough money
            print(f"Processing...")

            # for testing - OK
            # print(f"\nThe following items will be purchased: ")
            # for item in cust.total_order_list:
            #     print(f"{item.product.name}, qty: {int(item.quantity)}; ", end="")
            # print(f"Product index 0: {cust.total_order_list[0].product.name},\tqty: {cust.total_order_list[0].quantity}")

            # loop over the items in the customer shopping list
            for cust_item in cust.total_order_list:
                # check whether the product from customer's shopping list is matches with the shop stock list of products
                match_exist = 0  # initialy set to zero, assuming there is no match

                # assign the i-th product from the customer schopping list as a shorthand
                cust_item_name = cust_item.product.name

                # Iterate through shop stock list to match items from customer's order list
                for sh_item in sh.stock:
                    # assign the j-th product from the shop stock list as a shorthand
                    sh_item_name = sh_item.product.name

                    if (cust_item_name == sh_item_name):  # if both product names are identical
                        match_exist = + 1  # set to one, meaning there is a matach

                        # check whether sufficient amount of the product in the shop stock
                        if (cust_item.quantity <= sh_item.quantity):
                            # update the shop stock(full order)
                            sh_item.quantity = sh_item.quantity - cust_item.quantity
                            print(
                                f"Stock quantity of {cust_item.product.name} updated to: {sh_item.quantity:.0f}")

                        else:  # customer wants more than in stock
                            # buy whole stock of the current item
                            partial_order_qty = cust_item.quantity - \
                                (cust_item.quantity - sh_item.quantity)

                            # print(f"Only quantity {partial_order_qty:.0f} of {cust_item.product.name} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ", end="")
                            # Prints out cost of all items of the product

                            # update the shop stock(partial order)
                            sh_item.quantity = sh_item.quantity - partial_order_qty

                            print(
                                f"Stock quantity of {cust_item.product.name} updated to {sh_item.quantity:.0f}.")

                # if customer wants a product that is not in the shop
                if (match_exist == 0):  # there is no match of product
                    print(
                        f"\tThis product not available. Sub-total cost will be €0.00.")

            # update the cash in shop
            sh.cash = sh.cash + total_cost

            # update the customer's money
            cust.budget = cust.budget - total_cost

            print(f"\nShop has now €{sh.cash:.2f} in cash. ")
            # updated customer's budget
            print(f"{cust.name}'s remaining money is €{cust.budget:.2f}.")
            print("")

 

    def interactive_mode(self, sh, budget):

        # print(f"Budget: {budget:.2f}")  # for testing - ok

        # print shops stock
        print(f"\nThe following products are available in shop:")
        print(self)

        # declare required variables
        product_name = ""
        quantity = 0

        # initialise forever loop until user enter 'x' while typing the product name
        # this is a 'forever' loop, unless interupted (break)
        while product_name != "x":

            print()
            # Request input from the user, assign to the variable
            product_name = input("Enter desired product name (x to exit): ")

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
                                f"Come back with more money or reduce the quantity.\n")

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

   

    def display_menu(self):

        separator = "+" * 15

        while True:  # this is a 'forever' loop, unless interupted (break)

            # Main menu screen
          
            print("1 - Shop status")
            print("2 - Customer A - good case")
            print("3 - Customer B - insufficient funds case")
            print("4 - Customer C - exceeding order case")
            print("5 - Interactive mode")
            print("9 - Exit application\n")
            print("NB: The sequence of the customers being processed might affect the initial case of the customers.")
            print(separator)

            # Request input from the user, assign to variable choice
            choice = input("Enter your choice: ")

            if (choice == "1"):
                # print("in display_menu option 1 ")  # for testing - ok
                # print shop stock)
                print(self)

            elif (choice == "2"):
                # print("    in display_menu option 2 ")  # for testing - ok

                # # create customer A struct (good case) from file
                customer_A = Customer("Data/customer_good.csv")
                # print(customer_A) # for testing

                # # print customer details and evaluate shopping list
                customer_A.evaluate_order(self)

                # total_cost = evaluate_order(customer_A, shop)

                # # process customer's shopping list by calling relevant method
                self.process_order(customer_A, self,
                                   customer_A.total_cost, customer_A.total_order_list)

            elif (choice == "3"):
                # print("    in display_menu option 3 ")  # for testing - ok
                # create customer B struct (good case)
                # read data from a file
                customer_B = Customer(
                    "Data/customer_insufficient_funds.csv")

                # # print customer details and evaluate shopping list
                customer_B.evaluate_order(self)

                # # process customer's shopping list by calling relevant method
                self.process_order(customer_B, self,
                                   customer_B.total_cost, customer_B.total_order_list)

            elif (choice == "4"):
                # print("    in display_menu option 4 ")  # for testing - ok
                # # create customer C struct (good case)
                # read data from a file
                customer_C = Customer("Data/customer_exceeding_order.csv")

                # # print customer details and evaluate shopping list
                customer_C.evaluate_order(self)

                # # process customer's shopping list by calling relevant method
                self.process_order(customer_C, self,
                                   customer_C.total_cost, customer_C.total_order_list)

            elif (choice == "5"):

                # print("   in display_menu option 5 ")  # for testing - ok
                # Welcoming message
                print("\nInteractive shopping mode")
                print("-------------------------")

                # # get user's name
                self.customer_name = input(
                    "What's your name ")
                print(f"Welcome, {self.customer_name}. ")

                # # get user's budget
                self.budget = float(
                    input("Enter your budget: "))

                # # go to the interactive mode
                self.interactive_mode(self, self.budget)

            elif (choice == "9"):  # Exit condition
                print("")
                break

            else:
                print("Wrong key, try again.")
                # display_menu(self)

  

    def __repr__(self):
        str = ""
        str += f"\nShop has {self.cash:.2f} in cash \n==== ==== ====\n"
        for item in self.stock:
            str += f"{item}\n"

        return str




def main(): # main function 

    # Clear screen
    os.system("cls")   # for Windows systems
    os.system("clear")  # for Linux systems

 

    # Create shop only once, upon the program start; assign data from a file to variable shop_one.
    shop_one = Shop("Data/shop_stock.csv")
    # print(shop_one)  # for testing - ok

    # calls function that displays the shop menu
    shop_one.display_menu()


    # deafault customer, provided in the box
    c = Customer("Data/customer.csv")
    c.get_costs(shop_one.stock)
    print(c)
    



if __name__ == "__main__":
    # execute only if run as a script
    main()