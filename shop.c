#include <stdio.h> // for reading files
#include <string.h>
#include <stdlib.h> // required for atof()


struct Product
{
  char *name;   // * (asterix) indicates a pointer and will allow for dynamic memory allocation, because the length of the product name is not yet know.
  double price; // double float data type for the product price.
};


struct ProductStock
{
  struct Product product; // cross reference to 'Product' struct; struct type.
  int quantity;           // quantity of the product available in the shop stock.
};


struct ProductQuantity
{
  struct Product product; // cross reference to 'Product' struct; struct type.
  int quantity;           // quantity of the product available by the shop/customer.
};


struct Shop
{
  double cash;                   // The amount of money in the shop.
  struct ProductStock stock[20]; // Nested 'ProductStock' struct (which in turn consists of nested 'Product' struct). This variable has a preset limit of items.
  int index;                     // This variable is used for cycling through the content ('for loop'); default (starting) value of index is 0.
};


struct Customer
{
  char *name;                              // Pointer is used here, so that the size of memory is dynamically allocated, depending on the name's length.
  double budget;                           // This variable will limit the customer buying capacity.
  struct ProductQuantity shoppingList[10]; // Nested 'ProductQuantity' struck, predefined size of the array (amount of items a customer may hold).
  int index;                               // This variable allows for looping through the items the customer has.
};




void printProduct(struct Product prod) // This method requires a struct 'Product' (takes it as a parameter), named localy within the method as to 'prod'. The method does not return anything.
{
  // if the price is  defined (we are showing the shop stock), then both name and price are shown; otherwise (we are showing the customer shopping list) only product name is showm
  if (prod.price == 0)
  {
    printf("Product: %s; ", prod.name); // Values of prod.name and prod.price of the passed instance of the struct when the method was called. These are referring to product's properties defining the strut instance.
  }
  else
  {
    printf("Product: %s; \tPrice: €%.2f \t", prod.name, prod.price); // Values of prod.name and prod.price of the passed instance of the struct when the method was called. These are referring to product's properties defining the strut instance.
  }
}
// Getting product price from another struct
double get_product_price(struct Product prod) //  The method does not return anything.
{
  return prod.price; // Values of prod.price from another struct
}


struct Shop createAndStockShop() // This creates a struct of 'Shop' type and its actual instance is a results (return) of the function
{
  // Reading file script is based on https://stackoverflow.com/a/3501681
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  size_t read;

  // reading the file.
  fp = fopen("Data/shop_stock.csv", "r"); // The file is in the same directory, "r" means it is to be read only.

  // Error handling (in case the file cannot be found)
  if (fp == NULL)
  {
    printf("File not found\n");
    exit(EXIT_FAILURE);
  }

  // read the first line only - the initial value of cash available in shop
  read = getline(&line, &len, fp);
  double cashInShop = atof(line);
  struct Shop shop = {cashInShop}; // This struct initialises the 'shop' instance of 'Shop' struct, and saves the shop's initial cash

  // Below we read each line and extract and assign certain data to correct variables.
  while ((read = getline(&line, &len, fp)) != -1) // Reads line by line to the end of file. "&line" referres to value of the line (I guess); -1 means to the end of file.
  {
    // printf(": %s \n", line); // This is for testing if the program reads the file; comented out for clarity

    // Function "strtok" is used to break down a string by provided delimiter (eg ",").
    char *nam = strtok(line, ",");
    char *pri = strtok(NULL, ","); //  product price from the previous delimiter in the line (NULL) till encounter the next delimiter ",".
    char *qua = strtok(NULL, ","); // product available quantity from the previous delimiter in the line (NULLine?).

   

    // To convert string into intiger, we will use "atoi" method, and to float - "atof" method.
    double price = atof(pri);
    int quantity = atoi(qua);
    char *name = malloc(sizeof(char) * 50); // max length of the product name read from the file is dynamically allocated in the memory (with a pointer) and is limited to 50 characters
    strcpy(name, nam);                      // copies variable 'nam' (initialised in the line above) to string variable 'name'

    // assign the read values to the struct placeholders
    struct Product product = {name, price};
    struct ProductStock stockItem = {product, quantity};

    shop.stock[shop.index++] = stockItem; // The above data extracted from file will be added to shop stock of struct "Shop".
    // printf("Product: %s, €%.2f; available: %d pcs.\n", name, price, quantity); // Testing; the content of the struck will be read with a dedicated method below.
  }

  return shop; // this returns the struct 'shop' of Shop type
}

// ----- ----- ----- ----- -----
// Process customer shopping
// ----- ----- ----- ----- -----
// Reading data from a file line by line and converts into a variable (product stock) and add to struct that represents the customer.
struct Customer create_customer(char *path_to_customer)
{

  // Reading file script is based on https://stackoverflow.com/a/3501681
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  size_t read;

  // reading the file.
  fp = fopen(path_to_customer, "r"); // The file is in the same directory, "r" means it is to be read only.
  //fp = fopen("../Data/customer_insufficient_funds.csv", "r"); // The file is in the same directory, "r" means it is to be read only.
  //fp = fopen("../Data/customer_exceeding_order.csv", "r"); // The file is in the same directory, "r" means it is to be read only.

  // Error handling (in case the file cannot be found)
  if (fp == NULL)
  {
    printf("File not found\n");
    exit(EXIT_FAILURE);
  }

  // read the first line only - the name of the customer and available money
  read = getline(&line, &len, fp);

  // Function "strtok" is used to break down a string by provided delimiter (eg ",").
  char *nam = strtok(line, ","); // certain data (customer name) from the line (slicing) till encounter delimiter "," and assigns to variable "name" - here with pointer, as we do not know how long is the name.
  char *bud = strtok(NULL, ","); // product available quantity from the previous delimiter in the line (NULL) till encounter the next delimiter "," (or end of line?).

  // Printing the outcome. Note 1: quantity is read from file as string type. Note 2: the method introduces a line break after the line from file was read (because by default it reads data as string).

  // To convert string into intiger, we will use "atoi" method, and to float - "atof" method.
  char *name = malloc(sizeof(char) * 50); // max length of the customer name to be read from file is limited to 50 characters
  strcpy(name, nam);                      // copies variable 'nam' (initialised in the line above) to string variable 'name'
  double budget = atof(bud);

  //assign name and budget to the customer - use the above variables (name and budget)
  struct Customer customer = {name, budget};
  //printf("Ccustomer: %s, money: %.2f\n", customer.name, customer.budget); // for testing

  // read the remaining lines from the file, extract and assign certain data to the appropriate variables.
  while ((read = getline(&line, &len, fp)) != -1) // Reads line by line to the end of file. "&line" referres to value of the line (I guess); -1 means until the end of file.
  {
    // Method "strtok" is used to break down a string by provided delimiter (eg ",").
    char *p_nam = strtok(line, ","); // certain data (product name) from the line (slicing) till encounter delimiter "," and assigns to variable "name" - here with pointer, as we do not know how long is the name.
    char *p_qua = strtok(NULL, ","); // product available quantity from the previous delimiter in the line (NULL) till encounter the next delimiter ",".

    

    // To convert string into intiger, we will use "atoi" method, and to float - "atof" method.
    char *name = malloc(sizeof(char) * 50); // max length of the product name to be read from file is limited to 50 characters
    strcpy(name, p_nam);                    // copies variable nam to variable name (initialised in the line above)
    int quantity = atoi(p_qua);

    struct Product product = {name}; // variable product.price is omitted here, so the default value (zero) is assumed (?)

    struct ProductQuantity shopping_list_item = {product, quantity}; // 'shopping_list_item' is just a temporary variable
    // printf("Test3: %s, qty: %d\n", shopping_list_item.product, shopping_list_item.quantity); //test Ok
    customer.shoppingList[customer.index++] = shopping_list_item; // The above values from 'shopping_list_items' are now assigned to 'shoppingList[index]'.

    // printf("Test2: %s\n", product.name); //test OK
    // printf("Test3: %s\n", price); // test NOT OK
    // printf("qty, %d\n", customer.shoppingList[customer.index]); // for testing - OK
  }

  // test
  // printf("Number of itmes: %d\n", customer.index); // test OK
  // printf("1st product: %s\n", customer.shoppingList[0].product.name);       // test OK
  // printf("Amount of 1st product: %d\n", customer.shoppingList[0].quantity); // test OK
  // printf("****\n\n");

  return customer;
}


void printShop(struct Shop *sh)
// The method takes "struct Shop" as a parameter; it does not return anything.
{
  // Show shop detials
  printf("\nShop has €%.2f in cash\n", sh->cash);
  printf("==== ==== ====\n");

  // loop through the items and show the associated details (name, price, quantity)
  for (int i = 0; i < sh->index; i++)
  {
    printProduct(sh->stock[i].product);
    printf("Available amount: %d\n", sh->stock[i].quantity);
  }
  printf("\n");
}

// ----- ----- ----- ----- -----
// Show customers details
// ----- ----- ----- ----- -----
double print_customers_details(struct Customer *cust, struct Shop *sh) // returns total cost
{
  printf("\nCustomer name: %s, budget: €%.2f \n", cust->name, cust->budget); // Values of cust.name and cust.budget are referring to customer's details defined the strut instance (within 'Main' method).
  printf("---- ---- ----\n");

  // initialise auxiliary variables
  double total_cost = 0.0;

  //int customer_wants = cust.shoppingList[0].quantity;

  //show customer's shopping list
  printf("%s wants the following products: \n", cust->name);

  //loop over the items in the customer shopping list
  for (int i = 0; i < cust->index; i++) // Iteration of from i=0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
  {
    // Show customers details
    printf(" -%s, quantity %d. ", cust->shoppingList[i].product, cust->shoppingList[i].quantity); // example of chain-accessing the data in the nested stucts

    // initialise auxiliary variable
    double sub_total = 0; // sub total cost for items from the shopping list

    // Calculating sub-total cost of all items of the i-th product in customer's shopping list.

    // check whether the product from customer's shopping list is matches with the shop stock list of products
    int match_exist = 0;                                       // initialy set to zero, assuming there is no match
    char *cust_item_name = cust->shoppingList[i].product.name; // assign the i-th product from the customer schopping list as a shorthand

    // Iterate through shop stock list to match items from customer's shopping list
    for (int j = 0; j < sh->index; j++)
    {
      char *sh_item_name = sh->stock[j].product.name; // assign the j-th product from the shop stock list as a shorthand

      if (strcmp(cust_item_name, sh_item_name) == 0) // if true, both product names are identical
      {
        match_exist++; // set to one, meaning there is a matach

        // check if there is enought of the products in the shop stock
        if (cust->shoppingList[i].quantity <= sh->stock[j].quantity) // sufficient amount of the product in the shop stock
        {
          printf("\tOK, there is enough in stock and "); // Prints out cost of all items of the product

          // perform the cost of the i-th item from the customer's shopping list (full order for the item is done)
          double sub_total_full = cust->shoppingList[i].quantity * sh->stock[j].product.price; // qty*price
          printf("sub-total cost would be €%.2f. \n", sub_total_full);                         // Prints out cost of all items of the product
          sub_total = sub_total_full;                                                          // sub total cost for the i-th item
        }

        else // customer wants more than in stock
        {
          // check how many can be bought
          int partial_order_qty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - sh->stock[j].quantity); // will buy all that is in stock

          // perform the cost of the i-th item from the customer's shopping list
          double sub_total_partial = partial_order_qty * sh->stock[j].product.price;                                                          // partial qty * price
          printf("\tHowever only %d is available and sub-total cost for that many would be €%.2f. \n", partial_order_qty, sub_total_partial); // Prints out cost of all items of the product
          sub_total = sub_total_partial;
        }
        // addition of sub totals
        total_cost = total_cost + sub_total;
      }
    }
    // if customer wants a product that is not in the shop
    if (match_exist == 0) // there is no match of product
    {
      printf("\tThis product not available. Sub-total cost will be €%.2f. \n", sub_total); // Prints out cost of all items of the product
    }
  }
  printf("\nTotal shopping cost would be €%.2f. \n\n", total_cost); // Prints out cost of all items of the product

  return total_cost;
}


void process_order(struct Customer *cust, struct Shop *sh, double *total_cost)
{

  // Check whether the customer can afford the desired items
  if (cust->budget < *total_cost) // customer is short of money
  {
    printf("Unfortunately, the customer does not have enough money for all the desired items - short of €%.2f. ", (*total_cost - cust->budget));
    printf("Shopping aborted. Come back with more money or negotiate your shopping list.\n\n");
  }

  else // customer has enough money
  {
    printf("Processing...\n");

    //loop over the items in the customer shopping list
    for (int i = 0; i < cust->index; i++) // Iteration of from i=0, increasing by 1, through all the items the customer has. Variable 'index' (defined in the struct) by defult starts with value 0 (zero)
    {
      // check whether the product from customer's shopping list is matches with the shop stock list of products
      int match_exist = 0;                                       // initialy set to zero, assuming there is no match
      char *cust_item_name = cust->shoppingList[i].product.name; // assign the i-th product from the customer schopping list as a shorthand

      // Iterate through shop stock list to match items from customer's shopping list
      for (int j = 0; j < sh->index; j++)
      {
        char *sh_item_name = sh->stock[j].product.name; // assign the j-th product from the shop stock list as a shorthand

        if (strcmp(cust_item_name, sh_item_name) == 0) // if true, both product names are identical
        {
          match_exist++; // set to one, meaning there is a matach

          //check products availability
          if (cust->shoppingList[i].quantity <= sh->stock[j].quantity) // sufficient amount of the product in the shop stock
          {
            // update the shop stock (full order)
            sh->stock[j].quantity = sh->stock[j].quantity - cust->shoppingList[i].quantity;
            printf("Stock quantity of %s updated to: %d \n", cust->shoppingList[i].product.name, sh->stock[j].quantity);
          }

          else // customer wants more than in stock
          {
            // check how many can be bought
            int partial_order_qty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - sh->stock[j].quantity); // will buy all that is in stock

            // perform the cost of the i-th item from the customer's shopping list
            double sub_total_partial = partial_order_qty * sh->stock[j].product.price; // partial qty * price
            // printf("Only quantity %d of %s is available and that many bought. Sub-total cost was €%.2f. ", partial_order_qty, cust->shoppingList[i].product.name, sub_total_partial); // Prints out cost of all items of the product

            // update the shop stock (partial order)
            sh->stock[j].quantity = sh->stock[j].quantity - partial_order_qty;

            printf("Stock quantity of %s updated to %d. \n", cust->shoppingList[i].product.name, sh->stock[j].quantity);
          }
        }
      }
      // if customer wants a product that is not in the shop
      if (match_exist == 0) // there is no match of product
      {
        printf("\tThis product not available. Sub-total cost will be €0.00. \n"); // Prints out cost of all items of the product
      }
    }

    // update the cash in shop
    sh->cash = sh->cash + *total_cost;

    // update the customer's money
    cust->budget = (cust->budget - *total_cost);

    printf("\nShop has now €%.2f in cash. \n", sh->cash);
    // printf("%s's remaining money is €%.2f. \n", cust->name, cust->budget); //updated customer's budget
    printf("%s's remaining money is €%.2f in cash. \n", cust->name, cust->budget);
    printf("\n");
  };

  return;
}


void interactive_mode(struct Shop *sh, double *budget)
{
  //fflush(stdin); // flushes the input string from any left overs from previous inputs

  // printf("Budget: %.2f\n", (*budget)); // for testing - ok

  // print shops stock
  printf("\nThe following products are available in shop:\n");

  printShop(&(*sh));

  // declare required variables
  char product_name[100];
  int quantity;

  //initialise forever loop until user enter 'x' while typing the product name
  while (strcmp(&product_name, "x") != 0)
  {

    // get required data from user's input
    printf("\nEnter desired product name (x to exit): ");

    fgets(product_name, sizeof product_name, stdin);
    scanf("%[^\n]%*c", product_name);

    printf("Searching for: \"%s\"", product_name);

    // printf("Test 2: Customer budget: %.2f, product: %s\n", (*budget), product_name); // for testing - ok
    // printf("Test 3: Cash in shop: %f\n", *(&sh->cash));                        // for testing - ok
    // printf("Test 4: Product price of index 2: %.2f\n", *(&sh->stock[2].product.price));        // for testing - ok

    // check whether the product from customer's shopping list is matches with the shop stock list of products
    int match_exist = 0; // initialy set to zero, assuming there is no match

    // Iterate through shop stock list to match items from customer's shopping list
    for (int j = 0; j < sh->index; j++)
    {

      // initialise auxiliary variable
      double sub_total = 0; // sub total cost for items from the shopping list

      // printf("test 5: item in shop: %s\n", *(&sh->stock[j].product.name)); // for testing - ok
      char *sh_item_name = sh->stock[j].product.name; // assign the j-th product from the shop stock list as a shorthand

      if (strcmp(product_name, sh_item_name) == 0) // if true, both product names are identical
      {
        match_exist++; // set to one, meaning there is a matach

        printf("\nEnter desired quantity: ");
        scanf("%d", &quantity);

        //check products availability
        if (quantity <= sh->stock[j].quantity) // sufficient amount of the product in the shop stock
        {
          // check product price and calculate sub-total cost (price*qty)
          sub_total = sh->stock[j].product.price * quantity;

          // check if customer can afford it
          if (*budget >= sub_total)
          {

            // update customer's budget
            *budget = *budget - sub_total;
            printf("Bought! Sub total cost was €%.2f. Budget after buying this item: €%.2f. \n", sub_total, *budget);

            // printf("There is enough in stock. ");                                                     // for testing - ok
            // printf("Sub total: €%.2f. Budget after buying this item: €%.2f. \n", sub_total, *budget); // for testing - ok

            // update the shop stock (full order)
            sh->stock[j].quantity = sh->stock[j].quantity - quantity;
            // update the shop cash
            sh->cash = sh->cash + sub_total;
            printf("Stock quantity of %s in shop updated to: %d. Cash in shop now: %.2f. \n", product_name, sh->stock[j].quantity, sh->cash);
          }

          else
          {
            printf("Unfortunately, you do not have enough money for all the desired items - short of €%.2f. ", (sub_total - *budget));
            printf("Come back with more money or reduce the quantity.\n");
          }
        }

        else // customer wants more than in stock
        {
          // check how many can be bought
          int partial_order_qty = quantity - (quantity - sh->stock[j].quantity); // will buy all that is in stock

          // perform the sub-total cost for the item
          double sub_total_partial = partial_order_qty * sh->stock[j].product.price;                                             // partial qty * price
          printf("Only %d is available and that many bought. Sub-total cost was €%.2f. ", partial_order_qty, sub_total_partial); // Prints out cost of all items of the product

          // update customer's budget
          *budget = *budget - sub_total_partial;
          printf("Budget after buying this item: €%.2f. \n", *budget);

          // update the shop stock (partial order) and cash
          sh->stock[j].quantity = sh->stock[j].quantity - partial_order_qty;
          // update the shop cash
          sh->cash = sh->cash + sub_total_partial;
          printf("This product is no longer avilable in shop (stock: %d). Cash in shop now: %.2f. \n", sh->stock[j].quantity, sh->cash);
        }
      }
    }
    if (match_exist == 0) // product not available in stock
    {
      printf("Product not found in shop. \n");
    }
  }
  //;
}



// Menu script adapted from https://ladvien.com/command-line-menu-c/
void shop_menu(struct Shop sh)
{
  char char_choice[2];
  int choice = -1; // the initial value is set just to initialise the variable

  system("cls");   // for Windows systems
  system("clear"); // for Linux systems
 

  char separator[20] = "***************\n";

  do
  {
    printf("\n");
    printf(separator);
    printf("Shop Main Menu (C language):\n");
    printf(separator);
    printf("1. Shop status\n");
    printf("2. Customer A - good case\n");
    printf("3. Customer B - insufficient funds case\n");
    printf("4. Customer C - exceeding order case\n");
    printf("5. Interactive mode\n");
    printf("9. Exit application\n\n");
    printf("NB: The sequence of the customers being processed might affect the initial case of the customers. \n");
    printf(separator);
    printf("Enter your choice: ");

    fflush(stdin); // flushes the input string from any left overs from previous inputs
    scanf("%s", char_choice);
    choice = atoi(char_choice);

    switch (choice)
    {

 
    case 1:

      printShop(&sh);

      break;

    
    case 2:; // semicolon here, because: https://www.educative.io/edpresso/resolving-the-a-label-can-only-be-part-of-a-statement-error

      // create customer A struct (good case)
      struct Customer customer_A = create_customer("Data/customer_good.csv"); // This struct calls the method that will read data from a file.

      // print customer details and shopping list
      double total_cost = print_customers_details(&customer_A, &sh);

      // show customer's shopping list by calling relevant method
      process_order(&customer_A, &sh, &total_cost);

      break;

 
    case 3:;

      // create customer B struct (insufficient funds case)
      struct Customer customer_B = create_customer("Data/customer_insufficient_funds.csv"); // This struct calls the method that will read data from a file.

      // print customer details and shopping list
      total_cost = print_customers_details(&customer_B, &sh);

      // show customer's shopping list by calling relevant method
      process_order(&customer_B, &sh, &total_cost);

      break;

  
    case 4:;

      // create customer C struct (exceeding order case)
      struct Customer customer_C = create_customer("Data/customer_exceeding_order.csv"); // This struct calls the method that will read data from a file.

      // print customer details and shopping list
      total_cost = print_customers_details(&customer_C, &sh);

      // show customer's shopping list by calling relevant method
      process_order(&customer_C, &sh, &total_cost);

      break;

    case 5:;
      // Welcoming message
      printf("\nInteractive shopping mode\n");
      printf("-------------------------\n");

      // get user's name
      printf("What's your name ");
      char *customer_name = malloc(sizeof(char) * 50); // declare the variable
      scanf("%s", customer_name);
      printf("Welcome, %s. \n", customer_name);

      // get user's budget
      printf("Enter your budget: ");
      double budget; // declare the variable
      scanf("%lf", &budget);
      // printf("Confirming entering budget: €%.2f. \n", budget); // for testing - ok
      interactive_mode(&sh, &budget);

      break;

    case 9:;
      // exit
      break;

    default:
      printf("Wrong key. Enter the option number for desired operation.\n");
      break;
    }
  } while (choice != 9);
}



int main()
{

  // create shop
  struct Shop shop_one = createAndStockShop(); // This struct calls the method that will read data from a file.

  shop_menu(shop_one); // calls the method that displays the shop menu

  return 0;
}