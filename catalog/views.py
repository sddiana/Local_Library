from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre  # ← ДОБАВЬТЕ ИМПОРТ!

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    keyword = 'Маленькие'
    num_books_with_keyword = Book.objects.filter(title__icontains=keyword).count()

    keyword_genres = 'Novels'
    num_genres_with_keyword = Genre.objects.filter(name__icontains=keyword_genres).count()

    return render(
        request,
        'catalog/index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_books_with_keyword': num_books_with_keyword,
            'keyword': keyword,
            'num_genres_with_keyword': num_genres_with_keyword,
            'keyword_genres': keyword_genres,
        },
    )

def book_list(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'catalog/book_list.html', {
        'book_list': books
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {
        'book': book
    })

def author_list(request):
    authors = Author.objects.all().order_by('last_name', 'first_name')
    return render(request, 'catalog/author_list.html', {
        'author_list': authors
    })

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'catalog/author_detail.html', {
        'author': author
    })