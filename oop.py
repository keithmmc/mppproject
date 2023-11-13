import sys
import csv
import os 

class Product:
    def __init__(self, name, price):
        self.name = name 
        self.price = price
        
        def __repr__(self):
             return f'PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}'
         

class ProductStock:
    def __init__(self,product, quantity):
        self.product = product 
        self.quantity = quantity
        
    def name(self):
        return self.product.name
    def unit_price(self):
        return self.product.price
     
    def cost(self):
        return self.unit_price() * self.quantity
    
    def get_quantity(self):
        return self.get_quantity
    
    def set_quantity(self, saleQty):
        self.quantity -= saleQty

    # a getter method to access the product
    def get_product(self):
        return self

    # a repr method to print the product, uses the product repr method
    def __repr__(self):

        # self.product is an instance of the product a class 
        return f"{self.product}\nThe shop has {self.quantity} in stock \n-------------"