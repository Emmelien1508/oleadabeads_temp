## Features
### Database
In the making of the webshop, I will need a complex database. I will need to include several models that are linked to one another. 

These models are:
* Photo
* Color
* Product
* Customer
* OrderProduct
* Order
* Favorite

#### Relationships
![](doc/Tabellen.png)

Photo has Many-to-Many relationship with Product.

Color has Many-to-Many relationship with Product.

OrderProduct has One-to-Many relationship with Product and a One-to-Many relationship with Customer.

Order has One-to-Many relationship with Customer and a Many-to-Many relationship with OrderProduct.

Favorite has One-to-One relationship with Customer and Many-to-Many relationship with Product.

## Designs
### Log in
![](doc/login.jpg)

### Forgot password
![](doc/Wachtwoordvergeten.jpg)

### Register
![](doc/Registreren.jpg)

### Homepage
![](doc/Homepage.jpg)

### Products
![](doc/Productpage.jpg)

### One product
![](doc/Oneproductpage.jpg)

### Sold out product
![](doc/Uitverkochtproductpage.jpg)

### DIY jewelry page
![](doc/DIYsieraadpage.jpg)

### About us
![](doc/Aboutuspage.jpg)

### Ordering
#### Cart summary
![](doc/Winkelwagenpagina.jpg)

#### Log in or continue without account
![](doc/Inloggen_na_winkelwagendoorgaan.jpg)

#### Checkout page
![](doc/Checkoutpage.jpg)

#### Order confirmation
![](doc/Bestelbevestiging.jpg)

### Contact
![](doc/Contact.jpg)

### Photos
![](doc/Fotos.jpg)

### Profile
![](doc/Profielpage.jpg)

### Order info
![](doc/Verzendenretourneren.jpg)
