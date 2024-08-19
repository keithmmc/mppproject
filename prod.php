<?php 

class Product {
    public $name; 
    public $price;

    public function __construct($name, $price = 0.0) {
        $this->name = $name; 
        $this->price = $price;



    }
}

class ProductStock {
    public $product; 
    public $quantity;

    public function __construct($product, $quantity) {
        $this->product = $product;
        $this->quantity = $quantity;
    }
}

class Shop {
    public $cash;
    public $stock;

    public function __construct($cash = 0.0) {
        $this->cash = $cash;
        $this->stock = [];
    }
}


class Customer {
    public $name;
    public $budget;
    public $shopping_list;

    public function __construct($name = "", $budget = 0.0) {
        $this->name = $name;
        $this->budget = $budget;
        $this->shopping_list = [];
    }
}


function clear() {
    if (strncasecmp(PHP_OS, 'WIN', 3) === 0) {
        system('cls');
    } else {
        system('clear');
    }
}

function create_and_stock_shop() {
    $s = new Shop();
    if (($handle = fopen('stock.csv', 'r')) !== FALSE) {
        $data = fgetcsv($handle, 1000, ',');
        $s->cash = (float)$data[0];
        while (($data = fgetcsv($handle, 1000, 'r')) !== FALSE) {
            $p = new Product($data[0], (float)$data[1]);
            $ps = new ProductStock($p, (float)$data[2]); 
            $s->stock[] = $ps;

        }
        fclose($handle);
    }
    return $s;

}

function read_customer() {
    echo "Please upload your customer file name...\n";
    $path = "../" . trim(fgets(STDIN)) . ".csv";
    try {
        if (($handle = fopen($path, 'r')) !== FALSE) {
            $data = fgetcsv($handle, 1000, ',');
            $c = new Customer($data[0], (float)$data[1]);
            while (($data = fgetcsv($handle, 1000, ',')) !== FALSE) {
                $p = new Product($data[0]);
                $ps = new ProductStock($p, (float)$data[1]);
                $c->shopping_list[] = $ps;
            }
            fclose($handle);
            return $c;
        }
    } catch (Exception $e) {
        echo "Invalid customer file name.\n";
        return_to_menu();
    }
    return null;
}

function print_product($p) {
    echo "\nPRODUCT NAME: " . $p->name . " \nPRODUCT PRICE: €" . $p->price . "\n";
}

function print_shop($s) {
    echo "Shop has €" . $s->cash . " in cash\n";
    foreach ($s->stock as $item) {
        print_product($item->product);
        echo "the shop has " . $item->quantity . "of the above";
        echo "-----------------------";
    }
}

function return_to_menu() {
    echo "\nHit any key to return to main menu";
    fgets(STDIN);
    show_menu();
}

function show_menu() {
    
}