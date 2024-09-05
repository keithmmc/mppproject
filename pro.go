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

type Product struct {
	Name  string
	Price float64
}

type ProductStock struct {
	Product  Product
	Quantity int
}

type Shop struct {
	Cash  float64
	Stock []ProductStock
}

type Customer struct {
	Name         string
	Budget       float64
	ShoppingList []ProductStock
}

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
	fmt.print("please upload your customer file name here.... ")
	path, _ := reader.ReadString('\n')
	path = "../" + strings.TrimSpace(path) + ".csv"
	file, err := os.Open(path)
	if err != nil {
		fmt.Println("incorrect customer file name,")
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
func printProduct(p Product) {
	fmt.Printf("\nPRODUCT NAME: %s \nPRODUCT PRICE: €%.2f\n", p.Name, p.Price)
}

func printShop(s Shop) {
	fmt.Printf("Shop has €%.2f in cash\n", s.Cash)
	for _, item := range s.Stock {
		printProduct(item.Product)
		fmt.Printf("The Shop has %d of the above\n", item.Quantity)
		fmt.Println("-------------")
	}
}

func returnToMenu() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("press any key to return to main menu")
	reader.ReadString('\n')
	showMenu()
}

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

func processOrder(c Customer, s Shop) {
	fmt.Println("Processing order")
	fmt.Println("----------------")
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
