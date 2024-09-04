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

}
