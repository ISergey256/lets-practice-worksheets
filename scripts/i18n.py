"""Texts of the worksheets in several languages.

W[lang]  - what the child reads on the worksheet (task instructions, labels, word banks).
A[lang]  - the answer page for parents.
numwords(lang, n), ordinal(lang, n) - number words (task 6) and ordinals for ducks (task 18).

The worksheet language and the answer language are chosen separately (both default to English).
To add a language: copy the "en" entries of W and A, translate them, add numwords/ordinal rules
and the language name to LANGS. Keys must stay the same; values can be strings with {placeholders}
or functions (when the wording depends on a number, e.g. Russian "3 стороны" / "5 сторон").
"""

LANGS = {"en": "English", "uk": "Українська", "ru": "Русский", "el": "Ελληνικά",
         "de": "Deutsch", "fr": "Français", "es": "Español"}
DEFAULT = "en"
SHY = chr(0xAD)  # soft hyphen: lets a very long word break inside a narrow box (e.g. the 3D word bank)


# ---------------------------------------------------------------- number words 0..99
def _en(n):
    ones = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
            "sixteen seventeen eighteen nineteen").split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    return ones[n] if n < 20 else tens[n // 10] + ("" if n % 10 == 0 else "-" + ones[n % 10])


def _ru(n):
    ones = ("ноль один два три четыре пять шесть семь восемь девять десять одиннадцать двенадцать тринадцать "
            "четырнадцать пятнадцать шестнадцать семнадцать восемнадцать девятнадцать").split()
    tens = "_ _ двадцать тридцать сорок пятьдесят шестьдесят семьдесят восемьдесят девяносто".split()
    return ones[n] if n < 20 else tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])


def _uk(n):
    ones = ("нуль один два три чотири п’ять шість сім вісім дев’ять десять одинадцять дванадцять тринадцять "
            "чотирнадцять п’ятнадцять шістнадцять сімнадцять вісімнадцять дев’ятнадцять").split()
    tens = "_ _ двадцять тридцять сорок п’ятдесят шістдесят сімдесят вісімдесят дев’яносто".split()
    return ones[n] if n < 20 else tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])


def _el(n):
    ones = ("μηδέν ένα δύο τρία τέσσερα πέντε έξι επτά οκτώ εννέα δέκα έντεκα δώδεκα δεκατρία "
            "δεκατέσσερα δεκαπέντε δεκαέξι δεκαεπτά δεκαοκτώ δεκαεννέα").split()
    tens = "_ _ είκοσι τριάντα σαράντα πενήντα εξήντα εβδομήντα ογδόντα ενενήντα".split()
    return ones[n] if n < 20 else tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])


def _de(n):
    ones = ("null eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn "
            "fünfzehn sechzehn siebzehn achtzehn neunzehn").split()
    tens = "_ _ zwanzig dreißig vierzig fünfzig sechzig siebzig achtzig neunzig".split()
    if n < 20:
        return ones[n]
    u = n % 10
    return tens[n // 10] if u == 0 else ("ein" if u == 1 else ones[u]) + "und" + tens[n // 10]


def _fr(n):
    ones = ("zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize "
            "dix-sept dix-huit dix-neuf").split()
    tens = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
    if n < 20:
        return ones[n]
    if n < 70:
        t, u = divmod(n, 10)
        return tens[t] + ("" if u == 0 else " et un" if u == 1 else "-" + ones[u])
    if n < 80:  # 70..79 = soixante + 10..19
        return "soixante" + (" et onze" if n == 71 else "-" + ones[n - 60])
    if n == 80:
        return "quatre-vingts"
    return "quatre-vingt-" + ones[n - 80]  # 81..99: quatre-vingt-un, ..., quatre-vingt-dix-neuf


def _es(n):
    ones = ("cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince "
            "dieciséis diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro "
            "veinticinco veintiséis veintisiete veintiocho veintinueve").split()
    tens = "_ _ veinte treinta cuarenta cincuenta sesenta setenta ochenta noventa".split()
    if n < 30:
        return ones[n]
    t, u = divmod(n, 10)
    return tens[t] + ("" if u == 0 else " y " + ones[u])


_NUMWORDS = {"en": _en, "ru": _ru, "uk": _uk, "el": _el, "de": _de, "fr": _fr, "es": _es}


def numwords(lang, n):
    return _NUMWORDS[lang](n)


# ---------------------------------------------------------------- ordinals for "the n-th duck"
def ordinal(lang, n):
    if lang == "en":
        return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
    return {"ru": f"{n}-я",        # утка (f.)
            "uk": f"{n}-а",        # качка (f.)
            "el": f"{n}η",         # η πάπια (f.)
            "de": f"{n}.",
            "fr": "1er" if n == 1 else f"{n}e",   # le canard (m.)
            "es": f"{n}.º",        # el pato (m.)
            }[lang]


def _sides_ru(n):
    return f"Обведи фигуру, у которой {n} {'стороны' if n in (3, 4) else 'сторон'}."


def _sides_uk(n):
    return f"Обведи фігуру, яка має {n} {'сторони' if n in (3, 4) else 'сторін'}."


# ---------------------------------------------------------------- worksheet texts
W = {
    "en": {
        "title": "LET'S PRACTICE!", "badge": "Level {level} · No. {seed}", "name": "Name:", "date": "Date:",
        "what": {"fish": "fish", "apple": "apples", "star": "stars", "flower": "flowers", "ball": "balls", "heart": "hearts"},
        "t1": "Count the {what}. Write the number in the box.",
        "t2": "Estimate first. Then count the {what}.", "estimate": "My estimate:", "counted": "My count:",
        "t3_odd": "Circle all the odd numbers.", "t3_even": "Circle all the even numbers.",
        "t4": "Complete the missing numbers on the number line.",
        "t5": "Write &gt;, &lt; or = to compare the numbers.",
        "t6": "Write the numbers in words.",
        "t7": "Name the 3D shapes. Then count the faces and edges.",
        "th3": ("3D Shape", "Name", "Faces", "Edges"), "bank": "Word Bank",
        "shapes3d": {"cube": "cube", "cuboid": "cuboid", "cone": "cone", "cylinder": "cylinder",
                     "sphere": "sphere", "pyramid": "pyramid", "prism": "prism"},
        "t8": "Name and count the 2D shapes in the picture.",
        "th2": ("2D Shape", "How many?"), "shapes2d": ("Circles", "Triangles", "Squares", "Rectangles"),
        "t9": "Circle the shape that has {n} sides.",
        "t10": "Shade {frac} of each shape.",
        "frac": {"1/2": "one half (½)", "1/4": "one quarter (¼)", "1/3": "one third (⅓)", "3/4": "three quarters (¾)"},
        "t11": "Tick (✓) the shapes split into {n} equal parts.",
        "t12": "Compare.", "pencil_short": "Circle the shortest pencil.", "pencil_long": "Circle the longest pencil.",
        "tower_tall": "Circle the tallest tower.", "tower_low": "Circle the shortest tower.",
        "t13": "Find all the number bonds for {n}.",
        "t14": "Count in {s}s. Fill in the missing numbers.",
        "t15": "Complete the equations.",
        "t16": "Complete each wall.", "t16_sub": "Each brick is the two bricks under it added together.",
        "t17": "Look at the picture and complete the sentences with the positional words.",
        "pos": {"in": "in", "on": "on", "above": "above", "behind": "behind", "in front of": "in front of",
                "next to": "next to", "under": "under"},
        "items": {"ball": "The ball", "bird": "The bird", "cat": "The cat", "dog": "The dog", "teddy": "The teddy"},
        "sent": "{item} is {blank} the box.", "blank": 120, "letters": "abcd",
        "t18": "Write the ordinal number for each duck.", "t18_sub": "The duck nearest the pond is {first}.",
        "pond": "pond",
    },
    "ru": {
        "title": "ПОТРЕНИРУЕМСЯ!", "badge": "Уровень {level} · №{seed}", "name": "Имя:", "date": "Дата:",
        "what": {"fish": "рыбок", "apple": "яблоки", "star": "звёздочки", "flower": "цветы", "ball": "мячи", "heart": "сердечки"},
        "t1": "Посчитай {what}. Запиши число в окошко.",
        "t2": "Сначала прикинь на глаз, потом посчитай {what}.", "estimate": "Примерно:", "counted": "Точно:",
        "t3_odd": "Обведи все нечётные числа.", "t3_even": "Обведи все чётные числа.",
        "t4": "Впиши пропущенные числа на числовом луче.",
        "t5": "Поставь знак &gt;, &lt; или =.",
        "t6": "Запиши числа словами.",
        "t7": "Назови объёмные фигуры. Посчитай грани и рёбра.",
        "th3": ("Фигура", "Название", "Грани", "Рёбра"), "bank": "Слова",
        "shapes3d": {"cube": "куб", "cuboid": "брусок", "cone": "конус", "cylinder": "цилиндр",
                     "sphere": "шар", "pyramid": "пирамида", "prism": "призма"},
        "t8": "Найди и посчитай плоские фигуры на картинке.",
        "th2": ("Фигура", "Сколько?"), "shapes2d": ("Круги", "Треугольники", "Квадраты", "Прямоугольники"),
        "t9": _sides_ru,
        "t10": "Закрась {frac} каждой фигуры.",
        "frac": {"1/2": "половину (½)", "1/4": "четверть (¼)", "1/3": "треть (⅓)", "3/4": "три четверти (¾)"},
        "t11": "Отметь (✓) фигуры, разделённые на {n} равные части.",
        "t12": "Сравни.", "pencil_short": "Обведи самый короткий карандаш.", "pencil_long": "Обведи самый длинный карандаш.",
        "tower_tall": "Обведи самую высокую башню.", "tower_low": "Обведи самую низкую башню.",
        "t13": "Состав числа {n}: найди все пары.",
        "t14": "Считай по {s}. Впиши пропущенные числа.",
        "t15": "Реши примеры.",
        "t16": "Заполни каждую стену.", "t16_sub": "Каждый кирпичик равен сумме двух кирпичиков под ним.",
        "t17": "Посмотри на картинку и закончи предложения.",
        "pos": {"in": "в коробке", "on": "на коробке", "above": "над коробкой", "behind": "за коробкой",
                "in front of": "перед коробкой", "next to": "рядом с коробкой", "under": "под коробкой"},
        "items": {"ball": "Мяч", "bird": "Птица", "cat": "Кошка", "dog": "Собака", "teddy": "Мишка"},
        "sent": "{item} {blank}.", "blank": 190, "letters": "абвг",
        "t18": "Напиши порядковый номер каждой утки.", "t18_sub": "Ближе всех к пруду — {first} утка.",
        "pond": "пруд",
    },
    "uk": {
        "title": "ПОТРЕНУЙМОСЯ!", "badge": "Рівень {level} · №{seed}", "name": "Ім’я:", "date": "Дата:",
        "what": {"fish": "рибок", "apple": "яблука", "star": "зірочки", "flower": "квіти", "ball": "м’ячі", "heart": "сердечка"},
        "t1": "Порахуй {what}. Запиши число в клітинку.",
        "t2": "Спочатку прикинь на око, потім порахуй {what}.", "estimate": "Приблизно:", "counted": "Точно:",
        "t3_odd": "Обведи всі непарні числа.", "t3_even": "Обведи всі парні числа.",
        "t4": "Впиши пропущені числа на числовому промені.",
        "t5": "Постав знак &gt;, &lt; або =.",
        "t6": "Запиши числа словами.",
        "t7": "Назви об’ємні фігури. Порахуй грані та ребра.",
        "th3": ("Фігура", "Назва", "Грані", "Ребра"), "bank": "Слова",
        "shapes3d": {"cube": "куб", "cuboid": "брусок", "cone": "конус", "cylinder": "циліндр",
                     "sphere": "куля", "pyramid": "піраміда", "prism": "призма"},
        "t8": "Знайди й порахуй плоскі фігури на малюнку.",
        "th2": ("Фігура", "Скільки?"), "shapes2d": ("Кола", "Трикутники", "Квадрати", "Прямокутники"),
        "t9": _sides_uk,
        "t10": "Розфарбуй {frac} кожної фігури.",
        "frac": {"1/2": "половину (½)", "1/4": "чверть (¼)", "1/3": "третину (⅓)", "3/4": "три чверті (¾)"},
        "t11": "Познач (✓) фігури, поділені на {n} рівні частини.",
        "t12": "Порівняй.", "pencil_short": "Обведи найкоротший олівець.", "pencil_long": "Обведи найдовший олівець.",
        "tower_tall": "Обведи найвищу вежу.", "tower_low": "Обведи найнижчу вежу.",
        "t13": "Склад числа {n}: знайди всі пари.",
        "t14": "Лічи по {s}. Впиши пропущені числа.",
        "t15": "Розв’яжи приклади.",
        "t16": "Заповни кожну стіну.", "t16_sub": "Кожна цеглинка дорівнює сумі двох цеглинок під нею.",
        "t17": "Подивись на малюнок і закінчи речення.",
        "pos": {"in": "у коробці", "on": "на коробці", "above": "над коробкою", "behind": "за коробкою",
                "in front of": "перед коробкою", "next to": "біля коробки", "under": "під коробкою"},
        "items": {"ball": "М’яч", "bird": "Пташка", "cat": "Кішка", "dog": "Собака", "teddy": "Ведмедик"},
        "sent": "{item} {blank}.", "blank": 190, "letters": "абвг",
        "t18": "Напиши порядковий номер кожної качки.", "t18_sub": "Найближче до ставка — {first} качка.",
        "pond": "ставок",
    },
    "el": {
        "title": "ΑΣ ΕΞΑΣΚΗΘΟΥΜΕ!", "badge": "Επίπεδο {level} · αρ. {seed}", "name": "Όνομα:", "date": "Ημερομηνία:",
        "what": {"fish": "τα ψάρια", "apple": "τα μήλα", "star": "τα αστέρια", "flower": "τα λουλούδια",
                 "ball": "τις μπάλες", "heart": "τις καρδιές"},
        "t1": "Μέτρησε {what}. Γράψε τον αριθμό στο κουτάκι.",
        "t2": "Πρώτα υπολόγισε με το μάτι. Μετά μέτρησε {what}.", "estimate": "Περίπου:", "counted": "Ακριβώς:",
        "t3_odd": "Κύκλωσε όλους τους μονούς αριθμούς.", "t3_even": "Κύκλωσε όλους τους ζυγούς αριθμούς.",
        "t4": "Συμπλήρωσε τους αριθμούς που λείπουν.",
        "t5": "Βάλε &gt;, &lt; ή = για να συγκρίνεις τους αριθμούς.",
        "t6": "Γράψε τους αριθμούς με λέξεις.",
        "t7": "Ονόμασε τα στερεά. Μετά μέτρησε τις έδρες και τις ακμές.",
        "th3": ("Στερεό", "Όνομα", "Έδρες", "Ακμές"), "bank": "Λέξεις",
        "shapes3d": {"cube": "κύβος", "cuboid": "παραλληλε" + SHY + "πίπεδο", "cone": "κώνος", "cylinder": "κύλινδρος",
                     "sphere": "σφαίρα", "pyramid": "πυραμίδα", "prism": "πρίσμα"},
        "t8": "Βρες και μέτρησε τα επίπεδα σχήματα στην εικόνα.",
        "th2": ("Σχήμα", "Πόσα;"), "shapes2d": ("Κύκλοι", "Τρίγωνα", "Τετράγωνα", "Ορθογώνια"),
        "t9": "Κύκλωσε το σχήμα που έχει {n} πλευρές.",
        "t10": "Χρωμάτισε {frac} κάθε σχήματος.",
        "frac": {"1/2": "το μισό (½)", "1/4": "το ένα τέταρτο (¼)", "1/3": "το ένα τρίτο (⅓)", "3/4": "τα τρία τέταρτα (¾)"},
        "t11": "Βάλε (✓) στα σχήματα που είναι χωρισμένα σε {n} ίσα μέρη.",
        "t12": "Σύγκρινε.", "pencil_short": "Κύκλωσε το πιο κοντό μολύβι.", "pencil_long": "Κύκλωσε το πιο μακρύ μολύβι.",
        "tower_tall": "Κύκλωσε τον πιο ψηλό πύργο.", "tower_low": "Κύκλωσε τον πιο χαμηλό πύργο.",
        "t13": "Βρες όλους τους τρόπους να φτιάξεις το {n}.",
        "t14": "Μέτρα ανά {s}. Συμπλήρωσε τους αριθμούς που λείπουν.",
        "t15": "Συμπλήρωσε τις πράξεις.",
        "t16": "Συμπλήρωσε κάθε τοίχο.", "t16_sub": "Κάθε τούβλο είναι το άθροισμα των δύο τούβλων από κάτω του.",
        "t17": "Κοίτα την εικόνα και συμπλήρωσε τις προτάσεις.",
        "pos": {"in": "μέσα στο", "on": "πάνω στο", "above": "πάνω από το", "behind": "πίσω από το",
                "in front of": "μπροστά από το", "next to": "δίπλα στο", "under": "κάτω από το"},
        "items": {"ball": "Η μπάλα", "bird": "Το πουλί", "cat": "Η γάτα", "dog": "Ο σκύλος", "teddy": "Το αρκουδάκι"},
        "sent": "{item} είναι {blank} κουτί.", "blank": 120, "letters": "αβγδ",
        "t18": "Γράψε τον τακτικό αριθμό για κάθε πάπια.",
        "t18_sub": "Η πάπια που είναι πιο κοντά στη λίμνη είναι η {first}.",
        "pond": "λίμνη",
    },
    "de": {
        "title": "LASS UNS ÜBEN!", "badge": "Stufe {level} · Nr. {seed}", "name": "Name:", "date": "Datum:",
        "what": {"fish": "Fische", "apple": "Äpfel", "star": "Sterne", "flower": "Blumen", "ball": "Bälle", "heart": "Herzen"},
        "t1": "Zähle die {what}. Schreibe die Zahl in das Kästchen.",
        "t2": "Schätze zuerst. Dann zähle die {what}.", "estimate": "Geschätzt:", "counted": "Gezählt:",
        "t3_odd": "Kreise alle ungeraden Zahlen ein.", "t3_even": "Kreise alle geraden Zahlen ein.",
        "t4": "Ergänze die fehlenden Zahlen am Zahlenstrahl.",
        "t5": "Setze &gt;, &lt; oder = ein.",
        "t6": "Schreibe die Zahlen in Worten.",
        "t7": "Benenne die Körper. Zähle dann die Flächen und Kanten.",
        "th3": ("Körper", "Name", "Flächen", "Kanten"), "bank": "Wörter",
        "shapes3d": {"cube": "Würfel", "cuboid": "Quader", "cone": "Kegel", "cylinder": "Zylinder",
                     "sphere": "Kugel", "pyramid": "Pyramide", "prism": "Prisma"},
        "t8": "Benenne und zähle die Formen im Bild.",
        "th2": ("Form", "Wie viele?"), "shapes2d": ("Kreise", "Dreiecke", "Quadrate", "Rechtecke"),
        "t9": "Kreise die Form mit {n} Seiten ein.",
        "t10": "Male {frac} jeder Form an.",
        "frac": {"1/2": "die Hälfte (½)", "1/4": "ein Viertel (¼)", "1/3": "ein Drittel (⅓)", "3/4": "drei Viertel (¾)"},
        "t11": "Kreuze (✓) die Formen an, die in {n} gleiche Teile geteilt sind.",
        "t12": "Vergleiche.", "pencil_short": "Kreise den kürzesten Stift ein.", "pencil_long": "Kreise den längsten Stift ein.",
        "tower_tall": "Kreise den höchsten Turm ein.", "tower_low": "Kreise den niedrigsten Turm ein.",
        "t13": "Finde alle Zerlegungen der Zahl {n}.",
        "t14": "Zähle in {s}er-Schritten. Ergänze die fehlenden Zahlen.",
        "t15": "Löse die Aufgaben.",
        "t16": "Vervollständige jede Zahlenmauer.", "t16_sub": "Jeder Stein ist die Summe der beiden Steine darunter.",
        "t17": "Schau dir das Bild an und ergänze die Sätze mit den Lagewörtern.",
        "pos": {"in": "in", "on": "auf", "above": "über", "behind": "hinter", "in front of": "vor",
                "next to": "neben", "under": "unter"},
        "items": {"ball": "Der Ball", "bird": "Der Vogel", "cat": "Die Katze", "dog": "Der Hund", "teddy": "Der Teddy"},
        "sent": "{item} ist {blank} der Kiste.", "blank": 100, "letters": "abcd",
        "t18": "Schreibe die Ordnungszahl für jede Ente.", "t18_sub": "Die Ente, die dem Teich am nächsten ist, ist die {first}",
        "pond": "Teich",
    },
    "fr": {
        "title": "ON S’ENTRAÎNE !", "badge": "Niveau {level} · n° {seed}", "name": "Prénom :", "date": "Date :",
        "what": {"fish": "poissons", "apple": "pommes", "star": "étoiles", "flower": "fleurs", "ball": "ballons", "heart": "cœurs"},
        "t1": "Compte les {what}. Écris le nombre dans la case.",
        "t2": "Estime d’abord. Puis compte les {what}.", "estimate": "J’estime :", "counted": "Je compte :",
        "t3_odd": "Entoure tous les nombres impairs.", "t3_even": "Entoure tous les nombres pairs.",
        "t4": "Complète les nombres manquants sur la droite numérique.",
        "t5": "Écris &gt;, &lt; ou = pour comparer les nombres.",
        "t6": "Écris les nombres en lettres.",
        "t7": "Nomme les solides. Puis compte les faces et les arêtes.",
        "th3": ("Solide", "Nom", "Faces", "Arêtes"), "bank": "Mots",
        "shapes3d": {"cube": "cube", "cuboid": "pavé", "cone": "cône", "cylinder": "cylindre",
                     "sphere": "boule", "pyramid": "pyramide", "prism": "prisme"},
        "t8": "Nomme et compte les figures planes de l’image.",
        "th2": ("Figure", "Combien ?"), "shapes2d": ("Cercles", "Triangles", "Carrés", "Rectangles"),
        "t9": "Entoure la figure qui a {n} côtés.",
        "t10": "Colorie {frac} de chaque figure.",
        "frac": {"1/2": "la moitié (½)", "1/4": "un quart (¼)", "1/3": "un tiers (⅓)", "3/4": "trois quarts (¾)"},
        "t11": "Coche (✓) les figures partagées en {n} parties égales.",
        "t12": "Compare.", "pencil_short": "Entoure le crayon le plus court.", "pencil_long": "Entoure le crayon le plus long.",
        "tower_tall": "Entoure la tour la plus haute.", "tower_low": "Entoure la tour la plus basse.",
        "t13": "Trouve toutes les décompositions de {n}.",
        "t14": "Compte de {s} en {s}. Complète les nombres manquants.",
        "t15": "Complète les calculs.",
        "t16": "Complète chaque mur.", "t16_sub": "Chaque brique est la somme des deux briques en dessous.",
        "t17": "Regarde l’image et complète les phrases avec les mots de position.",
        "pos": {"in": "dans", "on": "sur", "above": "au-dessus de", "behind": "derrière", "in front of": "devant",
                "next to": "à côté de", "under": "sous"},
        "items": {"ball": "Le ballon", "bird": "L’oiseau", "cat": "Le chat", "dog": "Le chien", "teddy": "Le nounours"},
        "sent": "{item} est {blank} la boîte.", "blank": 120, "letters": "abcd",
        "t18": "Écris le nombre ordinal de chaque canard.", "t18_sub": "Le canard le plus près de la mare est le {first}.",
        "pond": "mare",
    },
    "es": {
        "title": "¡A PRACTICAR!", "badge": "Nivel {level} · n.º {seed}", "name": "Nombre:", "date": "Fecha:",
        "what": {"fish": "los peces", "apple": "las manzanas", "star": "las estrellas", "flower": "las flores",
                 "ball": "las pelotas", "heart": "los corazones"},
        "t1": "Cuenta {what}. Escribe el número en la casilla.",
        "t2": "Primero estima. Luego cuenta {what}.", "estimate": "Estimo:", "counted": "Cuento:",
        "t3_odd": "Rodea todos los números impares.", "t3_even": "Rodea todos los números pares.",
        "t4": "Completa los números que faltan en la recta numérica.",
        "t5": "Escribe &gt;, &lt; o = para comparar los números.",
        "t6": "Escribe los números con letras.",
        "t7": "Nombra los cuerpos. Luego cuenta sus caras y aristas.",
        "th3": ("Cuerpo", "Nombre", "Caras", "Aristas"), "bank": "Palabras",
        "shapes3d": {"cube": "cubo", "cuboid": "ortoedro", "cone": "cono", "cylinder": "cilindro",
                     "sphere": "esfera", "pyramid": "pirámide", "prism": "prisma"},
        "t8": "Nombra y cuenta las figuras planas del dibujo.",
        "th2": ("Figura", "¿Cuántas?"), "shapes2d": ("Círculos", "Triángulos", "Cuadrados", "Rectángulos"),
        "t9": "Rodea la figura que tiene {n} lados.",
        "t10": "Colorea {frac} de cada figura.",
        "frac": {"1/2": "la mitad (½)", "1/4": "un cuarto (¼)", "1/3": "un tercio (⅓)", "3/4": "tres cuartos (¾)"},
        "t11": "Marca (✓) las figuras divididas en {n} partes iguales.",
        "t12": "Compara.", "pencil_short": "Rodea el lápiz más corto.", "pencil_long": "Rodea el lápiz más largo.",
        "tower_tall": "Rodea la torre más alta.", "tower_low": "Rodea la torre más baja.",
        "t13": "Encuentra todas las formas de descomponer el {n}.",
        "t14": "Cuenta de {s} en {s}. Completa los números que faltan.",
        "t15": "Completa las operaciones.",
        "t16": "Completa cada muro.", "t16_sub": "Cada ladrillo es la suma de los dos ladrillos de abajo.",
        "t17": "Mira el dibujo y completa las frases con las palabras de posición.",
        "pos": {"in": "dentro de", "on": "sobre", "above": "por encima de", "behind": "detrás de",
                "in front of": "delante de", "next to": "al lado de", "under": "debajo de"},
        "items": {"ball": "La pelota", "bird": "El pájaro", "cat": "El gato", "dog": "El perro", "teddy": "El osito"},
        "sent": "{item} está {blank} la caja.", "blank": 120, "letters": "abcd",
        "t18": "Escribe el número ordinal de cada pato.", "t18_sub": "El pato más cercano al estanque es el {first}.",
        "pond": "estanque",
    },
}

# ---------------------------------------------------------------- answer page texts (for parents)
A = {
    "en": {
        "answers": "Answers", "sub": "Worksheet No. {seed}, level {level} ({lname}). For parents — no need to print this page.",
        "levels": {1: "easy", 2: "medium", 3: "hard"},
        "what": {"fish": "Fish", "apple": "Apples", "star": "Stars", "flower": "Flowers", "ball": "Balls", "heart": "Hearts"},
        "odd": "Odd", "even": "Even", "step": "step {s}",
        "faces": {"cube": "6 faces, 12 edges", "cuboid": "6 faces, 12 edges", "cone": "2 faces (1 flat, 1 curved), 1 edge",
                  "cylinder": "3 faces (2 flat, 1 curved), 2 edges", "sphere": "1 curved face, 0 edges",
                  "pyramid": "5 faces, 8 edges", "prism": "5 faces, 9 edges"},
        "extra": "extra word: {w}",
        "shapes2d": ("Circles", "Triangles", "Squares", "Rectangles"),
        "parts": {"sun": "sun", "house": "house", "chimney": "chimney", "roof": "roof", "round_window": "round window",
                  "window": "window", "door": "door", "trunk": "tree trunk", "fir": "fir tree", "crown": "tree top"},
        "none": "none",
        "poly": {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon"},
        "nth": ("first", "second", "third", "fourth"), "poly_ans": "{name} ({nth} shape)",
        "shade": "In each shape, shade {part}",
        "shade_part": {"1/2": "1 of 2 equal parts", "1/4": "1 of 4 equal parts", "1/3": "1 of 3 equal parts",
                       "3/4": "3 of 4 equal parts"},
        "eq_names": ("square", "circle", "first rectangle", "second rectangle"), "not_equal": "parts are not equal",
        "pencil_short": "Shortest pencil", "pencil_long": "Longest pencil",
        "tower_tall": "tallest tower", "tower_low": "shortest tower",
        "pencil_pos": ("1st (top)", "2nd", "3rd", "4th"),
        "tower_pos": ("1st from the left", "2nd from the left", "3rd from the left", "4th from the left"),
        "cubes": "{n} cubes",
        "column": "Column {i}", "wall": "Wall {i}", "top_down": "(top to bottom)", "left_right": "Left to right",
    },
    "ru": {
        "answers": "Ответы", "sub": "Лист №{seed}, уровень {level} ({lname}). Для родителей — эту страницу печатать не обязательно.",
        "levels": {1: "лёгкий", 2: "средний", 3: "сложный"},
        "what": {"fish": "Рыбки", "apple": "Яблоки", "star": "Звёздочки", "flower": "Цветы", "ball": "Мячи", "heart": "Сердечки"},
        "odd": "Нечётные", "even": "Чётные", "step": "шаг {s}",
        "faces": {"cube": "6 граней, 12 рёбер", "cuboid": "6 граней, 12 рёбер", "cone": "2 грани (1 плоская + 1 кривая), 1 ребро",
                  "cylinder": "3 грани (2 плоские + 1 кривая), 2 ребра", "sphere": "1 кривая грань, 0 рёбер",
                  "pyramid": "5 граней, 8 рёбер", "prism": "5 граней, 9 рёбер"},
        "extra": "лишнее слово: {w}",
        "shapes2d": ("Круги", "Треугольники", "Квадраты", "Прямоугольники"),
        "parts": {"sun": "солнце", "house": "дом", "chimney": "труба", "roof": "крыша", "round_window": "круглое окно",
                  "window": "окно", "door": "дверь", "trunk": "ствол", "fir": "ёлка", "crown": "крона дерева"},
        "none": "нет",
        "poly": {3: "треугольник", 4: "квадрат", 5: "пятиугольник", 6: "шестиугольник", 7: "семиугольник", 8: "восьмиугольник"},
        "nth": ("первая", "вторая", "третья", "четвёртая"), "poly_ans": "{name} ({nth} фигура)",
        "shade": "В каждой фигуре закрасить {part}",
        "shade_part": {"1/2": "1 часть из 2", "1/4": "1 часть из 4", "1/3": "1 часть из 3", "3/4": "3 части из 4"},
        "eq_names": ("квадрат", "круг", "первый прямоугольник", "второй прямоугольник"), "not_equal": "части не равные",
        "pencil_short": "Самый короткий карандаш", "pencil_long": "Самый длинный карандаш",
        "tower_tall": "самая высокая башня", "tower_low": "самая низкая башня",
        "pencil_pos": ("первый (верхний)", "второй", "третий", "четвёртый"),
        "tower_pos": ("первая слева", "вторая слева", "третья слева", "четвёртая слева"),
        "cubes": "кубиков: {n}",
        "column": "{i}-й столбец", "wall": "{i}-я стена", "top_down": "(сверху вниз)", "left_right": "Слева направо",
    },
    "uk": {
        "answers": "Відповіді", "sub": "Аркуш №{seed}, рівень {level} ({lname}). Для батьків — цю сторінку друкувати не обов’язково.",
        "levels": {1: "легкий", 2: "середній", 3: "складний"},
        "what": {"fish": "Рибки", "apple": "Яблука", "star": "Зірочки", "flower": "Квіти", "ball": "М’ячі", "heart": "Сердечка"},
        "odd": "Непарні", "even": "Парні", "step": "крок {s}",
        "faces": {"cube": "6 граней, 12 ребер", "cuboid": "6 граней, 12 ребер", "cone": "2 грані (1 плоска + 1 крива), 1 ребро",
                  "cylinder": "3 грані (2 плоскі + 1 крива), 2 ребра", "sphere": "1 крива грань, 0 ребер",
                  "pyramid": "5 граней, 8 ребер", "prism": "5 граней, 9 ребер"},
        "extra": "зайве слово: {w}",
        "shapes2d": ("Кола", "Трикутники", "Квадрати", "Прямокутники"),
        "parts": {"sun": "сонце", "house": "будинок", "chimney": "димар", "roof": "дах", "round_window": "кругле вікно",
                  "window": "вікно", "door": "двері", "trunk": "стовбур", "fir": "ялинка", "crown": "крона дерева"},
        "none": "немає",
        "poly": {3: "трикутник", 4: "квадрат", 5: "п’ятикутник", 6: "шестикутник", 7: "семикутник", 8: "восьмикутник"},
        "nth": ("перша", "друга", "третя", "четверта"), "poly_ans": "{name} ({nth} фігура)",
        "shade": "У кожній фігурі розфарбувати {part}",
        "shade_part": {"1/2": "1 частину з 2", "1/4": "1 частину з 4", "1/3": "1 частину з 3", "3/4": "3 частини з 4"},
        "eq_names": ("квадрат", "коло", "перший прямокутник", "другий прямокутник"), "not_equal": "частини не рівні",
        "pencil_short": "Найкоротший олівець", "pencil_long": "Найдовший олівець",
        "tower_tall": "найвища вежа", "tower_low": "найнижча вежа",
        "pencil_pos": ("перший (верхній)", "другий", "третій", "четвертий"),
        "tower_pos": ("перша зліва", "друга зліва", "третя зліва", "четверта зліва"),
        "cubes": "кубиків: {n}",
        "column": "{i}-й стовпчик", "wall": "{i}-а стіна", "top_down": "(згори донизу)", "left_right": "Зліва направо",
    },
    "el": {
        "answers": "Απαντήσεις",
        "sub": "Φύλλο αρ. {seed}, επίπεδο {level} ({lname}). Για τους γονείς — δεν χρειάζεται να τυπώσετε αυτή τη σελίδα.",
        "levels": {1: "εύκολο", 2: "μέτριο", 3: "δύσκολο"},
        "what": {"fish": "Ψάρια", "apple": "Μήλα", "star": "Αστέρια", "flower": "Λουλούδια", "ball": "Μπάλες", "heart": "Καρδιές"},
        "odd": "Μονοί", "even": "Ζυγοί", "step": "βήμα {s}",
        "faces": {"cube": "6 έδρες, 12 ακμές", "cuboid": "6 έδρες, 12 ακμές", "cone": "2 έδρες (1 επίπεδη + 1 καμπύλη), 1 ακμή",
                  "cylinder": "3 έδρες (2 επίπεδες + 1 καμπύλη), 2 ακμές", "sphere": "1 καμπύλη έδρα, 0 ακμές",
                  "pyramid": "5 έδρες, 8 ακμές", "prism": "5 έδρες, 9 ακμές"},
        "extra": "περιττή λέξη: {w}",
        "shapes2d": ("Κύκλοι", "Τρίγωνα", "Τετράγωνα", "Ορθογώνια"),
        "parts": {"sun": "ήλιος", "house": "σπίτι", "chimney": "καμινάδα", "roof": "στέγη", "round_window": "στρογγυλό παράθυρο",
                  "window": "παράθυρο", "door": "πόρτα", "trunk": "κορμός", "fir": "έλατο", "crown": "φύλλωμα δέντρου"},
        "none": "κανένα",
        "poly": {3: "τρίγωνο", 4: "τετράγωνο", 5: "πεντάγωνο", 6: "εξάγωνο", 7: "επτάγωνο", 8: "οκτάγωνο"},
        "nth": ("πρώτο", "δεύτερο", "τρίτο", "τέταρτο"), "poly_ans": "{name} ({nth} σχήμα)",
        "shade": "Σε κάθε σχήμα χρωματίζουμε {part}",
        "shade_part": {"1/2": "1 από 2 ίσα μέρη", "1/4": "1 από 4 ίσα μέρη", "1/3": "1 από 3 ίσα μέρη", "3/4": "3 από 4 ίσα μέρη"},
        "eq_names": ("τετράγωνο", "κύκλος", "πρώτο ορθογώνιο", "δεύτερο ορθογώνιο"), "not_equal": "τα μέρη δεν είναι ίσα",
        "pencil_short": "Το πιο κοντό μολύβι", "pencil_long": "Το πιο μακρύ μολύβι",
        "tower_tall": "ο πιο ψηλός πύργος", "tower_low": "ο πιο χαμηλός πύργος",
        "pencil_pos": ("1ο (πάνω)", "2ο", "3ο", "4ο"),
        "tower_pos": ("1ος από αριστερά", "2ος από αριστερά", "3ος από αριστερά", "4ος από αριστερά"),
        "cubes": "{n} κύβοι",
        "column": "Στήλη {i}", "wall": "Τοίχος {i}", "top_down": "(από πάνω προς τα κάτω)",
        "left_right": "Από αριστερά προς τα δεξιά",
    },
    "de": {
        "answers": "Lösungen", "sub": "Arbeitsblatt Nr. {seed}, Stufe {level} ({lname}). Für Eltern — diese Seite muss nicht gedruckt werden.",
        "levels": {1: "leicht", 2: "mittel", 3: "schwer"},
        "what": {"fish": "Fische", "apple": "Äpfel", "star": "Sterne", "flower": "Blumen", "ball": "Bälle", "heart": "Herzen"},
        "odd": "Ungerade", "even": "Gerade", "step": "Schritt {s}",
        "faces": {"cube": "6 Flächen, 12 Kanten", "cuboid": "6 Flächen, 12 Kanten", "cone": "2 Flächen (1 ebene, 1 gewölbte), 1 Kante",
                  "cylinder": "3 Flächen (2 ebene, 1 gewölbte), 2 Kanten", "sphere": "1 gewölbte Fläche, 0 Kanten",
                  "pyramid": "5 Flächen, 8 Kanten", "prism": "5 Flächen, 9 Kanten"},
        "extra": "überzähliges Wort: {w}",
        "shapes2d": ("Kreise", "Dreiecke", "Quadrate", "Rechtecke"),
        "parts": {"sun": "Sonne", "house": "Haus", "chimney": "Schornstein", "roof": "Dach", "round_window": "rundes Fenster",
                  "window": "Fenster", "door": "Tür", "trunk": "Baumstamm", "fir": "Tanne", "crown": "Baumkrone"},
        "none": "keine",
        "poly": {3: "Dreieck", 4: "Quadrat", 5: "Fünfeck", 6: "Sechseck", 7: "Siebeneck", 8: "Achteck"},
        "nth": ("erste", "zweite", "dritte", "vierte"), "poly_ans": "{name} ({nth} Form)",
        "shade": "In jeder Form anmalen: {part}",
        "shade_part": {"1/2": "1 von 2 gleichen Teilen", "1/4": "1 von 4 gleichen Teilen", "1/3": "1 von 3 gleichen Teilen",
                       "3/4": "3 von 4 gleichen Teilen"},
        "eq_names": ("Quadrat", "Kreis", "erstes Rechteck", "zweites Rechteck"), "not_equal": "Teile nicht gleich",
        "pencil_short": "Kürzester Stift", "pencil_long": "Längster Stift",
        "tower_tall": "höchster Turm", "tower_low": "niedrigster Turm",
        "pencil_pos": ("1. (oben)", "2.", "3.", "4."),
        "tower_pos": ("1. von links", "2. von links", "3. von links", "4. von links"),
        "cubes": "{n} Würfel",
        "column": "Spalte {i}", "wall": "Mauer {i}", "top_down": "(von oben nach unten)", "left_right": "Von links nach rechts",
    },
    "fr": {
        "answers": "Réponses", "sub": "Fiche n° {seed}, niveau {level} ({lname}). Pour les parents — inutile d’imprimer cette page.",
        "levels": {1: "facile", 2: "moyen", 3: "difficile"},
        "what": {"fish": "Poissons", "apple": "Pommes", "star": "Étoiles", "flower": "Fleurs", "ball": "Ballons", "heart": "Cœurs"},
        "odd": "Impairs", "even": "Pairs", "step": "de {s} en {s}",
        "faces": {"cube": "6 faces, 12 arêtes", "cuboid": "6 faces, 12 arêtes", "cone": "2 faces (1 plane, 1 courbe), 1 arête",
                  "cylinder": "3 faces (2 planes, 1 courbe), 2 arêtes", "sphere": "1 face courbe, 0 arête",
                  "pyramid": "5 faces, 8 arêtes", "prism": "5 faces, 9 arêtes"},
        "extra": "mot en trop : {w}",
        "shapes2d": ("Cercles", "Triangles", "Carrés", "Rectangles"),
        "parts": {"sun": "soleil", "house": "maison", "chimney": "cheminée", "roof": "toit", "round_window": "fenêtre ronde",
                  "window": "fenêtre", "door": "porte", "trunk": "tronc", "fir": "sapin", "crown": "feuillage"},
        "none": "aucun",
        "poly": {3: "triangle", 4: "carré", 5: "pentagone", 6: "hexagone", 7: "heptagone", 8: "octogone"},
        "nth": ("1re", "2e", "3e", "4e"), "poly_ans": "{name} ({nth} figure)",
        "shade": "Dans chaque figure, colorier {part}",
        "shade_part": {"1/2": "1 partie sur 2", "1/4": "1 partie sur 4", "1/3": "1 partie sur 3", "3/4": "3 parties sur 4"},
        "eq_names": ("carré", "cercle", "premier rectangle", "second rectangle"), "not_equal": "parties inégales",
        "pencil_short": "Crayon le plus court", "pencil_long": "Crayon le plus long",
        "tower_tall": "tour la plus haute", "tower_low": "tour la plus basse",
        "pencil_pos": ("1er (en haut)", "2e", "3e", "4e"),
        "tower_pos": ("1re en partant de la gauche", "2e en partant de la gauche", "3e en partant de la gauche",
                      "4e en partant de la gauche"),
        "cubes": "{n} cubes",
        "column": "Colonne {i}", "wall": "Mur {i}", "top_down": "(de haut en bas)", "left_right": "De gauche à droite",
    },
    "es": {
        "answers": "Soluciones", "sub": "Ficha n.º {seed}, nivel {level} ({lname}). Para las familias: no hace falta imprimir esta página.",
        "levels": {1: "fácil", 2: "medio", 3: "difícil"},
        "what": {"fish": "Peces", "apple": "Manzanas", "star": "Estrellas", "flower": "Flores", "ball": "Pelotas", "heart": "Corazones"},
        "odd": "Impares", "even": "Pares", "step": "de {s} en {s}",
        "faces": {"cube": "6 caras, 12 aristas", "cuboid": "6 caras, 12 aristas", "cone": "2 caras (1 plana, 1 curva), 1 arista",
                  "cylinder": "3 caras (2 planas, 1 curva), 2 aristas", "sphere": "1 cara curva, 0 aristas",
                  "pyramid": "5 caras, 8 aristas", "prism": "5 caras, 9 aristas"},
        "extra": "palabra que sobra: {w}",
        "shapes2d": ("Círculos", "Triángulos", "Cuadrados", "Rectángulos"),
        "parts": {"sun": "sol", "house": "casa", "chimney": "chimenea", "roof": "tejado", "round_window": "ventana redonda",
                  "window": "ventana", "door": "puerta", "trunk": "tronco", "fir": "abeto", "crown": "copa del árbol"},
        "none": "ninguno",
        "poly": {3: "triángulo", 4: "cuadrado", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono"},
        "nth": ("primera", "segunda", "tercera", "cuarta"), "poly_ans": "{name} ({nth} figura)",
        "shade": "En cada figura, colorear {part}",
        "shade_part": {"1/2": "1 parte de 2", "1/4": "1 parte de 4", "1/3": "1 parte de 3", "3/4": "3 partes de 4"},
        "eq_names": ("cuadrado", "círculo", "primer rectángulo", "segundo rectángulo"), "not_equal": "partes desiguales",
        "pencil_short": "Lápiz más corto", "pencil_long": "Lápiz más largo",
        "tower_tall": "torre más alta", "tower_low": "torre más baja",
        "pencil_pos": ("1.º (arriba)", "2.º", "3.º", "4.º"),
        "tower_pos": ("1.ª por la izquierda", "2.ª por la izquierda", "3.ª por la izquierda", "4.ª por la izquierda"),
        "cubes": "{n} cubos",
        "column": "Columna {i}", "wall": "Muro {i}", "top_down": "(de arriba abajo)", "left_right": "De izquierda a derecha",
    },
}


def text(entry, **kw):
    """A translation entry is either a format string or a function of the same keyword arguments."""
    return entry(**kw) if callable(entry) else entry.format(**kw)


def check():
    """Every language must have the same keys as English (run: python scripts/i18n.py)."""
    for table, name in ((W, "W"), (A, "A")):
        ref = table["en"]
        for lang in LANGS:
            assert lang in table, f"{name}: no {lang}"
            for k, v in ref.items():
                assert k in table[lang], f"{name}[{lang}] misses {k}"
                if isinstance(v, dict):
                    assert set(v) == set(table[lang][k]), f"{name}[{lang}][{k}] keys differ"
                if isinstance(v, tuple):
                    assert len(v) == len(table[lang][k]), f"{name}[{lang}][{k}] length differs"
    for lang in LANGS:
        for n in range(100):
            assert numwords(lang, n)
    return True


if __name__ == "__main__":
    check()
    for lang in LANGS:
        print(lang, [numwords(lang, n) for n in (0, 1, 7, 17, 21, 71, 80, 81, 99)], ordinal(lang, 1))
