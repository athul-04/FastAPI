from fastapi import FastAPI,HTTPException,Path,Query
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status
app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id:Optional[int]=Field(description="ID is not needed on create",default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=6)
    published_date:int=Field(gt=1999,lt=2031)


    model_config={
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"Athul",
                "description":"This is a sample description of the new book",
                "rating":5,
                "published_date":2000
            }
        }
    }



BOOKS = [
    Book(1, "The Astral Gate", "Ronan Vale",
         "A sci-fi adventure through parallel worlds.", 5, 2012),

    Book(2, "Whispers in the Fog", "Elara Finch",
         "A mystery set in a quiet fog‑covered town.", 4, 2016),

    Book(3, "The Silent Kingdom", "Marion Hale",
         "A fantasy kingdom where music controls magic.", 5, 2019),

    Book(4, "Echoes of the Deep", "Tristan Grey",
         "A deep‑sea journey uncovering ancient ruins.", 4, 2014),

    Book(5, "Forgotten Skies", "Lydia Cross",
         "A dystopian world where no one has seen the sky for centuries.", 3, 2011),

    Book(6, "Clockwork Rebellion", "Jasper Thorn",
         "Steampunk machines rise up with free will.", 4, 2018),

    Book(7, "Fragments of Aurora", "Selene Ward",
         "A woman pieces together her lost memories.", 5, 2020),

    Book(8, "The Crimson Cipher", "Damien Crest",
         "A spy thriller about an unbreakable code.", 4, 2015),

    Book(9, "Beneath the Willow Tree", "Harper Dean",
         "A touching tale of friendship and healing.", 5, 2013),

    Book(10, "The Quantum Paradox", "Felix Orion",
         "A physicist faces a reality‑breaking time anomaly.", 5, 2021)
]



@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.post("/create_new_book",status_code=status.HTTP_201_CREATED)
async def create_new_book(bookParams:BookRequest):
    new_book=Book(**bookParams.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book     
    HTTPException(status_code=404,detail="No such book found with id {}".format(book_id))

@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating:int=Query(gt=-1,lt=6)):
    for book in BOOKS:
        if book.rating==rating:
            return book     
    HTTPException(status_code=404,detail="No such book found with rating {}".format(rating))


@app.put("/books/update",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updatedbook:BookRequest):
    update_book=Book(**updatedbook.model_dump())
    for idx,book in enumerate(BOOKS):
        if book.id==update_book.id:
            BOOKS[idx]=update_book
            return BOOKS
    raise HTTPException(status_code=404,detail="No such book exists with id")
    
    

@app.get("/books/filter/",status_code=status.HTTP_200_OK)
async def filter_by_published_date(published_date:int=Query(gt=1999,lt=2031)):
    books=[]
    for book in BOOKS:
        if book.published_date==published_date:books.append(book)
    return books    



def find_book_id(book:Book):
    book.id= 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book 



