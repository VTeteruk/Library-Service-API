# Library Service API
The Library Service API is designed to manage and facilitate book borrowing operations within a library. It provides various features to handle book information, borrowing records, and user authentication. Below are some key features of the Library Service API:
___
## Features
### User Management
* User Registration: Allows users to register and create an account in the system.
* User Authentication: Supports user authentication using JSON Web Tokens (JWT), ensuring secure access to API endpoints.
* User Profile: Provides endpoints to view and update user profiles.
### Book Management
* Book Listing: Allows users to view a list of available books in the library.
* Book Details: Provides detailed information about a specific book, including title, author, cover type, inventory count, and daily fee.
* Admin Access: Certain book management endpoints are restricted to admin users for added security.
### Borrowing Operations
* Borrowing Books: Allows users to borrow books from the library by creating borrowing records.
* Borrowing History: Provides a list of past borrowing records for users to track their borrowing history.
* Message will be sent to telegram chat when you borrow a book
### API Documentation
* Interactive API Documentation: Utilizes Spectacular to generate an interactive API documentation (Swagger) for easy API exploration.
* OpenAPI Schema: Offers an OpenAPI schema endpoint to access the API's specification.
___
## Installation and Setup
1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required packages using `pip install -r requirements.txt`.
4. Run database migrations using `python manage.py migrate`.
5. Create a superuser to access the Django admin panel with `python manage.py createsuperuser`.
6. Start the development server with `python manage.py runserver`.
## User Authentication
To access protected endpoints, users must authenticate by obtaining a JWT token using their credentials.

The api/token/ endpoint provides token obtainment through the TokenObtainPairView.

Token refresh can be done via the api/token/refresh/ endpoint using the TokenRefreshView.
## API Endpoints
For detailed information about each API endpoint, refer to the interactive API documentation (Swagger) available at /api/schema/swagger/.

Note: Due to security reasons, some endpoints are restricted to admin users and will require admin-level authentication.

## Version
The current version of the Library Service API is 1.0.0.

## About
The Library Service API is developed to streamline book management and borrowing operations, offering a convenient and secure system for both users and administrators. If you encounter any issues or have suggestions for improvements, feel free to contribute or report them to the project maintainers. Happy reading!
