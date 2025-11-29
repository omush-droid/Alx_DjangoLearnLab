# Testing Documentation

## Testing Strategy

This project uses Django's built-in testing framework to ensure API functionality, data integrity, and security controls.

## Test Database Configuration

- **Separate Test Database**: Configured to use in-memory SQLite database during testing
- **No Impact on Production**: Tests run in isolation without affecting development or production data
- **Configuration**: Located in `settings.py` with conditional database setup

## Test Cases Implemented

### CRUD Operations Testing
1. **Book List View** - Tests retrieving all books (GET /api/books/)
2. **Book Detail View** - Tests retrieving single book (GET /api/books/{id}/)
3. **Book Create** - Tests creating new books (POST /api/books/create/)
4. **Book Update** - Tests updating existing books (PUT /api/books/update/{id}/)
5. **Book Delete** - Tests deleting books (DELETE /api/books/delete/{id}/)

### Authentication & Permission Testing
- **Authenticated Operations** - Verifies CRUD operations work with authentication
- **Unauthenticated Operations** - Ensures proper 403 Forbidden responses
- **Permission Enforcement** - Tests IsAuthenticatedOrReadOnly permission class

### Advanced Features Testing
- **Filtering** - Tests filtering books by publication_year
- **Searching** - Tests search functionality on title field
- **Ordering** - Tests ordering books by title

## Status Code Verification

Tests verify correct HTTP status codes:
- **200 OK** - Successful GET requests
- **201 Created** - Successful POST requests
- **204 No Content** - Successful DELETE requests
- **403 Forbidden** - Unauthenticated write operations

## Running Tests

### Execute All Tests
```bash
python manage.py test api
```

### Execute Specific Test Class
```bash
python manage.py test api.test_views.BookAPITestCase
```

### Execute Specific Test Method
```bash
python manage.py test api.test_views.BookAPITestCase.test_book_create_authenticated
```

## Test Results Interpretation

- **OK** - All tests passed successfully
- **FAILED** - One or more tests failed (details provided)
- **ERROR** - Test execution error (check setup/configuration)

## Test Coverage

The test suite covers:
- ✅ All CRUD operations
- ✅ Authentication and permissions
- ✅ Filtering, searching, and ordering
- ✅ Correct status codes
- ✅ Data integrity verification
- ✅ Security controls enforcement