

# 📘 **Library Search API — README**

A fully‑validated FastAPI project that provides flexible search, filtering, and sorting capabilities for a collection of books.  
This API demonstrates strong parameter validation, Enum usage, pagination, and clean routing design.

---

## 🚀 **Overview**

The Library Search API supports:

- Listing books with multiple optional filters  
- Searching book titles  
- Filtering by genre  
- Filtering by publication year ranges  
- Pagination with skip/limit  
- Sorting by title or year  
- Retrieving a specific book by ID  

All validation is handled by FastAPI’s `Query` and `Path` utilities.

Swagger UI is available at:

```
/docs
```

---

## 🧱 **Project Structure**

```
app/
│
├── main.py
│
└── routers/
    └── library_route.py
```

---

## 📚 **Sample Data**

The API includes **8 sample books**, each with:

- `id`
- `title`
- `year`
- `genre` (Enum)

Genres are strictly validated using:

- fiction  
- nonfiction  
- science  
- history  

---

## 🔌 **Endpoints**

### **GET /books**

List books with optional filters:

| Parameter | Type | Validation | Description |
|----------|------|------------|-------------|
| genre | Enum | fiction/nonfiction/science/history | Filter by genre |
| min_year | int | > 0 | Minimum publication year |
| max_year | int | > 0 | Maximum publication year |
| search | str | min_length=1 | Case‑insensitive title search |
| skip | int | ≥ 0 | Pagination offset |
| limit | int | 1–25 | Pagination limit (capped at 25) |

Supports combining filters:

```
/books?genre=science&min_year=2000&search=star&limit=5
```

---

### **GET /books/{book_id}**

Retrieve a single book by ID.

Validation:

- `book_id` must be **greater than 0**
- Returns **404** if not found

---

### **GET /books/genre/{genre}**

List all books in a genre.

Optional sorting:

```
sort_by=title
sort_by=year
```

Validation:

- `sort_by` must match regex: `^(title|year)$`

Example:

```
/books/genre/history?sort_by=year
```

---

## 🧪 **Validation Behavior**

The API returns clear `422 Unprocessable Entity` errors for:

- Invalid genre values  
- Negative or zero IDs  
- `min_year <= 0`  
- `search` shorter than 1 character  
- `limit > 25`  
- Invalid `sort_by` values  

---

## 🏁 **Running the API**

Start the server:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## 🧠 **WHY / DESIGN Commentary**

This project demonstrates:

- Clean separation of routing and validation  
- Proper use of FastAPI’s `Query` and `Path`  
- Enum‑based filtering  
- Pagination with strict caps  
- Regex‑validated sorting  
- Predictable behavior for empty results  
- Strong error handling (404 and 422 responses)

The router is intentionally strict, ensuring invalid input is rejected early while still allowing flexible combinations of filters.

---

## 📌 **Next Steps**

- Add author fields
- Add sorting by multiple fields
- Add POST/PUT endpoints
- Convert books to Pydantic models

