# Reservation System

This is a Django application that provides a reservation system for multiple listings. The system provides REST API endpoints for making reservations and checking availability of rooms, as well as an HTML or TEXT report for listing owners to view their booked rooms.
Requirements

*   Python 3.6 or higher
*   Django 3.2 or higher
*   djangorestframework 3.12 or higher

## Installation and Usage

```cmd
    Clone the repository and install the dependencies:
```

```cmd
$ git clone https://github.com/username/reservation-system.git
$ cd reservation-system/
$ pip install -r requirements.txt
```

##    Run database migrations:

```python
$ python manage.py migrate
```

##    Create a superuser:

```python

$ python manage.py createsuperuser
```

##    Start the Django development server:

```python

$ python manage.py runserver
```

Visit `http://localhost:8000/admin/` to log in to the admin site using the superuser credentials you created.

To make reservations or check availability using the REST API, you can use tools like curl or Postman to send requests to the appropriate endpoints:

To make a reservation: POST /api/reservations/

Example request body:

```json

{
    "name": "John Doe",
    "start_time": "2023-03-01T10:00:00Z",
    "end_time": "2023-03-03T12:00:00Z",
    "listing": 1
}

```

where listing is the ID of the listing being reserved.

To check availability: GET /api/reservations/available/

Example request URL:

```cmd

    http://localhost:8000/api/reservations/available/?listing_id=1&start_time=2023-03-02T10:00:00Z&end_time=2023-03-04T12:00:00Z
```

where listing_id is the ID of the listing being checked, and start_time and end_time are the start and end times of the reservation being checked.

To view the booked rooms report, visit `http://localhost:8000/api/reservations/report/` and enter the listing_id of the specific list you want to view or without input to see all reservations.

## Running with Docker

You can also run the application with Docker.

Clone the repository:

```shell

$ git clone https://github.com/username/reservation-system.git
$ cd reservation-system/
```

Build the Docker image:

```cmd

$ docker build -t reservation-system .
```

Start a Docker container:

```cmd

$ docker run -p 8000:8000 reservation-system
```

Follow steps 5 and 6 in the Installation and Usage section above to use the application.

## Running on Linux or Windows

If you are running the application on Linux or Windows without Docker, make sure you have Python 3 and the required dependencies installed. Then follow the Installation and Usage section above. The commands to start the development server may be slightly different on Windows.
Limitations

Authentication and authorization have not been implemented in this application, so it is not suitable for production use. You should implement proper security measures before deploying it to a production environment.
