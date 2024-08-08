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

def read_customer
  puts "Please upload your customer name"
  path = "../" + gets.chomp + ".csv"
  begin
    c = nil 
    CSV.foreach(path, headers: false).with_index do | row, index | 
      if index == 0 
        c = Customer.new(row[0], row[1].to_f)
      else
        p = Product.new(row[0])
        ps = ProductStock.new(p, row[1].to_f)
        c.shopping_list << ps 
      end 
    end 
    c
  rescue 
    puts "incorrect file has been entered"
    return_to_menu 
    nil 
  end 
end 

def print_product(p)
  puts "\nPRODUCT NAME: #{p.name} \nPRODUCT PRICE: €#{p.price}"
end

def print_shop(s)
  puts "Shop has €#{s.cash} in cash"
  s.stock.each do |item|
    print_product(item.product)
    puts "The Shop has #{item.quantity} of the above"
    puts '-------------'
  end
end

def return_to_menu
  puts "\nHit any key to return to the main menu"
  STDIN.getch
  show_menu 
end 

def show_menu
  clear
  puts "\n\n"
  puts "\t\tWelcome to the ATU shop\n"
  puts "\t\t----------------------------------"
  puts "\t\tSelect 1 for Shop Overview"
  puts "\t\tSelect 2 for Batch orders"
  puts "\t\tSelect 3 for Live orders"
  puts "\t\tSelect 0 to Exit Shop Application"
end

def process_order(c, s)
  puts "processing order"
  puts "----------------"
  totalProduct = 0 
  c.shopping_list do |item| 
    s.stock.each do |prod| 
      if item.product.name == prod.product.name 
        if prod.quantity >= item.quantity
          totalProductCost = item.quantity * prod.product.price 
          if c.budget >= totalProductCost
            s.cash += totalProductCost 
            c.budget -= totalProductCost
            puts "€#{totalProductCost} deducted from the customer funds for #{item.quantity} of #{item.product.name}.\n"
            prod.quantity -= item.quantity
            elsif c.budget < totalProductCost
            puts "You have insufficient funds, you only have €#{c.budget} but you need €#{totalProductCost} to pay for #{item.product.name}"
            totalProductCost = prod.quantity * prod.product.price
            if c.budget >= totalProductCost
              puts "€#{totalProductCost} deducted from the customer funds for #{prod.quantity} unit(s) of #{item.product.name}.\n"
              prod.quantity -= prod.quantity
              
              s.cash += totalProductCost
              
              c.budget -= totalProductCost
            
            elsif c.budget < totalProductCost
              puts "Insufficient funds, Customer has €#{c.budget} but €#{totalProductCost} required for #{item.product.name}\n"
              
              c.budget -= 0
            end
          end
        end
      end
    end
    puts "UPDATING CASH\n-------------------\nCustomer #{c.name} has €#{c.budget} left\n."
  end


def print_customer(c, s)
  puts "CUSTOMER NAME: #{c.name} \nCUSTOMER BUDGET: €#{c.budget}"
  puts "-------------\n"
  puts "CUSTOMER ORDER"
  orderCost = [] 
  c.shopping_list do |item|
    print_product(item.product)
    puts "#{c.name} ORDERS #{item.quantity} OF ABOVE PRODUCT\n"
    puts "*************************"
  end
  puts "Please wait while we check our stock...\n"
  puts "-----------------------------------------"
  puts "We have the following items in stock:\n"
  c.shopping_list.each do |item|
    s.stock.each do |prod|
      if item.product.name == prod.product.name
        cost = item.quantity * prod.product.price
        orderCost << cost
        puts "#{item.quantity} units of #{item.product.name} at €#{prod.product.price} per unit for cost of €#{item.quantity * prod.product.price}\n"
      end
    end
  end
end

def live_order(s)
  c = Customer.new 
  print "Please enter your name"
  c.name = gets.chomp 
  puts "Welcome to the atu shop, #{c.name}"
  loop do 
    print "please enter your budget"
    begin
      c.budget = Float(gets.chomp)
      break
    rescue ArgumentError
      puts "Please enter your budget as a number"
    end
  end

  print "Please enter the name of the product you are looking for (case sensitive): "
  product = gets.chomp
  p = Product.new(product)

  loop do
    print "Please enter the quantity of #{product} you are looking for: "
    begin
    quantity = Integer(gets.chomp)
    breaj 
    rescue ArgumentError
      puts "please enter the quantity as an integer"
    end 
  end 

  ps = ProductStock.new(p, quantity)
  puts "please wait while we check"
  c.shopping_list << ps 
  c
end 






