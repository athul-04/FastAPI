from fastapi import FastAPI,HTTPException,Body

app=FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Time Weaver",
        "author": "Elias Ward",
        "category": "Science Fiction"
    },
    {
        "id": 2,
        "title": "Shadows of Aramore",
        "author": "Liana Crestfall",
        "category": "Fantasy"
    },
    {
        "id": 3,
        "title": "Beyond the Silent River",
        "author": "Marcus Hale",
        "category": "Adventure"
    },
    {
        "id": 4,
        "title": "Fragments of Yesterday",
        "author": "Nora Everly",
        "category": "Drama"
    },
    {
        "id": 5,
        "title": "The Arcane Paradox",
        "author": "Victor Renn",
        "category": "Mystery"
    },
    {
        "id": 6,
        "title": "The Arcane Paradox 2",
        "author": "Victor Renn",
        "category": "Mystery"
    }
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{dynamic_book}")
async def get_book(dynamic_book:int):
    for book in BOOKS:
        if book.get("id")==dynamic_book:
            return book
    raise HTTPException(status_code=404,detail="Book not found error")


@app.get("/books/")
async def get_books_via_queryParam(category:str):
    for book in BOOKS:
        if book.get("category").casefold()==category.casefold():
            return book
    raise HTTPException(status_code=404,detail="No such book found")


@app.get("/books/{dynamic_id}")
async def get_book_via_queryParam(dynamic_id:int,category:str):

    return [ x for x in BOOKS if x.get("id")==dynamic_id and x.get("category").casefold()==category.casefold()]


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    return BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for idx,book in enumerate(BOOKS):
        if book.get("id")==updated_book.get("id"):
            BOOKS[idx]=updated_book
            return BOOKS
    raise HTTPException(status_code=404,detail="Book not found for update")


@app.delete("/books/{book_id}")
async def delete_book(book_id:int):
    for idx,book in enumerate(BOOKS):
        if book.get("id")==book_id:
            del BOOKS[idx]
            return BOOKS
    raise HTTPException(status_code=404,detail="No such book found")
    



