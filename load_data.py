import json
from models import Author, Quote

def load_authors(path="authors.json"):
    with open(path, encoding="utf-8") as f:
        for item in json.load(f):
            Author.objects(fullname=item["fullname"]).update_one(
                set__born_date=item["born_date"],
                set__born_location=item["born_location"],
                set__description=item["description"],
                upsert=True
            )

def load_quotes(path="qoutes.json"):
    with open(path, encoding="utf-8") as f:
        for item in json.load(f):
            author = Author.objects.get(fullname=item["author"])
            Quote(
                tags=item["tags"],
                author=author,
                quote=item["quote"]
            ).save()

if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("✓ Дані успішно завантажено")
