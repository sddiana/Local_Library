from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View 

@login_required
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
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

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
            'num_visits':num_visits,
        },
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.all().order_by('title')

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    #paginate_by = 2
    
    def get_queryset(self):
        return Author.objects.all().order_by('last_name', 'first_name')

class AuthorDetailView(generic.DetailView):
    model = Author

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        # Добавь метод get
        return render(request, 'catalog/my_protected_page.html')
    
    def post(self, request):
        # Добавь метод post если нужен
        pass

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/all_borrowed_books.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').select_related('book', 'borrower').order_by('due_back')