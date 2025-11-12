from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

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

class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list'
    
    def get_queryset(self):
        return Book.objects.all().order_by('title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'
    
    def get_queryset(self):
        return Author.objects.all().order_by('last_name', 'first_name')

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'