# Bookstore Management System — REST API

Django REST Framework backend aligned with the supplied project brief. Features include book CRUD, customer registration, JWT login/refresh, role-based access, orders, inventory checks and updates, search/filtering, pagination, Swagger/OpenAPI docs, Django Admin, and API tests.

## Requirements
Python 3.10+ recommended. SQLite is configured by default so you can run the project without installing a separate database server.

## Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations store
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Then visit:
- Swagger: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- Admin: http://127.0.0.1:8000/admin/
- Books: http://127.0.0.1:8000/api/books/

The superuser created by `createsuperuser` can manage inventory and orders. Public registration always creates a customer and does not accept a role field.

## Endpoints
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/register/` | Public | Register customer |
| POST | `/api/login/` | Public | Obtain JWT tokens |
| POST | `/api/token/refresh/` | Public | Refresh access token |
| GET | `/api/me/` | Authenticated | Current user |
| GET | `/api/books/` | Public | Paginated list |
| GET | `/api/books/{id}/` | Public | Book detail |
| POST/PUT/PATCH/DELETE | `/api/books/...` | Admin | Manage books |
| GET | `/api/orders/` | Authenticated | Admin sees all; customer sees own |
| GET | `/api/orders/{id}/` | Authenticated | Read order if permitted |
| POST | `/api/orders/` | Customer | Place order |
| PATCH | `/api/orders/{id}/status/` | Admin | Update order/payment status |

Trailing slashes are expected. Send `Authorization: Bearer <access-token>` to protected endpoints.

## Example registration
`POST /api/register/`
```json
{"name":"Asha Rao","email":"asha@example.com","username":"asha","password":"Use-A-Strong-Password-123"}
```

## Example login
`POST /api/login/`
```json
{"email":"asha@example.com","password":"Use-A-Strong-Password-123"}
```

## Create a book (admin token)
`POST /api/books/`
```json
{"title":"Learning Django","authors":"A. Author","genre":"Technology","isbn":"9781234567890","price":"499.00","description":"Django introduction","stock_quantity":12,"image_url":"https://example.com/cover.jpg"}
```

## Search/filter/pagination
- `/api/books/?search=django` (title or author)
- `/api/books/?genre=Technology`
- `/api/books/?ordering=price`
- `/api/books/?page=2`

## Place an order
`POST /api/orders/`
```json
{"items":[{"book_id":1,"quantity":2}]}
```
Prices are taken from the database rather than client input. Stock validation and decrement happen inside a database transaction. Payment is a mock/manual status; this project does not process real payments.

## Update status (admin token)
`PATCH /api/orders/1/status/`
```json
{"status":"shipped","payment_status":"paid"}
```
Statuses: `pending`, `shipped`, `delivered`, `cancelled`; payment: `unpaid`, `paid`, `refunded`.

## Tests
```powershell
python manage.py test
```

## Before deployment
Replace the development secret, set `DJANGO_DEBUG=False`, configure allowed hosts and HTTPS, and use PostgreSQL for production concurrency. SQLite is used here for easy local setup and does not provide effective row-level locking for concurrent inventory transactions.
# Bookstore-Management-api
Bookstore Management REST API built with Django REST Framework and JWT authentication
