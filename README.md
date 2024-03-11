# simple-bank

Thank you for your interest in the Simple Bank repository! In this readme file, we will guide you through the process of
building and running the project using Docker and Docker Compose. We will also provide an overview of the different
parts of the repository.

#### **Building and Running with Docker**

To build and run the Simple Bank project using Docker, please follow these steps:

1. Clone the repository to your local machine using the following command:

   ```
   git clone https://github.com/rmmbdev/simple-bank.git
   ```

2. Navigate to the project directory:

   ```
   cd simple-bank
   ```

3. Build the Docker image using the provided Dockerfile:

   ```
   docker build -t simple-bank .
   ```

4. Run the application using Docker Compose:

   ```
   docker-compose up
   ```

   This command will start the application and its dependencies, such as the `PostgreSQL` database, `Redis` database
   and `Rabbitmq` as message broker.

#### **Requests**

You can access various functionalities through these endpoints:

| Request             | url                                                        | method | body                                                                                                                        |
|---------------------|------------------------------------------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------|
| `signup`            | http://localhost:8000/api/signup/                          | POST   | {	"username": "user1","password": "!123Aa456!"}                                                                             |
| `login`             | http://localhost:8000/api/token/                           | POST   | {	"username": "user1","password": "!123Aa456!"}                                                                             |
| `profile`           | http://localhost:8000/api/profile/                         | GET    |                                                                                                                             |
| `list accounts`     | http://localhost:8000/api/accounts/                        | GET    |                                                                                                                             |
| `create account`    | http://localhost:8000/api/accounts/                        | POST   |                                                                                                                             |
| `list transactions` | http://localhost:8000/api/transactions/                    | GET    |                                                                                                                             |
| `create increment`  | [http://localhost:8002/accounts/<account-id>/increment/]() | POST   | {"amount": 1000000 }                                                                                                        |
| `create transfer`   | http://localhost:8002/transactions/                        | POST   | {                                             	"source": "<source-id>",	"destination": "<destination-id>",	"amount": 15000} |
| `track request`     | [http://localhost:8002/requests/<request-id>/]()           | GET    |                                                                                                                             |

+ You need to send `authorization` header in order to authorize your account it should be set like `Bearer <TOKEN>`
  except for `signup` and `login` requests. This `<TOKEN>` can be obtained from the response of `login` request.
+ You can filter `list accounts` by `created_at` and `id` fields. `created_at` can be filtered by `lt` and `gt` params:
    + http://localhost:8000/api/accounts/?created_at__lt=2024-03-11T19:28:21.930227Z&created_at__gt=2024-02-11T19:28:21.930227Z
+ You have multiple filters for `list transactions`:
    + `created_at`: http://localhost:8000/api/transactions/?created_at__lt=2024-03-11T19:28:21.930227Z&created_at__gt=2024-02-11T19:28:21.930227Z
    + `amount`:
        + http://localhost:8000/api/transactions/?amount=2000000
        + http://localhost:8000/api/transactions/?amount__lt=2000000
        + http://localhost:8000/api/transactions/?amount__gt=2000000
    + `source`:
        + for `out` transactions: [http://localhost:8000/api/transactions/?source=<account-id>]()
        + for `in` transactions: [http://localhost:8000/api/transactions/?destination=<account-id>]()
+ Whenever you submit a request for `create increment` and `create transfer`, a tracking id will be shown in the
  response, you can track your request using this code and `track request` url.
+ You can run multiple instances if `gateway` and `requestors` if it was necessary for performing real-time requests
 
#### **Architecture**
###### This diagram show a brief overview of our app.
![arch.png](docs%2Farch.png)
+ `signup`, `login`, `profile`, `list accounts`, `create account`, `list transactions` are directed to `Core`
+ `create increment`, `create transfer` and `track request` are directed to `Gateway` which will be handled through async requests using event driven architecture
+ `Transaction Status` database is a fast in-memory database (Redis) which can handle high transaction rates.
+ `Database` us a Postgres instance which is able to store datas permanently
+ We used RabbitMQ for queues in this project which are:
  1. `increment`: to handle increase requests. (as soon as possible)
  2. `transfer-small`: to handle transfer requests less than 10,000,000 (as soon as possible)
  3. `transfer-large`: to handle transfer requests more than 10,000,000 (every 4 hours from 00:00 to 24:00)