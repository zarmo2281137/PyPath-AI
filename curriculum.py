"""Повний навчальний план від нуля до Junior+ Python / AI Backend розробника (Етапи 0–10)."""

CURRICULUM = [
    {
        "id": "stage-0",
        "number": 0,
        "title": "ЕТАП 0: Комп'ютерна грамотність та середовище розробника",
        "duration": "2–3 тижні",
        "goal": "Перш ніж писати код, треба вільно почуватися в системі.",
        "topics": [
            {
                "id": "s0-terminal",
                "title": "Термінал / Командний рядок",
                "summary": "Навігація по папках (cd, ls/dir), створення та видалення файлів (mkdir, rm, touch), перегляд процесів.",
                "tags": ["CLI", "cd/ls/dir", "mkdir/rm", "процеси"],
                "practice": "Створіть структуру папок для проєкту з терміналу без мишки та перевірте запущені процеси."
            },
            {
                "id": "s0-hardware-os",
                "title": "Як працює комп'ютер і код",
                "summary": "Що таке оперативна пам'ять (RAM), диск, процесор, чим відрізняється інтерпретована мова (Python) від компільованої (C++).",
                "tags": ["RAM", "CPU", "Інтерпретатор", "Компілятор"],
                "practice": "Поясніть своїми словами, що відбувається в RAM при запуску Python-скрипта."
            },
            {
                "id": "s0-venv",
                "title": "Віртуальні оточення (обов'язково)",
                "summary": "Навіщо потрібен venv або uv / poetry, що таке pip, файл requirements.txt або pyproject.toml, і чому не можна ставити всі бібліотеки глобально в систему.",
                "tags": ["venv", "uv", "poetry", "pip", "requirements.txt", "pyproject.toml"],
                "practice": "Створіть ізольоване .venv, встановіть пакет і збережіть залежності у requirements.txt."
            },
            {
                "id": "s0-vscode-debugger",
                "title": "VS Code та Дебагер",
                "summary": "Як ставити брейкпоінти (червоні крапки), запускати код покроково (Step Over / Step Into) і дивитися значення змінних у реальному часі замість print().",
                "tags": ["VS Code", "Breakpoints", "Step Over", "Step Into"],
                "practice": "Пройдіть простий цикл у режимі Debug, інспектуючи змінні на кожній ітерації."
            }
        ]
    },
    {
        "id": "stage-1",
        "number": 1,
        "title": "ЕТАП 1: Синтаксис Python з повного нуля",
        "duration": "Місяці 1–2",
        "goal": "Це база, яку ти маєш писати з закритими очима без підказок ШІ.",
        "topics": [
            {
                "id": "s1-types",
                "title": "Змінні та базові типи",
                "summary": "int (цілі числа), float (дробові, чому 0.1 + 0.2 != 0.3 і навіщо потрібен Decimal для грошей), str (рядки), bool (True/False), None.",
                "tags": ["int", "float", "Decimal", "str", "bool", "None"],
                "practice": "Напишіть калькулятор бюджету з використанням Decimal замість float."
            },
            {
                "id": "s1-operators",
                "title": "Оператори та умови",
                "summary": "Арифметика (//, %, **), логіка (and, or, not), конструкції if / elif / else, тернарний оператор, match / case.",
                "tags": ["// % **", "if/elif/else", "match/case", "тернарний оператор"],
                "practice": "Реалізуйте маршрутизатор команд (start, help, exit) через match / case."
            },
            {
                "id": "s1-loops",
                "title": "Цикли",
                "summary": "for (і функція range), while, керування циклами (break, continue, else після циклу).",
                "tags": ["for", "while", "range", "break/continue"],
                "practice": "Напишіть пошук простого числа з використанням for ... else."
            },
            {
                "id": "s1-lists",
                "title": "Списки (list)",
                "summary": "Індекси, зрізи ([1:5:2]), методи (append, extend, pop, sort), генератори списків ([x*2 for x in nums if x > 0]).",
                "tags": ["list", "slicing", "list comprehension"],
                "practice": "Відфільтруйте та трансформуйте список чисел в один рядок через list comprehension."
            },
            {
                "id": "s1-tuples",
                "title": "Кортежі (tuple)",
                "summary": "Незмінність (immutability), розпакування (a, b = (1, 2)).",
                "tags": ["tuple", "immutability", "unpacking"],
                "practice": "Обміняйте значення двох змінних через розпакування кортежу."
            },
            {
                "id": "s1-dicts",
                "title": "Словники (dict)",
                "summary": "Ключ-значення, методи .get(), .items(), .keys(), .values(), чому пошук за ключем миттєвий (O(1)).",
                "tags": ["dict", "O(1)", ".get()", ".items()"],
                "practice": "Порахуйте частоту кожного слова у тексті за допомогою словника."
            },
            {
                "id": "s1-sets",
                "title": "Множини (set)",
                "summary": "Унікальні елементи, перетин, об'єднання, різниця множин.",
                "tags": ["set", "унікальність", "операції над множинами"],
                "practice": "Знайдіть спільні теги двох користувачів за допомогою перетину множин."
            },
            {
                "id": "s1-strings",
                "title": "Рядки в деталях",
                "summary": "f-рядки (f\"{var:.2f}\"), методи .split(), .join(), .strip(), .replace(), кодування UTF-8.",
                "tags": ["f-strings", "split/join", "UTF-8"],
                "practice": "Очистіть та відформатуйте CSV-рядок у читабельний звіт."
            },
            {
                "id": "s1-functions",
                "title": "Функції",
                "summary": "Оголошення def, аргументи за замовчуванням, позиційні та іменовані аргументи, *args та **kwargs, область видимості змінних (LEGB: Local, Enclosing, Global, Built-in), lambda-функції.",
                "tags": ["def", "*args/**kwargs", "LEGB", "lambda"],
                "practice": "Напишіть функцію логування, яка приймає будь-які *args і **kwargs."
            }
        ]
    },
    {
        "id": "stage-2",
        "number": 2,
        "title": "ЕТАП 2: Просунутий Python та робота з файлами",
        "duration": "Місяць 3",
        "goal": "Перехід від простих скриптів до чистого коду.",
        "topics": [
            {
                "id": "s2-files",
                "title": "Робота з файлами та шляхами",
                "summary": "Контекстний менеджер with open(...) (режими r, w, a, кодування utf-8) та модуль pathlib (сучасна робота зі шляхами замість os.path).",
                "tags": ["with open", "utf-8", "pathlib"],
                "practice": "Зберіть усі .py файли у папці через pathlib.Path.rglob()."
            },
            {
                "id": "s2-formats",
                "title": "Формати даних (JSON, CSV, .env)",
                "summary": "Робота з json (loads, dumps), csv, .env файли (бібліотека python-dotenv).",
                "tags": ["json", "csv", "python-dotenv", ".env"],
                "practice": "Зчитайте конфігурацію з .env та збережіть звіт у JSON з ensure_ascii=False."
            },
            {
                "id": "s2-exceptions",
                "title": "Обробка помилок (Exceptions)",
                "summary": "Конструкція try / except / else / finally, основні типи помилок (ValueError, KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError), raise та власний клас винятку.",
                "tags": ["try/except", "raise", "Custom Exceptions"],
                "practice": "Створіть власний виняток InvalidConfigError та обробіть його коректно."
            },
            {
                "id": "s2-modules",
                "title": "Модулі та пакети",
                "summary": "Як розбивати проєкт на багато файлів, як працює import, навіщо потрібен __init__.py і конструкція if __name__ == \"__main__\":.",
                "tags": ["import", "__init__.py", "__main__"],
                "practice": "Розбийте монолітний скрипт на пакет із кількох модулів."
            },
            {
                "id": "s2-decorators-generators",
                "title": "Декоратори та генератори",
                "summary": "Як працює yield і навіщо потрібні генератори (економія пам'яті на великих даних). Як написати свій декоратор (замір часу виконання або повторний запит при збої).",
                "tags": ["yield", "generators", "decorators", "functools.wraps"],
                "practice": "Напишіть декоратор @retry(attempts=3) та генератор построкового читання великого логу."
            },
            {
                "id": "s2-typing",
                "title": "Типізація (Type Hints)",
                "summary": "Анотації типів у функціях (def get_user(user_id: int) -> dict[str, Any] | None:).",
                "tags": ["Type Hints", "typing", "Any", "Union |"],
                "practice": "Додайте повну типізацію до попередніх модулів проєкту."
            },
            {
                "id": "s2-logging",
                "title": "Логування (logging / structlog)",
                "summary": "Рівні логів (DEBUG, INFO, WARNING, ERROR, CRITICAL), форматери, ротація файлів та структуровані JSON-логи замість print().",
                "tags": ["logging", "structlog", "JSON logs", "RotatingFileHandler"],
                "practice": "Замініть усі print() у скрипті на налаштований logger із рівнями INFO та ERROR."
            },
            {
                "id": "s2-stdlib",
                "title": "Потужні інструменти stdlib (collections, itertools, functools)",
                "summary": "Counter, defaultdict, lru_cache / cache, itertools (chain, islice, batched) — готові швидкі рішення зі стандартної бібліотеки.",
                "tags": ["Counter", "defaultdict", "lru_cache", "itertools"],
                "practice": "Використайте Counter та @lru_cache для оптимізації підрахунків і рекурсії."
            }
        ]
    },
    {
        "id": "stage-3",
        "number": 3,
        "title": "ЕТАП 3: Об'єктно-орієнтоване програмування — ООП",
        "duration": "Місяць 4",
        "goal": "Без ООП неможливо зрозуміти, як влаштовані фреймворки, клієнти API та великі проєкти.",
        "topics": [
            {
                "id": "s3-oop-basics",
                "title": "Основи класів та об'єктів",
                "summary": "Що таке клас (креслення) і екземпляр/об'єкт (будинок), атрибути та методи, параметр self.",
                "tags": ["class", "instance", "self", "атрибути/методи"],
                "practice": "Створіть клас BankAccount з методами поповнення та зняття коштів."
            },
            {
                "id": "s3-dunder",
                "title": "Магічні (dunder) методи",
                "summary": "__init__, __str__, __repr__, __len__, __eq__, __enter__ / __exit__.",
                "tags": ["__init__", "__repr__", "__eq__", "__enter__/__exit__"],
                "practice": "Реалізуйте власний контекстний менеджер через __enter__ та __exit__."
            },
            {
                "id": "s3-pillars",
                "title": "4 стовпи ООП на практиці",
                "summary": "Інкапсуляція (_attr, __attr, @property), Наслідування (super(), перевизначення), Поліморфізм (однаковий інтерфейс), Абстракція (abc.ABC, @abstractmethod).",
                "tags": ["Інкапсуляція", "Наслідування", "Поліморфізм", "Абстракція"],
                "practice": "Спроєктуйте абстрактний клас PaymentProvider і 2 конкретні реалізації."
            },
            {
                "id": "s3-dataclasses-pydantic",
                "title": "Dataclasses та Pydantic",
                "summary": "@dataclass для простих структур даних та BaseModel із Pydantic для суворої валідації даних.",
                "tags": ["@dataclass", "Pydantic", "BaseModel", "валідація"],
                "practice": "Опишіть схему конфігурації через Pydantic BaseModel з валідацією полів."
            }
        ]
    },
    {
        "id": "stage-4",
        "number": 4,
        "title": "ЕТАП 4: Алгоритми, структури даних та Git",
        "duration": "Місяць 5",
        "goal": "Те, що відрізняє інженера від людини, яка просто склеює чужі бібліотеки.",
        "topics": [
            {
                "id": "s4-bigo",
                "title": "Оцінка складності (Big O notation)",
                "summary": "Різниця між O(1), O(log n), O(n), O(n log n) та O(n²). Чому вкладений цикл по 100 000 елементів покладе сервер.",
                "tags": ["Big O", "O(1)", "O(n)", "O(n²)"],
                "practice": "Оптимізуйте пошук дублікатів з O(n²) до O(n) за допомогою set."
            },
            {
                "id": "s4-algos",
                "title": "Базові алгоритми та структури",
                "summary": "Бінарний пошук, сортування, рекурсія, стек (LIFO), черга (FIFO — collections.deque), хеш-таблиці (як під капотом працює dict і set).",
                "tags": ["Binary Search", "Recursion", "LIFO/FIFO", "deque", "Hash Table"],
                "practice": "Реалізуйте бінарний пошук руками без підказок."
            },
            {
                "id": "s4-git-basics",
                "title": "Git та GitHub: базовий цикл і гілки",
                "summary": "Життєвий цикл файлів (git init, status, add, commit, push, pull) та робота з гілками (git branch, checkout, switch, merge).",
                "tags": ["git", "GitHub", "branch", "merge"],
                "practice": "Створіть feature-гілку, зробіть коміти та змерджіть у main."
            },
            {
                "id": "s4-git-pro",
                "title": "Git на профі-рівні: конфлікти, відкат, .gitignore",
                "summary": "Вирішення Merge Conflicts, відкат змін (git reset, revert, stash), правильний .gitignore (ніколи не заливати .env, ключі API, venv, __pycache__).",
                "tags": ["Merge Conflicts", "reset/revert/stash", ".gitignore"],
                "practice": "Зімітуйте конфлікт злиття у двох гілках і вирішіть його чисто."
            }
        ]
    },
    {
        "id": "stage-5",
        "number": 5,
        "title": "ЕТАП 5: Мережа, HTTP та Асинхронність",
        "duration": "Місяць 6",
        "goal": "Python-бекенд і боти — це на 90% спілкування по мережі між різними сервісами.",
        "topics": [
            {
                "id": "s5-internet",
                "title": "Як працює інтернет",
                "summary": "Клієнт-серверна архітектура, IP-адреси, DNS, порти.",
                "tags": ["Client-Server", "IP", "DNS", "Ports"],
                "practice": "Перевірте DNS-записи домену та порти за допомогою утиліт командного рядка."
            },
            {
                "id": "s5-http",
                "title": "Протокол HTTP/HTTPS, REST API та авторизація",
                "summary": "Headers, Body, Query-параметри; методи GET, POST, PUT, PATCH, DELETE; коди 200, 201, 400, 401/403, 404, 429, 500/502; REST API, API-ключі та Bearer-токени (JWT).",
                "tags": ["HTTP/HTTPS", "REST API", "Status Codes", "JWT"],
                "practice": "Протестуйте публічний REST API через curl або Postman/HTTP-клієнт."
            },
            {
                "id": "s5-http-clients",
                "title": "Синхронні та асинхронні запити",
                "summary": "Бібліотеки requests (синхронна) та httpx / aiohttp (асинхронні).",
                "tags": ["requests", "httpx", "aiohttp"],
                "practice": "Напишіть клієнт на httpx.AsyncClient з таймаутами та обробкою статусів."
            },
            {
                "id": "s5-asyncio",
                "title": "Асинхронний Python (asyncio)",
                "summary": "Різниця між Threads, Multiprocessing (обхід GIL) та Event Loop. async def, await, asyncio.gather, asyncio.create_task, asyncio.Semaphore.",
                "tags": ["asyncio", "GIL", "Event Loop", "gather", "Semaphore"],
                "practice": "Виконайте 50 асинхронних HTTP-запитів паралельно з обмеженням через Semaphore(5)."
            },
            {
                "id": "s5-websockets",
                "title": "Real-time: WebSockets та Server-Sent Events (SSE)",
                "summary": "Двосторонній зв'язок у реальному часі (WebSockets) та потокова передача токенів від AI-моделей (SSE / StreamingResponse).",
                "tags": ["WebSockets", "SSE", "Streaming", "Real-time"],
                "practice": "Реалізуйте простий SSE-ендпоінт у FastAPI, який віддає текст по словах із затримкою."
            }
        ]
    },
    {
        "id": "stage-6",
        "number": 6,
        "title": "ЕТАП 6: Бази даних та SQL",
        "duration": "Місяці 7–8 (Літо)",
        "goal": "Будь-який реальний продукт десь зберігає дані користувачів, замовлення або історію повідомлень.",
        "topics": [
            {
                "id": "s6-postgres-theory",
                "title": "Реляційні БД (PostgreSQL)",
                "summary": "Таблиці, рядки, стовпці, типи даних (INTEGER, VARCHAR, TEXT, BOOLEAN, TIMESTAMP, JSONB), PK/FK, зв'язки (1:1, 1:N, M:N), індекси, транзакції та ACID.",
                "tags": ["PostgreSQL", "PK/FK", "Індекси", "ACID"],
                "practice": "Спроєктуйте схему БД для інтернет-магазину (users, orders, products, order_items)."
            },
            {
                "id": "s6-sql",
                "title": "Мова SQL (писати руками)",
                "summary": "SELECT, FROM, WHERE, ORDER BY, LIMIT; агрегація COUNT, SUM, AVG, GROUP BY, HAVING; INNER JOIN, LEFT JOIN; INSERT, UPDATE, DELETE (з WHERE!).",
                "tags": ["SQL", "JOIN", "GROUP BY", "INSERT/UPDATE/DELETE"],
                "practice": "Напишіть запит із LEFT JOIN та GROUP BY для підрахунку суми замовлень кожного користувача."
            },
            {
                "id": "s6-orm-alembic",
                "title": "ORM та міграції (SQLAlchemy 2.0 + Alembic)",
                "summary": "SQLAlchemy 2.0 (async): опис таблиць як Python-класів та запити через Python. Alembic: міграції структури таблиць без втрати даних.",
                "tags": ["SQLAlchemy 2.0", "AsyncSession", "Alembic"],
                "practice": "Налаштуйте моделі SQLAlchemy 2.0 та згенеруйте першу міграцію Alembic."
            },
            {
                "id": "s6-redis",
                "title": "NoSQL / Кешування (Redis)",
                "summary": "Зберігання «ключ-значення» в RAM, TTL (час життя запису), кешування важких запитів, зберігання станів користувачів.",
                "tags": ["Redis", "TTL", "Caching", "In-memory"],
                "practice": "Додайте кешування відповідей з TTL 60 секунд у Redis."
            },
            {
                "id": "s6-sql-perf",
                "title": "Оптимізація SQL та проблема N+1 в ORM",
                "summary": "Як знайти повільні запити через EXPLAIN ANALYZE та вирішити проблему N+1 запитів у SQLAlchemy через selectinload / joinedload.",
                "tags": ["EXPLAIN ANALYZE", "N+1 Problem", "selectinload", "Query Optimization"],
                "practice": "Порівняйте кількість SQL-запитів до та після додавання selectinload()."
            }
        ]
    },
    {
        "id": "stage-7",
        "number": 7,
        "title": "ЕТАП 7: Backend-фреймворки та Боти",
        "duration": "Місяці 9–10",
        "goal": "Збираємо все разом у повноцінні додатки.",
        "topics": [
            {
                "id": "s7-fastapi",
                "title": "FastAPI (основний робочий інструмент)",
                "summary": "Ендпоінти, Path/Query-параметри, Pydantic v2, Dependency Injection (Depends), HTTPException, CORS, BackgroundTasks, автодокументація Swagger (/docs).",
                "tags": ["FastAPI", "Pydantic v2", "Depends", "Swagger /docs"],
                "practice": "Створіть CRUD REST API з авторизацією, БД та автодокументацією Swagger."
            },
            {
                "id": "s7-aiogram",
                "title": "Telegram-боти (aiogram 3.x)",
                "summary": "Роутери, фільтри, хендлери повідомлень і колбеків (inline-кнопки), FSM (Finite State Machine), Middlewares, різниця між Polling та Webhook.",
                "tags": ["aiogram 3", "FSM", "Middlewares", "Polling/Webhook"],
                "practice": "Розробіть бота з покроковим оформленням заявки через FSM та inline-кнопками."
            },
            {
                "id": "s7-scraping",
                "title": "Парсинг даних (Web Scraping)",
                "summary": "Статичні сайти (httpx + BeautifulSoup4 / selectolax), динамічні сайти з JS (Playwright), робота з проксі, User-Agent та затримками.",
                "tags": ["BeautifulSoup4", "selectolax", "Playwright", "Proxies"],
                "practice": "Напишіть асинхронний парсер новин або цін зі збереженням у БД."
            },
            {
                "id": "s7-auth-security",
                "title": "Автентифікація та безпека API (JWT, RBAC, Rate Limit)",
                "summary": "Хешування паролів (bcrypt / argon2 / PBKDF2), Access & Refresh JWT-токени, ролі доступу (RBAC) та захист від brute-force.",
                "tags": ["JWT", "bcrypt/argon2", "OAuth2", "RBAC", "Rate Limiting"],
                "practice": "Реалізуйте реєстрацію, логін із JWT та захищений ендпоінт лише для ролі admin."
            },
            {
                "id": "s7-queues",
                "title": "Фонові задачі та черги (ARQ / Celery / Taskiq)",
                "summary": "Асинхронна обробка важких задач у окремих воркерах (парсинг, індексація RAG, розсилки) через Redis без блокування API.",
                "tags": ["Celery", "ARQ", "Taskiq", "Workers", "Queues"],
                "practice": "Винесіть довгу генерацію звіту у фонового воркера через Redis."
            }
        ]
    },
    {
        "id": "stage-8",
        "number": 8,
        "title": "ЕТАП 8: Прикладна AI-інженерія",
        "duration": "Місяці 11–13",
        "goal": "Твоя головна конкурентна перевага на ринку.",
        "topics": [
            {
                "id": "s8-llm-api",
                "title": "Робота з LLM API на рівні інженера",
                "summary": "OpenAI SDK / Google GenAI SDK / Anthropic / Groq. Системні промпти, temperature, контекстне вікно, підрахунок токенів і вартості.",
                "tags": ["LLM API", "System Prompt", "Tokens", "Temperature"],
                "practice": "Створіть сервіс-обгортку над LLM API з підрахунком вартості кожного запиту."
            },
            {
                "id": "s8-structured-tools",
                "title": "Structured Outputs та Tool Calling",
                "summary": "Гарантоване отримання JSON за Pydantic-схемою та Function Calling: підключення до LLM твоїх Python-функцій (БД, пошук, API).",
                "tags": ["Structured Outputs", "Tool Calling", "Pydantic"],
                "practice": "Підключіть до LLM інструмент для пошуку товарів у вашій базі даних."
            },
            {
                "id": "s8-rag",
                "title": "RAG (Retrieval-Augmented Generation)",
                "summary": "Векторні ембедінги (Embeddings), нарізка тексту (Chunking), парсинг PDF/DOCX/Excel, векторні БД (pgvector або Qdrant), гібридний пошук та реранкінг (Reranking).",
                "tags": ["RAG", "Embeddings", "Chunking", "pgvector/Qdrant", "Reranking"],
                "practice": "Побудуйте RAG-бота, який відповідає на питання за завантаженими PDF-документами."
            },
            {
                "id": "s8-ai-reliability",
                "title": "Надійність AI-систем",
                "summary": "Фолбеки між провайдерами, таймаути, захист від Prompt Injection, логування запитів і відповідей.",
                "tags": ["Fallbacks", "Prompt Injection", "Observability"],
                "practice": "Реалізуйте автоматичний fallback на резервну модель при таймауті основної."
            },
            {
                "id": "s8-agents-evals",
                "title": "AI-агенти (LangGraph) та оцінка якості (Evals)",
                "summary": "Багатокрокові агенти з пам'яттю та станом (LangGraph), а також автоматичне тестування точності RAG і промптів (LLM-as-a-Judge).",
                "tags": ["AI Agents", "LangGraph", "Evals", "LLM-as-a-Judge"],
                "practice": "Зберіть набір із 15 тестових питань для вашого RAG і оцініть точність відповідей."
            }
        ]
    },
    {
        "id": "stage-9",
        "number": 9,
        "title": "ЕТАП 9: Інфраструктура, Якість коду та Продакшн",
        "duration": "Місяці 14–16",
        "goal": "Те, що перетворює «код школяра» на код комерційного розробника.",
        "topics": [
            {
                "id": "s9-code-quality",
                "title": "Якість коду, лінтери та тестування",
                "summary": "DRY, KISS, базовий SOLID; Ruff і Mypy; Pytest (тести функцій та API, @pytest.fixture, мокінг платних AI API через unittest.mock / pytest-mock).",
                "tags": ["SOLID", "Ruff", "Mypy", "Pytest", "Mocking"],
                "practice": "Покрийте FastAPI-ендпоінти тестами на pytest з моком LLM API."
            },
            {
                "id": "s9-docker",
                "title": "Контейнеризація (Docker & Docker Compose)",
                "summary": "Image vs Container, оптимальний Dockerfile, Docker Compose для запуску всього стеку (FastAPI + PostgreSQL + Redis + Bot) однією командою.",
                "tags": ["Docker", "Dockerfile", "Docker Compose"],
                "practice": "Упакуйте свій проєкт у docker-compose.yml із healthcheck-ами."
            },
            {
                "id": "s9-devops",
                "title": "Сервери, Деплой та CI/CD",
                "summary": "VPS (Ubuntu Linux), SSH-ключі, фаєрвол (ufw), DNS A-записи, Nginx (reverse proxy) + HTTPS через Certbot, базовий CI/CD у GitHub Actions.",
                "tags": ["Linux VPS", "SSH", "Nginx", "Certbot", "GitHub Actions"],
                "practice": "Задеплойте FastAPI-додаток на VPS із доменом, HTTPS та автотестами у GitHub Actions."
            },
            {
                "id": "s9-monitoring",
                "title": "Моніторинг, алерти та Sentry",
                "summary": "Відстеження помилок у продакшені (Sentry), healthcheck-ендпоінти, базові метрики (Prometheus / Grafana) та алерти в Telegram.",
                "tags": ["Sentry", "Prometheus", "Grafana", "Healthcheck", "Alerts"],
                "practice": "Підключіть Sentry SDK до FastAPI або налаштуйте алерт у Telegram при 500-й помилці."
            }
        ]
    },
    {
        "id": "stage-10",
        "number": 10,
        "title": "ЕТАП 10: Вихід на ринок та перша комерція",
        "duration": "Місяці 17–24 (Друга половина 11 класу)",
        "goal": "Фінальна підготовка до роботи на 1-му курсі.",
        "topics": [
            {
                "id": "s10-portfolio",
                "title": "Портфоліо (3–4 сильні проєкти на GitHub)",
                "summary": "1) Асинхронний парсер/агрегатор з PostgreSQL; 2) REST API на FastAPI + SQLAlchemy + Alembic + Redis + Docker + pytest; 3) Комерційний AI-асистент (RAG + Telegram-бот + адмінка); 4) Власний нішевий проєкт.",
                "tags": ["GitHub Portfolio", "README", "Architecture"],
                "practice": "Оформіть 3–4 репозиторії з якісними README, діаграмами та інструкцією запуску."
            },
            {
                "id": "s10-interviews",
                "title": "Тренування співбесід",
                "summary": "70–100 задач Easy та 15–20 Medium на LeetCode / Codewars без ШІ. Усне пояснення: dict, GIL, SQL JOIN, HTTP-запит, Docker, RAG.",
                "tags": ["LeetCode", "Codewars", "System Design", "Теорія"],
                "practice": "Пройдіть імітацію технічної співбесіди, пояснюючи концепції вголос."
            },
            {
                "id": "s10-freelance",
                "title": "Перші замовлення та резюме",
                "summary": "Старт на фрилансі (Freelancehunt, Upwork) та прямі пропозиції малому бізнесу (автоматизація заявок, парсинг, AI-боти). Збір реальних відгуків і цифр для резюме.",
                "tags": ["Freelancehunt", "Upwork", "CV", "Комерційний досвід"],
                "practice": "Складіть резюме з вимірюваними результатами та візьміть перше реальне замовлення."
            }
        ]
    }
]
