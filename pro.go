package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

// Product is a data container here only.
type Product struct {
	Name  string
	Price float64
}

// ProductStock is equivalent to the ProductStock Struct in C.
type ProductStock struct {
	Product  Product
	Quantity int
}

// Shop is a data container for a shop.
type Shop struct {
	Cash  float64
	Stock []ProductStock
}

// Customer is a data container for a customer.
type Customer struct {
	Name         string
	Budget       float64
	ShoppingList []ProductStock
}

// clear the screen
func clear() {
	if strings.Contains(strings.ToLower(os.Getenv("OS")), "windows") {
		cmd := exec.Command("cmd", "/c", "cls")
		cmd.Stdout = os.Stdout
		cmd.Run()
	} else {
		cmd := exec.Command("clear")
		cmd.Stdout = os.Stdout
		cmd.Run()
	}
}

func createAndStockShop() Shop {
	var s Shop
	file, err := os.Open("stock.csv")
	if err != nil {
		fmt.Println("Error opening stock file:", err)
		return s
	}
	defer file.Close()

	reader := csv.NewReader(file)
	firstRow, _ := reader.Read()
	s.Cash, _ = strconv.ParseFloat(firstRow[0], 64)

	for {
		row, err := reader.Read()
		if err != nil {
			break
		}
		price, _ := strconv.ParseFloat(row[1], 64)
		quantity, _ := strconv.Atoi(row[2])
		p := Product{Name: row[0], Price: price}
		ps := ProductStock{Product: p, Quantity: quantity}
		s.Stock = append(s.Stock, ps)
	}
	return s
}

func readCustomer() Customer {
	var c Customer
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Please upload your customer file name... ")
	path, _ := reader.ReadString('\n')
	path = "../" + strings.TrimSpace(path) + ".csv"
	file, err := os.Open(path)
	if err != nil {
		fmt.Println("Invalid customer file name.")
		returnToMenu()
		return c
	}
	defer file.Close()

	csvReader := csv.NewReader(file)
	firstRow, _ := csvReader.Read()
	c.Name = firstRow[0]
	c.Budget, _ = strconv.ParseFloat(firstRow[1], 64)

	for {
		row, err := csvReader.Read()
		if err != nil {
			break
		}
		quantity, _ := strconv.Atoi(row[1])
		p := Product{Name: row[0]}
		ps := ProductStock{Product: p, Quantity: quantity}
		c.ShoppingList = append(c.ShoppingList, ps)
	}
	return c
}

// Takes in a product and prints out the price
func printProduct(p Product) {
	fmt.Printf("\nPRODUCT NAME: %s \nPRODUCT PRICE: €%.2f\n", p.Name, p.Price)
}

// This function prints the cash in the shop and each item in stock
func printShop(s Shop) {
	fmt.Printf("Shop has €%.2f in cash\n", s.Cash)
	for _, item := range s.Stock {
		printProduct(item.Product)
		fmt.Printf("The Shop has %d of the above\n", item.Quantity)
		fmt.Println("-------------")
	}
}

// define a function to return to menu after a key is pressed
func returnToMenu() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("\nHit any key to return to main menu")
	reader.ReadString('\n')
	showMenu()
}

// a function to display the menu options
func showMenu() {
	clear()
	fmt.Println("\n\n")
	fmt.Println("\t\tWelcome to the ATU shop")
	fmt.Println("\t\t----------------------------------")
	fmt.Println("\t\tSelect 1 for Shop Overview")
	fmt.Println("\t\tSelect 2 for Batch orders")
	fmt.Println("\t\tSelect 3 for Live orders")
	fmt.Println("\t\tSelect 0 to Exit Shop Application")
}

// a function to actually process the order
func processOrder(c Customer, s Shop) {
	fmt.Println("Processing order...")
	fmt.Println("-------------------")
	totalProductCost := 0.0
	for _, item := range c.ShoppingList {
		for i, prod := range s.Stock {
			if item.Product.Name == prod.Product.Name {
				if prod.Quantity >= item.Quantity {
					totalProductCost = float64(item.Quantity) * prod.Product.Price
					if c.Budget >= totalProductCost {
						s.Cash += totalProductCost
						c.Budget -= totalProductCost
						fmt.Printf("€%.2f deducted from the customer funds for %d of %s.\n", totalProductCost, item.Quantity, item.Product.Name)
						s.Stock[i].Quantity -= item.Quantity
					} else {
						fmt.Printf("You have insufficient funds, you only have €%.2f but you need €%.2f to pay for %s\n", c.Budget, totalProductCost, item.Product.Name)
					}
				} else {
					fmt.Printf("We only have %d of %s at the moment. You will be charged only for the products sold.\n", prod.Quantity, prod.Product.Name)
					totalProductCost = float64(prod.Quantity) * prod.Product.Price
					if c.Budget >= totalProductCost {
						fmt.Printf("€%.2f deducted from the customer funds for %d unit(s) of %s.\n", totalProductCost, prod.Quantity, item.Product.Name)
						s.Stock[i].Quantity = 0
						s.Cash += totalProductCost
						c.Budget -= totalProductCost
					} else {
						fmt.Printf("Insufficient funds, Customer has €%.2f but €%.2f required for %s\n", c.Budget, totalProductCost, item.Product.Name)
					}
				}
			}
		}
	}
	fmt.Printf("UPDATING CASH\n-------------------\nCustomer %s has €%.2f left\n.", c.Name, c.Budget)
}

// takes in a customer c read in from the csv file (called from the batch function)
func printCustomer(c Customer, s Shop) {
	fmt.Printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: €%.2f\n", c.Name, c.Budget)
	fmt.Println("-------------")
	fmt.Println("CUSTOMER ORDER:")
	for _, item := range c.ShoppingList {
		printProduct(item.Product)
		fmt.Printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.Name, item.Quantity)
		fmt.Println("*************************")
	}

	fmt.Println("Please wait while we check our stock...")
	fmt.Println("-----------------------------------------")
	fmt.Println("We have the following items in stock:")
	for _, item := range c.ShoppingList {
		for _, prod := range s.Stock {
			if item.Product.Name == prod.Product.Name {
				cost := float64(item.Quantity) * prod.Product.Price
				fmt.Printf("%d units of %s at €%.2f per unit for cost of €%.2f\n", item.Quantity, item.Product.Name, prod.Product.Price, cost)
			}
		}
	}
}

// a function to deal with live customer orders
func liveOrder(s Shop) Customer {
	var c Customer
	reader := bufio.NewReader(os.Stdin)

	fmt.Print("Please enter your name: ")
	c.Name, _ = reader.ReadString('\n')
	c.Name = strings.TrimSpace(c.Name)
	fmt.Printf("Welcome to the shop, %s\n", c.Name)

	for {
		fmt.Print("Please enter your budget: ")
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		budget, err := strconv.ParseFloat(input, 64)
		if err == nil {
			c.Budget = budget
			break
		} else {
			fmt.Println("Please enter your budget as a number")
		}
	}

	fmt.Print("Please enter the name of the product you are looking for (case sensitive): ")
	productName, _ := reader.ReadString('\n')
	productName = strings.TrimSpace(productName)
	p := Product{Name: productName}

	for {
		fmt.Printf("Please enter the quantity of %s you are looking for: ", productName)
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		quantity, err := strconv.Atoi(input)
		if err == nil {
			ps := ProductStock{Product: p, Quantity: quantity}
			c.ShoppingList = append(c.ShoppingList, ps)
			break
		} else {
			fmt.Println("Please enter the quantity as an integer")
		}
	}

	fmt.Println("Please wait while we check")
	return c
}

// the main program calls the functions above to create the shop, print the shop, create customers from csv and live
// process the customer orders if possible and update the shop stock and cash state
func main() {
	clear()
	fmt.Println("Setting up the shop for today...")
	s := createAndStockShop()

	// a forever loop
	for {
		showMenu()
		fmt.Print("\nPlease select option from the main menu: ")
		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			fmt.Println("1: SHOP OVERVIEW")
			printShop(s)
			returnToMenu()
		case "2":
			fmt.Println("2: BATCH ORDERS")
			c := readCustomer()
			if c.Name != "" {
				printCustomer(c, s)
				processOrder(c, s)
			}
			returnToMenu()
		case "3":
			fmt.Println("3:*** LIVE MODE ***")
			fmt.Println("Please choose from our products listed below")
			printShop(s)
			c := liveOrder(s)
			printCustomer(c, s)
			processOrder(c, s)
			returnToMenu()
		case "0":
			fmt.Println("\nThank you for shopping here. Goodbye.")
			return
		default:
			showMenu()
		}
	}
}
