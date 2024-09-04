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
    clear();
    echo "\n\n";
    echo "\t\tWelcome to the ATU shop\n";
    echo "\t\t----------------------------------\n";
    echo "\t\tSelect 1 for Shop Overview\n";
    echo "\t\tSelect 2 for Batch orders\n";
    echo "\t\tSelect 3 for Live orders\n";
    echo "\t\tSelect 0 to Exit Shop Application\n";
}

function process_order($c, $s) {
    echo "Processing order...\n";
    echo "-------------------\n";
    $totalProductCost = 0;
    foreach ($c->shopping_list as $item) {
        foreach ($s->stock as $prod) {
            if ($item->product->name == $prod->product->name) {
                if ($prod->quantity >= $item->quantity) {
                    $totalProductCost = $item->quantity * $prod->product->price;
                    if ($c->budget >= $totalProductCost) {
                        $s->cash += $totalProductCost;
                        $c->budget -= $totalProductCost;
                        echo "€" . $totalProductCost . " deducted from the customer funds for " . $item->quantity . " of " . $item->product->name . ".\n";
                        $prod->quantity -= $item->quantity;
                    } else {
                        echo "You have insufficient funds, you only have €" . $c->budget . " but you need €" . $totalProductCost . " to pay for " . $item->product->name . "\n";
                    }
                } else {
                    echo "We only have " . $prod->quantity . " of " . $prod->product->name . " at the moment. You will be charged only for the products sold.\n";
                    $totalProductCost = $prod->quantity * $prod->product->price;
                    if ($c->budget >= $totalProductCost) {
                        echo "€" . $totalProductCost . " deducted from the customer funds for " . $prod->quantity . " unit(s) of " . $item->product->name . ".\n";
                        $prod->quantity -= $prod->quantity;
                        $s->cash += $totalProductCost;
                        $c->budget -= $totalProductCost;
                    } else {
                        echo "Insufficient funds, Customer has €" . $c->budget . " but €" . $totalProductCost . " required for " . $item->product->name . "\n";
                    }
                }
            }
        }
    }
    echo "UPDATING CASH\n-------------------\nCustomer " . $c->name . " has €" . $c->budget . " left\n.";
}

// takes in a customer c read in from the csv file (called from the batch function)
function print_customer($c, $s) {
    echo "CUSTOMER NAME: " . $c->name . " \nCUSTOMER BUDGET: €" . $c->budget . "\n";
    echo "-------------\n";
    echo "CUSTOMER ORDER:\n";
    $orderCost = [];
    foreach ($c->shopping_list as $item) {
        print_product($item->product);
        echo $c->name . " ORDERS " . $item->quantity . " OF ABOVE PRODUCT\n";
        echo "*************************\n";
    }

    echo "Please wait while we check our stock...\n";
    echo "-----------------------------------------\n";
    echo "We have the following items in stock:\n";
    foreach ($c->shopping_list as $item) {
        foreach ($s->stock as $prod) {
            if ($item->product->name == $prod->product->name) {
                $cost = $item->quantity * $prod->product->price;
                $orderCost[] = $cost;
                echo $item->quantity . " units of " . $item->product->name . " at €" . $prod->product->price . " per unit for cost of €" . ($item->quantity * $prod->product->price) . "\n";
            }
        }
    }
}


function live_order($s) {
    $c = new Customer();
    echo "Please enter your name: ";
    $c->name = trim(fgets(STDIN));
    echo "Welcome to the shop, " . $c->name. "/n";
    while (true){
        echo "Please enter your budget";
        $input = trim(fgets(STDIN));
        if (is_numeric($input)) {
            $c->budget = (float)$input;
            break; 
        } else {
            echo "Please enter your budget as a number\n";
        }
    }
    echo "Please enter the name of the product you are looking for (case sensitive): ";
    $product = trim(fgets(STDIN));
    $p = new Product($product);

    while (true) {
        echo "Please enter the quantity of " . $product . " you are looking for: ";
        $input = trim(fgets(STDIN));
        if (is_numeric($input)) {
            $quantity = (int)$input;
            break;
        } else {
            echo "Please enter the quantity as an integer\n";
        }
    }

    $ps = new ProductStock($p, $quantity);
    echo "Please wait while we check\n";
    $c->shopping_list[] = $ps;
    return $c;
}


function main() {
    clear();
    echo "setting up shop for today";
    $s = create_and_stock_shop();
    while (true) {
        show_menu();
        echo "\nPlease select option from the main menu: ";
        $choice = trim(fgets(STDIN));

        switch ($choice) {
            case "1":
                echo "1: SHOP OVERVIEW\n";
                print_shop($s);
                return_to_menu();
                break;
            case "2":
                echo "2: BATCH ORDERS\n";
                $c = read_customer();
                if ($c) {
                    print_customer($c, $s);
                    process_order($c, $s);
                }
                return_to_menu();
                break;
            case "3":
                echo "3:*** LIVE MODE ***\n";
                echo "Please choose from our products listed below\n";
                print_shop($s);
                $c = live_order($s);
                print_customer($c, $s);
                process_order($c, $s);
                return_to_menu();
                break;
            case "0":
                echo "\nThank you for shopping here. Goodbye.\n";
                exit;
            default:
                show_menu();
        }
    }
}

if (php_sapi_name() == "cli") {
    main();
}