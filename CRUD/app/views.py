from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Book
import json


@csrf_exempt
@require_http_methods(["GET"])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        data = list(books.values('id', 'title', 'author', 'published_date'))
        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_http_methods(["POST"])
def create_book(request):
    data = json.loads(request.body)
    title = data.get('title')
    author = data.get('author')
    published_date = data.get('published_date')

    if not title or not author or not published_date:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    book = Book(title=title, author=author, published_date=published_date)
    book.save()

    return JsonResponse({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date
    }, status=201)


@csrf_exempt
@require_http_methods(["GET"])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date
    }
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["PUT"])
def update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    data = json.loads(request.body)
    title = data.get('title', book.title)
    author = data.get('author', book.author)
    published_date = data.get('published_date', book.published_date)

    book.title = title
    book.author = author
    book.published_date = published_date
    book.save()

    return JsonResponse({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    book.delete()
    return JsonResponse({'message': 'Book deleted successfully'})
