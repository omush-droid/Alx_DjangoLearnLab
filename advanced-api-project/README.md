# Advanced API Project - Django REST Framework

## API Endpoints

### Book CRUD Operations

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/books/` | List all books | AllowAny |
| GET | `/api/books/<id>/` | Retrieve single book | AllowAny |
| POST | `/api/books/create/` | Create new book | IsAuthenticated |
| PUT/PATCH | `/api/books/<id>/update/` | Update existing book | IsAuthenticated |
| DELETE | `/api/books/<id>/delete/` | Delete book | IsAuthenticated |

## View Configurations

### BookListView (ListView)
- **Purpose**: Retrieve all books
- **Permission**: AllowAny (read-only access for all users)
- **Generic View**: `ListAPIView`

### BookDetailView (DetailView)
- **Purpose**: Retrieve a single book by ID
- **Permission**: AllowAny (read-only access for all users)
- **Generic View**: `RetrieveAPIView`

### BookCreateView (CreateView)
- **Purpose**: Add a new book
- **Permission**: IsAuthenticated (authenticated users only)
- **Generic View**: `CreateAPIView`
- **Validation**: Includes custom publication year validation

### BookUpdateView (UpdateView)
- **Purpose**: Modify an existing book
- **Permission**: IsAuthenticated (authenticated users only)
- **Generic View**: `UpdateAPIView`

### BookDeleteView (DeleteView)
- **Purpose**: Remove a book
- **Permission**: IsAuthenticated (authenticated users only)
- **Generic View**: `DestroyAPIView`

## Testing the API

### Using curl:

```bash
# List all books
curl -X GET http://localhost:8000/api/books/

# Get specific book
curl -X GET http://localhost:8000/api/books/1/

# Create book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "New Book", "publication_year": 2023, "author": 1}'

# Update book (requires authentication)
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Updated Book", "publication_year": 2023, "author": 1}'

# Delete book (requires authentication)
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN"
```