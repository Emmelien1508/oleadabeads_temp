# Improvement points
I did the code review with Reinout Mensing from my group and he pointed out a few things that I might want to improve next time.

#### Anonymous users
In order to deal with anonymous users -- users who are not logged in but wish to complete an order -- I checked with an if-statement (in which I used a try and except method to get the Customer object that corresponds with this anonymous user) if this user is anonymous. This line of code was seen in a couple of functions in views.py, and it took about 7-8 lines of code every time. In the future it might be handy to write one function to extract the Customer object of the user in order to add products to their cart, complete orders, etc., since it took more than a few dozen lines of code in total. There is some room for improvement there.

#### Chaotic importing
At the top of my views.py file, I have imported several modules that I use. However, this looks very messy and not every module is used. This could have been ordered so that the first impression is not so chaotic.

#### Customer object
In order to log in with an emailaddress instead of the usual user authentication via a username, I had to create a whole new object that overrules the AbstractUser. However, I do not have a complete understanding of the custom made authentication system that I have implemented. This causes the model to be messy and I believe some lines of code are redundant in the making of the Customer object. An improvement point would be to read more on the documentation of customizing user authentication.

#### Bugs in the views.py file
Due to lack of time, there were a couple of bugs in my views.py file which have not been cleaned up. For example, if a customer places an order and they change the input of the email field, then this new email does not get a confirmation email after ordering, but the old one. These minor bugs need fixing. In the future I will make sure to focus on these details as well. 

#### Efficiency of the code
Some functions in the views.py file as well as the HTML pages could have been more efficient. For example, adding and removing products from a user's favorites could have been done in the same function. Overall, the code in views.py could have probably be shortened by at least one quarter of the whole code. 

#### Displaying products
The displaying of the products was not done with a flex-wrapper but shown as 4 products per row. For example, if there are 9 products to show, the first two rows look perfectly fine. However, the last product is spanned over the whole width of the page instead of having the same size as the products in the previous row. This does not look professional and should be changed in the future.

#### DIY product
With my current models, when a user adds a DIY product to their cart, a normal Product object is created and given the title "DIY {first name of user}". However, when a user has multiple DIY products in their cart, these all have the same name en when they want to remove one of these DIY products from their cart, the screen shows an error while retrieving this one object it wants to delete. Because there is a possibility of having multiple products with the same name in the cart, it is not possible to get only one of these objects. A solution would be to create a DIY object and give the DIY product the title "DIY {id DIY object}" so that the title of these DIY products are unique. 

#### Editing personal profile
I would like to add a button where a user can edit or delete his/her profile. I haven't had the time to add this but in the future I want to add this to the website.

#### Layout when not logged in
When the user is logged in, the navigation bar at the bottom of the page spans the full width of the page. However, when the user is not logged in one item in this bar is excluded and it doesn't span the full width of the page anymore. This is something to fix in the future.
