require 'csv'
require 'io/console'

class Product
  attr_accessor :name, :price

  def initialize(name, price = 0.0)
    @name = name
    @price = price
  end
end

class ProductStock
  attr_accessor :product, :quantity

  def initialize(product, quantity)
    @product = product 
    @quantity = quantity
  end 
end 

class Shop 
  attr_accessor :cash, :stock 
  
  def initialize(cash = 0.0)
    @cash = cash 
    @stock = []
  end
end 

class Customer 
  attr_accessor :name, :budget, :shopping_list

  def initialize(name = "", budget = 0.0)
    @name = name 
    @budget = budget 
    @shopping_list = [] 
  end 
end 

def clear 
  system('clear' || system('cls'))
end 

def create_and_stock_shop
s = shop.new
CSV.foreach('stock.csv', headers:false).with_index do ||row, index| 
  if index == 0 
    s.cash = r[0].to_f
  else 
    p = Product.new(row[0], row[1].to_f)
    ps = ProductStock.new(p, row[2].to_f)
    s.stock << ps 
  end 
end 
s 
end 






