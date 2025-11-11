from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

#inline class

class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ('title', 'isbn')
    show_change_link = True

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1
    fields = ('status', 'due_back', 'imprint')
    show_change_link = True

# admin class

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', 'imprint')
    list_filter = ('status', 'due_back') 
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

#регистрация моделей

admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)