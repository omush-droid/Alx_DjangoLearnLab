import rest_framework.generics
import rest_framework.viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
