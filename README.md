# API for ordering

API for managing orders, clients and products, built with FastAPI.
It allows you to: create clients, add products, create orders for client
and get orders by user ID. 

### Endpoints:

| Method | Endpoint  | Description      |
|--------|-----------|------------------|
| POST   | /clients  | Create client    |
| GET    | /products | List of products |
| POST   | /products | Add new product  |
| POST   | /orders   | Create new order |
| GET    | /order    | Get order by ID  |


### Get started

Python3 must be already installed!
```shell
git clone https://github.com/pohonets-crypto/k2_test_task.git
cd k2_test_task
```

### Run with Docker

```shell
docker-compose build
docker-compose up
```

Allows at: http://127.0.0.1:8000/docs

Swagger API Documentation: http://127.0.0.1:8000/docs
