import datetime
from django.contrib import admin
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion


class BookInline(admin.StackedInline):
    model = Book  # This shows all fields of Book.
    fields = [('title', 'author'), 'duedate',]   #  Customizes to show only certain fields
    extra = 0

class DvdInline(admin.TabularInline):
    model = Dvd  # This shows all fields of Dvd.
    fields = [('title', 'maker', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'), ('rating','num_chkout','duration')]
    extra = 0

class LibuserAdmin(admin.ModelAdmin):
    # fields = [('username'), ('first_name', 'last_name')]
    inlines = [BookInline, DvdInline]


def renew(modeladmin, request, queryset):
    for item in queryset:
        if item.checked_out== True:
            item.duedate = datetime.date.today() + datetime.timedelta(21)
            item.save()

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'category']
    list_display = ('title', 'borrower','overdue')
    actions = [renew]
    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''

class DvdAdmin(admin.ModelAdmin):
    fields = [('title', 'maker', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'), 'rating']
    list_display = ('title','rating', 'borrower','overdue')
    actions = [renew]
    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user  # Returns the user who has borrowed this book
        else:
            return ''



# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Dvd, DvdAdmin)
admin.site.register(Libuser,LibuserAdmin)
admin.site.register(Suggestion)