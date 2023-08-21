# uav-rental
Creating UAV Rental project with Django and PostgreSQL. The project includes Register, Login, UAV CRUD operations.

--Views.py--

Imports:

Various utility functions and classes are imported from Django and local modules to facilitate operations.

home_page(request):

Renders the home page, showing all the UAVs available.
Sends whether the user is authenticated as part of the context to the template.

register_page(request: HttpRequest):

Handles user registration.
If a POST request is received, the function tries to fetch details from the form to create a new user.
If the email is already taken, an error message is displayed.
Otherwise, a new user is saved in the database.

login_page(request):

Handles user login.
If a POST request is received, the function tries to authenticate the user based on the provided email and password.
If the user is found and the password is correct, the user is logged in.
Otherwise, an error message is displayed.

logout_page(request):

Logs the user out and redirects them to the home page.

uav_form(request, id=0):

A dual-purpose view for adding a new UAV or editing an existing UAV.
If the id is 0, it means a new UAV is being added. Otherwise, an existing UAV with that id is being edited.
If the request method is GET, it renders the UAV form. For a POST request, it processes the submitted form data.

uav_delete(request, id):

Deletes a UAV based on its id.

rental_form(request, id=0):

Similar to uav_form, but for rentals.
For a POST request, it checks the validity of the form, checks if the UAV is available, and then saves the rental.

rental_delete(request, id):

Allows a user to delete a rental.
It first checks if the user trying to delete the rental is the same user who created the rental. If not, an error message is displayed.
If the user is authorized, the rental is deleted.

rentals_list(request):

Fetches and displays all rentals in a list format.

Throughout the views:

print statements are used for debugging purposes, showing specific pieces of information in the console.
messages is a Django utility that helps in displaying one-time notifications to the user.
The redirect function is used to navigate to different endpoints based on the outcome of operations.
The render function is used to serve HTML templates, often with a context that contains dynamic data to be rendered.
In summary, this views.py file handles the primary operations related to UAVs and rentals – including CRUD operations (Create, Read, Update, Delete) – as well as user registration and authentication.


--Models.py--



Imports:

models from django.db is the main module to define ORM-based database models in Django.
AbstractBaseUser is a core user authentication model provided by Django.

CAT_CHOICES:

A tuple containing choices for categories. It will be used as choices for the Category model's title field.

User(AbstractBaseUser):

A custom user model derived from Django's AbstractBaseUser.
name: Stores the user's first name.
surname: Stores the user's last name.
email: A unique field storing the user's email address. Also, the primary identifier for authentication instead of the usual username.
phone: To store the user's phone number.
password: To store the user's hashed password.
last_login: A nullable field to store the timestamp of the user's last login.
USERNAME_FIELD: This informs Django that email is the field used for user authentication.

Category(models.Model):

Represents categories for UAVs.
title: This field represents the title of the category and is restricted to choices defined in CAT_CHOICES. It defaults to 'cat1'.

UAV(models.Model):

Represents the Unmanned Aerial Vehicle (UAV) model.
brand: The brand of the UAV.
model: The model name/number of the UAV.
weight: The weight of the UAV.
category: A foreign key relation to the Category model. This signifies the category of the UAV.
is_available: A boolean field to check if the UAV is available for rent.
__str__: Returns a string representation of the UAV.

Rental(models.Model):

Represents the rental details of a UAV by a user.
uav: A foreign key relation to the UAV model.
user: A foreign key relation to the User model. It represents the user who has rented the UAV.
start_date and end_date: DateTime fields indicating the rental period.
is_uav_available(): A method that checks if a UAV is available for rent. It does this by finding any existing rentals of the UAV that overlap with the current rental period. If such rentals exist, the UAV is considered unavailable.
Meta: This inner class specifies model-specific options. The ordering option ensures that queries retrieving rentals are ordered by the start_date in descending order.
__str__: Provides a human-readable representation of the Rental instance.

The models defined in this file enable you to:

Create a custom user system with attributes like name, surname, email, etc.
Categorize UAVs.
Keep a record of all the UAVs along with their details and availability status.
Record all rentals of UAVs, the user renting them, and the rental period.
The relationships between models (like ForeignKey between UAV and Category) allow you to associate UAVs with specific categories and users with specific rentals.
