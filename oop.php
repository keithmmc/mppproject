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
    
}