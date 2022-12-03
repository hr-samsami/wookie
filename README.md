### Objective

Your assignment is to implement a bookstore REST API using Python and any framework. While we will allow the use of any framework you prefer (incl. none at all) we would be grateful if you could complete the assignment in FastAPI or Django if you prefer.

### Brief

Lohgarra, a Wookie from Kashyyyk, has a great idea. She wants to build a marketplace that allows her and her friends to
self-publish their adventures and sell them online to other Wookies. The profits would then be collected and donated to purchase medical supplies for an impoverished Ewok settlement.

### Tasks

-   Implement assignment using:
    -   Language: **Python**
    -   Framework: **any framework** (preferred: FastAPI or Django)
-   Implement a REST API returning JSON or XML based on the `Content-Type` header
-   Implement a custom user model with a "author pseudonym" field
-   Implement a book model. Each book should have a title, description, author (your custom user model), cover image and price
    -   Choose the data type for each field that makes the most sense
-   Provide an endpoint to authenticate with the API using username, password and return a JWT
-   Implement REST endpoints for the `/books` resource
    -   No authentication required
    -   Allows only GET (List/Detail) operations
    -   Make the List resource searchable with query parameters
-   Provide REST resources for the authenticated user
    -   Implement the typical CRUD operations for this resource
    -   Implement an endpoint to unpublish a book (DELETE)
-   Implement tests as you see fit
    -   These could be unit test as well as API tests
    -   We would also count schema based validation as testing

### Evaluation Criteria

-   **Python** best practices
-   If you are using a framework make sure best practices are followed for models, configuration and tests
-   Sanity and usefulness of tests
-   Protect users' data
    -   Make sure that users may only unpublish and change their own books
-   Bonus: Make sure the user _Darth Vader_ is unable to publish his work on Wookie Books

### CodeSubmit

Please organize, design, test and document your code as if it were
going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The aidhere GmbH Team

### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    $ docker-compose exec web python manage.py collectstatic --no-input --clear
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "wookie" folder is mounted into the container and your code changes apply automatically.
1. To see the Swagger api document go to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) and you will see something like bellow:
![img.png](document/images/swagger.png)
### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose down -v
    $ docker-compose -f docker-compose.prod.yml up -d --build
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
