
# Book-Cinema- A Movie Ticket Booking System

This project is a Django web application that allows users to book movie tickets online. The project has been implemented using Django Rest Framework and supports the following features:

* User can view all the movies playing in your city.

* User can check all theaters in which a movie is playing along with all the showtimes.

* User can check the availability of seats for a particular shows.

* User can sign up and login to application if they want to proceed to the booking.

* User can select multiple seats and book tickets and proceed to the payment(payment gateway not integrated).



## Installation

1.Clone this repository to your local machine.

```bash
  git clone https://github.com/sachint97/book-cinema-api.git
```

2.Build the Docker image.

```bash
docker-compose build
```
3.To build the container and run the project.
```bash
docker-compose up
```

4.To remove the container and stop the project.
```bash
Ctrl + C

docker-compose down
```
## Usage

Once the development server is running, you can access the project by visiting http://localhost:8000 in your web browser.


## API Reference
### User API's
* #### User signup.

```http
  POST /api/user/create/
```

| Parameter | Type     | Description            |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**.      User email address |
| `name` | `string` | **Required**.   User name |
| `password` | `string` | **Required**. User password |
| `confirm_password` | `string` | **Required**. Confirmation password |

* #### User login.

```http
  POST /api/user/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required**. User email address. |
| `password`      | `string` | **Required**. User password. |

* #### User logout.

```http
  POST /api/user/logout/ (requires authentication)
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh_token`      | `string` | **Required**. Pass refresh token to block and logout. |

### Theater API's

* #### List of movies playing in city.

```http
  GET /api/theater/movies/<str:city>/
```
#### Response
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | Movie title. |
| `slug`      | `string` | Unique slug. |
| `description`      | `text` | Description about movie. |
| `description`      | `text` | Description about movie. |
| `duration`      | `time` | Movie duration. |
| `release_date`      | `date` | Movie release date. |
| `language`      | `string` | Movie language. |
| `certificate`      | `string` | Movie certificate U,UA,A or R. |
| `images`      | `list` | List of images url. |

<details>
  <summary>Show full response</summary>

  ```bash
  [
    {
        "title": "string",
        "slug": "string",
        "description": "string",
        "duration": "time",
        "release_date": "date",
        "language": "string",
        "certificate": "string",
        "images": [
            {
                "image": "url",
                "alt_text": "string",
                "is_feature": boolean
            }
        ]
    },
]
  ```

</details>

* #### List of shows running certain movie in a city.

```http
  GET /api/theater/shows/?movie=movie&city=city
```
#### Response
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `show`      | `object` | Object consist of movies and its timings. |
| `screen`   | `object` | Objects consist of theater and its screen details. |

<details>
  <summary>Show full response</summary>

  ```bash
  [
      {
          "show": {
              "movie": {
                  "title": "string",
                  "slug": "string",
                  "description": "string",
                  "duration": "time",
                  "release_date": "date",
                  "language": "string",
                  "certificate": "string",
                  "images": [
                      {
                          "image": "url",
                          "alt_text": "string",
                          "is_feature": boolean
                      },
                  ]
              },
              "start_date": "date",
              "end_date": "date",
              "start_time": "time",
              "end_time": "time",
              "slug": "string"
          },
          "screen": {
              "name": "string",
              "slug": "string",
              "theater": {
                  "name": "string",
                  "slug": "string",
                  "address": "string",
                  "city": {
                      "slug": "string",
                      "name": "string"
                  }
              }
          }
      }
  ]
  ```
</details>

* #### Show available seats on a particular show running on a screen.

```http
  POST /api/theater/seats-available/<str:show_screen_slug>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `show`      | `object` | Object consist of movies and its timings. |
| `screen`   | `object` | Objects consist of theater and its screen details. |
| `seating_arrangment`   | `object` | Object consistof list of seats and its availability. |

<details>
  <summary>Show full response</summary>

  ```bash
   {
    "show": {
        "movie": {
            "title": "string",
            "slug": "string",
            "description": "string",
            "duration": "time",
            "release_date": "date",
            "language": "string",
            "certificate": "string",
            "images": [
                {
                    "image": "url",
                    "alt_text": "string",
                    "is_feature": boolean
                },
            ]
        },
        "start_date": "date",
        "end_date": "date",
        "start_time": "time",
        "end_time": "time",
        "slug": "string"
    },
    "screen": {
        "name": "string",
        "slug": "string",
        "theater": {
            "name": "string",
            "slug": "string",
            "address": "string",
            "city": {
                "slug": "string",
                "name": "string"
            }
        }
    }
    "seating_arrangement": [
        {
          "seating_class": "Bolcany",
          "price": 400.0,
          "seats": [
              {
                  "row": 1,
                  "column": 1,
                  "is_available": true
              },
            ]
        }
      ]
}
```

</details>

### Booking API's

* #### Booking seats for a show

```http
  POST /api/booking/seat-booking/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `booking_date` | `Date` | Booking date. |
| `screen_show`  | `string` | Screen and show slug. |
| `seats`      | `object` | Object consisting of seat class , row and column. |

<details>

  <summary>Show full post data.</summary>

  ```bash
  {
    "booking_date":"date",
    "screen_show":"string",
    "seats":[
        {
            "seating_class":"string",
            "row":integer,
            "column":integer
        },
    ]
}
  ```

</details>


* #### Payment for booking

```http
  POST /api/booking/payment/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `booking` | `string` | Booking slug. |
| `amount`  | `integer` | amount for booking. |
| `payment_method`| `object` | Payment method UPI, Debit Card,and Credit card etc |

<details>

  <summary>Show full post data.</summary>

  ```bash
  {
    "booking":"string",
    "amount":integer,
    "payment_method":"string"
}
  ```

</details>






## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`


## Running Tests

To run tests, run the following command

```bash
  docker-compose run --rm app sh -c "python manage.py test"
```


## Tech Stack

**Server:** Python, Django, Django-rest-framework

**Database:** Postgresql
