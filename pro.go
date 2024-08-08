package main

import (
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

type shop struct {
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
