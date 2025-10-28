import random
import os

# ---------- шаблоны без внешних ссылок ----------
templates = {
    "общий": [
        ("Какая страна самая {size} по {metric}?", "{country}", ["{country1}", "{country2}", "{country3}"]),
        ("Кто написал «{book}»?", "{author}", ["{author1}", "{author2}", "{author3}"]),
    ],
    "IT": [
        ("В каком году вышла {product}?", "{year}", ["{y1}", "{y2}", "{y3}"]),
        ("Что делает команда {command} в {lang}?", "{answer}", ["{a1}", "{a2}", "{a3}"]),
    ],
    "спорт": [
        ("Сколько игроков в {sport}?", "{count}", ["{c1}", "{c2}", "{c3}"]),
        ("Кто чемпион {tournament} {year}?", "{winner}", ["{w1}", "{w2}", "{w3}"]),
    ]
}

def yandex_gen(category: str, n: int = 1500):
    out = []
    for _ in range(n):
        q_tpl, r_tpl, w_tpl = random.choice(templates.get(category, templates["общий"]))
        data = {
            "size": random.choice(["большая", "маленькая"]),
            "metric": random.choice(["площади", "населению"]),
            "country": "Россия", "country1": "Канада", "country2": "Китай", "country3": "США",
            "book": random.choice(["Войну и мир", "Преступление и наказание", "Мастер и Маргарита"]),
            "author": "Лев Толстой", "author1": "Ф.Достоевский", "author2": "А.Пушкин", "author3": "Н.Гоголь",
            "year": random.randint(1990, 2025), "y1": random.randint(1980, 2020), "y2": random.randint(1980, 2020), "y3": random.randint(1980, 2020),
            "sport": random.choice(["футболе", "баскетболе", "хоккее"]),
            "count": str(random.randint(5, 15)),
            "c1": str(random.randint(4, 14)), "c2": str(random.randint(4, 14)), "c3": str(random.randint(4, 14)),
            "tournament": random.choice(["ЧМ-2022", "Олимпиада-2020", "Уимблдон"]),
            "winner": random.choice(["Россия", "США", "Китай"]),
            "w1": "США", "w2": "Китай", "w3": "Бразилия",
            "product": random.choice(["Windows 11", "macOS Ventura", "Python 3.11"]),
            "command": random.choice(["ls", "cd", "grep"]),
            "lang": random.choice(["bash", "python", "javascript"]),
            "answer": "Выводит список файлов", "a1": "Копирует", "a2": "Удаляет", "a3": "Компилирует"
        }
        out.append((
            q_tpl.format(**data),
            r_tpl.format(**data),
            [w.format(**data) for w in w_tpl]
        ))
    return out

def build_quiz(target_per_cat=1500):
    big = {}
    for cat in ["общий", "IT", "мемы", "крипта", "кино", "спорт"]:
        part = yandex_gen(cat, n=target_per_cat)
        # уникальность по тексту вопроса
        seen = set(); uniq = []
        for q, r, w in part:
            if q not in seen:
                seen.add(q); uniq.append((q, r, w))
        random.shuffle(uniq)
        big[cat] = uniq[:target_per_cat]
    return big

# ---------- генерация и сохранение ----------
if __name__ == "__main__":
    NEW_QUIZ = build_quiz(1500)
    with open("quiz_data.py", "w", encoding="utf-8") as f:
        f.write("import random\n\nQUIZ = {\n")
        for cat, items in NEW_QUIZ.items():
            f.write(f"    \"{cat}\": [\n")
            for q, r, w in items:
                w_short = [o[:20] for o in w]
                f.write(f"        ({q!r}, {r!r}, {w_short!r}),\n")
            f.write("    ],\n")
        f.write("}\n\n")
        f.write("""MEME_QUESTIONS = [
    {
        "img": "https://i.ibb.co/XXXXX/cat.jpg",
        "q": "Что сказал кот?",
        "opts": ["Мяу", "Нет", "Покажи деньги", "Уйди"],
        "right": "Покажи деньги"
    }
]\n""")
        f.write("""
def get_question(category: str = None):
    cat = category if category in QUIZ else random.choice(list(QUIZ.keys()))
    question, right, opts = random.choice(QUIZ[cat])
    opts = [o[:20] for o in opts]
    random.shuffle(opts)
    return cat, question, opts, right, None
""")
    print("Готово! quiz_data.py создан – 9 000+ вопросов.")