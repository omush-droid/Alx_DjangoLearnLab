import rest_framework.generics
from .models import Book
from .serializers import BookSerializer

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
