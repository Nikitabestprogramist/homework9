import redis
from models import Quote, Author
from bson import ObjectId


r = redis.Redis(host="localhost", port=6379, decode_responses=True)

HELP = """Команди:
  name:<частина_імені>   — цитати автора
  tag:<частина_тегу>     — цитати для одного тегу
  tags:tag1,tag2         — цитати, де є ХОЧА Б ОДИН із тегів
  exit                   — вийти
"""

print(HELP)

while True:
    cmd = input(">>> ").strip()
    if cmd == "exit":
        break
    if ":" not in cmd:
        print("Невірний формат. Спробуйте ще.")
        continue

    key, value = cmd.split(":", 1)
    cache_key = cmd


    if r.exists(cache_key):
        print("🟢 Кеш:")
        print(r.get(cache_key))
        continue


    if key == "name":
        authors = Author.objects(fullname__istartswith=value)
        quotes  = Quote.objects(author__in=authors)
    elif key == "tag":
        quotes = Quote.objects(tags__istartswith=value)
    elif key == "tags":
        tag_list = value.split(",")
        quotes   = Quote.objects(tags__in=tag_list)
    else:
        print("Невідома команда")
        continue


    result = "\n".join(f"- {q.quote}" for q in quotes)
    print(result or "Нічого не знайдено")


    r.set(cache_key, result, ex=300)
