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

Validation:

- Leave any one field empty and try to send. The field should say "Please fill out this field." and the form will not send.

#### Item filtering

Success case:

- Under "Search inventory", click "Clear" then ensure that all fields are empty, then click "Search".
- Check that all items are reflected in the table.
- Enter start date as a date after today, and click "Search". Check that no items are returned. Clear the field.
- Enter end date as a date before today, and click "Search". Check that no items are returned. Clear the field.
- Enter different categories and check that the appropriate items are returned.

#### Backend validation

Access the backend's Swagger API at <http://localhost:8000/docs>.
