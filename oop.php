<?php 

class Product{
    public $name; 
    public $price;

    public function __construct($name, $price = 0){
        $this->name = $name;
        $this->price = $price;
    }
    public function __toString() {
            return "PRODUCT NAME: $this->name\nPRODUCT PRICE: €$this->price\n";
        }
    }

class ProductStock {
    public $product; 
    public $quantity;

    public function __construct($product, $quantity) {
        $this->product = $product; 
        $this->quantity = $quantity;
    }

    public function name() {
        return $this->product->name;

    }

    public function unitPrice() {
        return $this->product->price;
    }

    public function cost() {
        return $this->unitPrice() * $this->quantity;
    }
    
    public function reduceQuantity($saleQty) {
        $this->quantity -= $saleQty;
    }

    public function __toString() {
        return $this->product->__toString() . "The shop has $this->quantity in stock\n-------------\n";
    }
}

class Customer {
    public $name; 
    public $budget;
    public $shoppingList = [];

    public function __construct($filename){
        $this->loadCustomerData($filename);
    }

    public function loadCustomerData($filename){
        $filePath = '../$filename.csv';
        if(!file_exists($filePath)) {
            echo "Invalid customer file name.\n";
            exit;

        }

        $file = fopen($filePath, 'r');
        $firstRow = fgetcsv($file);
        $this->name = $firstRow[0];
        $this->budget = floatval($firstRow[1]);
    

    while ($row = fgetcsv($file)) {
        $productName = $row[0];
        $quantity = floatval($row[1]);
        $product = new Product($productName);
        $productStock = new ProductStock($product, $quantity);
        $this->shoppingList[] = $productStock;
    }

    fclose($file);
}
public function calculateCosts($priceList) {
    foreach ($priceList as $shopItem) {
        foreach ($this->shoppingList as $listItem) {
            if ($listItem->name() == $shopItem->name()) {
                $listItem->product->price = $shopItem->unitPrice();
            }
        }
    }
}

}