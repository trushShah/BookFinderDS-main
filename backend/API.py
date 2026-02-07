from fastapi import FastAPI, HTTPException, Query
import sqlite3
import faiss
from sentence_transformers import SentenceTransformer

app = FastAPI(
    title="Book Information API",
    description="API to fetch books data from a server",
    version='1.0.0'
)

DB_PATH = "books.db"

VDB_PATH = "books.faiss"

MODEL_PATH = "./minilm"

model = SentenceTransformer(MODEL_PATH)

vdb = faiss.read_index(VDB_PATH)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def root():
    return {
        "message": "Book API is up"
        }


@app.get("/books")
def get_books(
    limit: int = Query(None, ge=1, le=31532, description="Number of books to fetch (leave empty if trying to fetch all)")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    if limit is None:
        cursor.execute("""
            SELECT *
            FROM book
            ORDER BY AccDate DESC
        """)
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"code": 200, "count": len(books), "data":books}
        
    cursor.execute("""
        SELECT *
        FROM book
        ORDER BY AccNo
        LIMIT ?
    """, (limit, ))

    books = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "code": 200,
        "count": len(books),
        "data": books
    }

@app.get("/books/{id}")
def get_book_by_isbn_path(id: str):
    id = id.strip().replace("-", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM book
        WHERE ISBN = ? OR ISBN13 = ? OR AccNo = ? OR DDC = ?
    """, (id, id, id, id))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return dict(row)

@app.get("/name/{name}")
def get_book_by_name(name:str):
    name = name.strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM book WHERE TRIM(title) LIKE TRIM(?)", (f"%{name}%",))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row)

def aggregate_results(result):

    scores, indices = result
    
    agg = {}

    for i, s in zip(indices[0].tolist(), scores[0].tolist()):
        agg[i] = agg.get(i, 0) + s

    return sorted(agg.items(), key=lambda x: x[1], reverse=True)

@app.get("/query/{query}")
def get_books_by_query(query: str):
    query = model.encode([query], normalize_embeddings=True).astype('float32')
    results = vdb.search(query, 10)
    conn = get_db_connection()
    cursor = conn.cursor()
    agg_res = aggregate_results(results)
    ids = [id for id, _ in agg_res]
    
    rows = cursor.execute(
        f"SELECT * FROM book WHERE AccNo IN ({','.join('?'*len(ids))})",
        ids
    ).fetchall()
    
    row_map = {row["AccNo"]: row for row in rows}
    ordered = [row_map[i] for i in ids if i in row_map]
    return ordered

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)