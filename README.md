# inv-mgmt

Rudimentary inventory management app using a FastAPI backend and React TypeScript frontend. The database used by the backend is MySQL.

## Installation

You should have Docker Desktop installed in order to run Docker, which this app uses. Clone repository first, then run `docker compose up`.

    git clone git@github.com:echarin/inv-mgmt.git
    cd inv-mgmt
    docker compose up --build

Check the console and ensure that the backend is running (`Uvicorn running on ...`). Afterwards, you can access the frontend at <http://localhost:80> and the backend's Swagger API at <http://localhost:8000/docs>.

## Testing

### Hello world

Access <http://localhost:8000/> which should respond with this body:

    {
        "msg": "Hello World"
    }

### Testing flow

Access the frontend at <http://localhost:80>.

#### Item creation and update

Success case:

- Enter "Test Item", "5.5" and "Stationery" as fields for the item and click "Send".
- The system should state "Item created successfully with id `number`".
- The new item should appear in the table below.
- Enter "Test Item", "1" and "Electronics" for the item and click "Send".
- The system should state "Item with id `number` updated successfully".
- The table should reflect the updated item and total price.
- Add another item and the table should reflect the items and correct total price.

Form validation:

- Leave any one field empty and try to send. The field should say "Please fill out this field." and the form will not send.
- For price, try to enter more than 2 decimal places, or a negative number. The field should state the appropriate error and the form will not send.
- Enter a single whitespace character for name and fill in the rest of the fields, and try to send. The name field should turn red and the form will not send.

#### Item filtering

Success case:

- Under "Search inventory", click "Clear" then ensure that all fields are empty, then click "Search".
- Check that all items are reflected in the table.
- Enter start date as a date after today, and click "Search". Check that no items are returned. Clear the field.
- Enter end date as a date before today, and click "Search". Check that no items are returned. Clear the field.
- Enter different categories and check that the appropriate items are returned.

#### Backend validation

Access the backend's Swagger API at <http://localhost:8000/docs>.

- See that `GET /` gives `200 OK` and a Hello World JSON.
- See that `GET /items/categories` gives 200 OK and a list of categories.

##### Item creation and updating

Success case:

- For `POST /items/create`, send in this request body:

        {
            "name": "string",
            "category": "stationery",
            "price": 0
        }

  - Provided there isn't already an item named "string", you should receive this response:

        {
            "id": 4, // note down the ID
            "status": "created"
        }

  - Then send in this request body:

        {
            "name": "string",
            "category": "electronics",
            "price": 5.5
        }

  - Expected response:

        {
            "id": 4, // same ID as before
            "status": "updated"
        }

Validation:

- Any of these request bodies should give a 422 Unprocessable Content along with a response body detailing the error:

        {
            // empty object
        }

        // Any permutation of the following
        {
            "name": "",
            "category": "nonexistentcategory",
            "price": 5.555 // try -6 as well
        }

##### Reading items

Success case:

- For `POST /items/`, send in these request bodies:

        // any of these fields are optional and can be omitted
        // you can also leave a field as an empty string to make it optional
        {
            "dt_from": "2000-11-13T08:05:37.884Z", // date in the past
            "dt_to": "3000-11-13T08:05:37.884Z", // date in the future
            "category": "stationery"
        }

  - The response should reflect the correct number of items and total price.

Validation:

- Any of these request bodies should give a 422 Unprocessable Content along with a response body detailing the error:

        // Any permutation of the following
        {
            "dt_from": "invalidstring",
            "dt_to": "2024-11-13 08:05",
            "category": "nonexistentcategory"
        }
