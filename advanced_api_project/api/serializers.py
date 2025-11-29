from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for the Book model
# Handles one book at a time and validates year
class BookSerializer(serializers.ModelSerializer):

    # Custom validation to ensure year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = '__all__'   # title, publication_year, author
        

# Serializer for the Author model
# Includes a nested serializer of all books written by the author
class AuthorSerializer(serializers.ModelSerializer):
    # This automatically serializes all related Book objects
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
        # 'books' comes from related_name='books' in the Book model