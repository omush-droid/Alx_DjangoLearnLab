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

## Advanced Query Features

### Filtering
Filter books by specific field values:
- `/api/books/?title=Book Title`
- `/api/books/?author=1`
- `/api/books/?publication_year=2023`

### Searching
Search across title and author name:
- `/api/books/?search=python`
- `/api/books/?search=author name`

### Ordering
Order results by any field:
- `/api/books/?ordering=title` (ascending)
- `/api/books/?ordering=-publication_year` (descending)
- `/api/books/?ordering=title,publication_year` (multiple fields)

### Combined Queries
Combine filtering, searching, and ordering:
- `/api/books/?search=python&ordering=-publication_year&author=1`

## Testing the API

### Using curl:

```bash
# List all books
curl -X GET http://localhost:8000/api/books/

# Filter books by publication year
curl -X GET "http://localhost:8000/api/books/?publication_year=2023"

# Search for books
curl -X GET "http://localhost:8000/api/books/?search=python"

# Order books by title
curl -X GET "http://localhost:8000/api/books/?ordering=title"

# Combined query
curl -X GET "http://localhost:8000/api/books/?search=book&ordering=-publication_year"

# Get specific book
curl -X GET http://localhost:8000/api/books/1/

# Create book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "New Book", "publication_year": 2023, "author": 1}'

# Update book (requires authentication)
curl -X PUT http://localhost:8000/api/books/update/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Updated Book", "publication_year": 2023, "author": 1}'

# Delete book (requires authentication)
curl -X DELETE http://localhost:8000/api/books/delete/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```