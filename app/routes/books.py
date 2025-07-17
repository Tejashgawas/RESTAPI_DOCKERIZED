from flask import Blueprint, request
from marshmallow import ValidationError
from app.schemas.book_schema import BookSchema
from app.models.book import Book
from app import db
from app.utils.response import success_response, error_response
from sqlalchemy import or_, asc, desc
from flasgger import swag_from

books_bp = Blueprint('books_bp', __name__, url_prefix='/books')
book_schema = BookSchema()

# ✅ GET all books
@books_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Books'],
    'parameters': [
        {'name': 'search', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Search by title or author'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'default': 10},
        {'name': 'sort', 'in': 'query', 'type': 'string', 'enum': ['id', 'title', 'author'], 'default': 'id'},
        {'name': 'order', 'in': 'query', 'type': 'string', 'enum': ['asc', 'desc'], 'default': 'asc'},
    ],
    'responses': {
        200: {
            'description': 'Books fetched successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'pages': {'type': 'integer'},
                    'limit': {'type': 'integer'},
                    'books': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    }
                }
            }
        }
    }
})
def get_books():
    # Get query params
    search_query = request.args.get('search', '', type=str)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    sort_field = request.args.get('sort', 'id', type=str)
    sort_order = request.args.get('order', 'asc', type=str)

    # Base query
    query = Book.query

    # 🔍 Search filter (case-insensitive match)
    if search_query:
        query = query.filter(or_(
            Book.title.ilike(f'%{search_query}%'),
            Book.author.ilike(f'%{search_query}%')
        ))

    # ↕️ Sorting
    if sort_field in ['id', 'title', 'author']:
        sort_column = getattr(Book, sort_field)
        if sort_order == 'desc':
            sort_column = desc(sort_column)
        else:
            sort_column = asc(sort_column)
        query = query.order_by(sort_column)

    # 📄 Pagination
    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    # Result list
    books = [book.to_dict() for book in paginated.items]

    return success_response({
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages,
        "limit": paginated.per_page,
        "books": books
    }, "Books fetched with filters", 200)

# ✅ GET a book by ID
@books_bp.route('/<int:book_id>', methods=['GET'])
@swag_from({
    'tags': ['Books'],
    'parameters': [
        {'name': 'book_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Book ID'}
    ],
    'responses': {
        200: {
            'description': 'Book found',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'title': {'type': 'string'},
                    'author': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Book not found'}
    }
})
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return success_response(book.to_dict(), "Book found", 200)
    return error_response("Book not found", 404)

# ✅ POST - Add a new book
@books_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Books'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title', 'author'],
                'properties': {
                    'title': {'type': 'string', 'example': 'Atomic Habits'},
                    'author': {'type': 'string', 'example': 'James Clear'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Book added successfully'},
        400: {'description': 'Validation error'}
    }
})
def add_book():
    try:
        data = request.get_json()
        validated = book_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)

    book = Book(title=validated['title'], author=validated['author'])
    db.session.add(book)
    db.session.commit()

    return success_response(book.to_dict(), "Book added successfully", 201)

# ✅ PUT - Update book by ID
@books_bp.route('/<int:book_id>', methods=['PUT'])
@swag_from({
    'tags': ['Books'],
    'consumes': ['application/json'],
    'parameters': [
        {'name': 'book_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string', 'example': 'Updated Title'},
                    'author': {'type': 'string', 'example': 'Updated Author'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Book updated successfully'},
        404: {'description': 'Book not found'}
    }
})
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error_response("Book not found", 404)

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()

    return success_response(book.to_dict(), "Book updated successfully", 200)

# ✅ DELETE - Delete book by ID
@books_bp.route('/<int:book_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Books'],
    'parameters': [
        {'name': 'book_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Book deleted successfully'},
        404: {'description': 'Book not found'}
    }
})
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error_response("Book not found", 404)

    db.session.delete(book)
    db.session.commit()
    return success_response(None, "Book deleted successfully", 200)
