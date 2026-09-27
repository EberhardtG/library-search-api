"""
WHY:
The Library Search API router provides flexible, validated search capabilities
for a collection of books. It demonstrates how path parameters, query
parameters, enums, and pagination work together to create a predictable and
user-friendly search interface. The router is intentionally strict in its
validation to ensure that invalid input produces clear errors, while still
remaining flexible enough for real-world search scenarios.

DESIGN:
1. A Genre Enum restricts genre filtering to four valid categories. This prevents
   invalid input and ensures consistent behavior across all endpoints.

2. The sample dataset includes at least eight books, providing enough variety to
   meaningfully test filtering, searching, sorting, and pagination.

3. The GET /books endpoint supports multiple optional filters:
   - genre: filters by a validated Enum value
   - min_year: validated to be greater than zero
   - max_year: optional upper bound on publication year
   - search: case-insensitive substring match on book titles
   - skip and limit: pagination with a strict maximum limit of 25
   These filters can be combined freely, giving clients flexible search options.
   Edge cases such as skip exceeding the result count or empty filter results
   intentionally return empty lists rather than errors.

4. The GET /books/{book_id} endpoint validates that the ID is greater than zero
   using Path(), ensuring correct usage of FastAPI's parameter types. A clear
   404 error is returned when the book does not exist.

5. The GET /books/genre/{genre} endpoint provides genre-specific browsing with
   optional sorting by title or year. The sort_by parameter is validated using a
   regex pattern, ensuring only supported values are accepted and rejecting
   invalid or uppercase variants.

6. All parameters use FastAPI's Query and Path validation features, ensuring
   that invalid input produces clear 422 errors in Swagger UI. Logical edge
   cases—such as min_year greater than max_year—result in empty lists, keeping
   the API predictable and easy to consume.

Overall, this router demonstrates clean API design, strong validation, and
flexible search functionality. It serves as a solid foundation for more advanced
library or catalog systems while maintaining strict, predictable behavior across
all endpoints.
"""




from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query, Path
from enum import Enum
from typing import Optional

router = APIRouter(prefix="/books", tags=["Library"])

# -----------------------------
# ENUM
# -----------------------------
class Genre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    science = "science"
    history = "history"

# -----------------------------
# SAMPLE DATA
# -----------------------------
books_db = [
    {"id": 1, "title": "The Silent Forest", "year": 1998, "genre": Genre.fiction},
    {"id": 2, "title": "Quantum Realities", "year": 2010, "genre": Genre.science},
    {"id": 3, "title": "Ancient Civilizations", "year": 1985, "genre": Genre.history},
    {"id": 4, "title": "The Human Mind", "year": 2005, "genre": Genre.nonfiction},
    {"id": 5, "title": "Stars and Beyond", "year": 2020, "genre": Genre.science},
    {"id": 6, "title": "War Stories", "year": 1992, "genre": Genre.history},
    {"id": 7, "title": "Life Lessons", "year": 2015, "genre": Genre.nonfiction},
    {"id": 8, "title": "Dreamcatcher", "year": 2001, "genre": Genre.fiction},
]

# -----------------------------
# GET /books — with filters
# -----------------------------
@router.get("/")
def list_books(
    genre: Optional[Genre] = None,
    min_year: Optional[int] = Query(None, gt=0),
    max_year: Optional[int] = Query(None, gt=0),
    search: Optional[str] = Query(None, min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=25),
):
    results = books_db

    if genre:
        results = [b for b in results if b["genre"] == genre]

    if min_year:
        results = [b for b in results if b["year"] >= min_year]

    if max_year:
        results = [b for b in results if b["year"] <= max_year]

    if search:
        results = [b for b in results if search.lower() in b["title"].lower()]

    return results[skip : skip + limit]

# -----------------------------
# GET /books/{book_id}
# -----------------------------

@router.get("/{book_id}")
def get_book(book_id: int = Path(..., gt=0)):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# -----------------------------
# GET /books/genre/{genre}
# -----------------------------
@router.get("/genre/{genre}")
def list_books_by_genre(
    genre: Genre,
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$"),
):
    results = [b for b in books_db if b["genre"] == genre]

    if sort_by == "title":
        results = sorted(results, key=lambda b: b["title"])
    elif sort_by == "year":
        results = sorted(results, key=lambda b: b["year"])

    return results
