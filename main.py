import mysql.connector
import logging

#a
class Buku:
    def __init__(self, judul, penulis, konten, penerbit=None, tahun_terbit=None, iktisar=None):
        self.judul = judul
        self.penulis = penulis
        self.konten = konten
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.iktisar = iktisar

    def read(self, nomor_halaman):
        for i, bab in enumerate(self.konten, start=1):
            if i <= nomor_halaman:
                print(f"Halaman {i}: {bab}")
            else:
                break

    def __str__(self):
        return f"{self.judul} by {self.penulis}"

#c
class BukuRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_buku(self, id):
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()

        query = "SELECT * FROM buku WHERE id = %s"
        cursor.execute(query, (id,))

        result = cursor.fetchone()
        if result:
            buku = Buku(*result[1:]) 
            return buku
        else:
            return None

        cursor.close()
        cnx.close()

#d
def post_buku(self, buku):
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()

        query = "INSERT INTO buku (judul, penulis, konten, penerbit, tahun_terbit, iktisar) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            buku.judul,
            buku.penulis,
            buku.konten,
            buku.penerbit,
            buku.tahun_terbit,
            buku.iktisar
        ))

        cnx.commit()
        cursor.close()
        cnx.close()

#e
class BukuLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

class HTTPException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

#pengguna
buku = Buku("Mathematics for Machine Learning", "Marc Peter Deisenroth", ["Introduction", "Linear Algebra", "Calculus"])
print(buku) 
buku.read(2) 
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'perpustakaan'
}
repository = BukuRepository(db_config)
buku = Buku("Mathematics for Machine Learning", "Marc Peter Deisenroth", ["Introduction", "Linear Algebra", "Calculus"])
repository.post_buku(buku)
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'perpustakaan'
}
repository = BukuRepository(db_config)
buku = repository.get_buku(1) 
print(buku)  
logger = BukuLogger()
try:
    buku = Buku("Invalid book", None, []) 
except Exception as e:
    logger.logger.error(f"Error creating book: {e}")
try:
    buku = Buku("Invalid book", None, [])  
    raise HTTPException(400, "Invalid book request")
except HTTPException as e:
    print(f"Error {e.status_code}: {e.message}")