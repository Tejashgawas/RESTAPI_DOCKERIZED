from app import create_app, db
from app.models.book import Book

app = create_app()

with app.app_context():
    books = [
        ("Atomic Habits", "James Clear"),
        ("Deep Work", "Cal Newport"),
        ("The Subtle Art of Not Giving a F*ck", "Mark Manson"),
        ("Can't Hurt Me", "David Goggins"),
        ("The Alchemist", "Paulo Coelho"),
        ("Sapiens", "Yuval Noah Harari"),
        ("Educated", "Tara Westover"),
        ("Think and Grow Rich", "Napoleon Hill"),
        ("The Power of Now", "Eckhart Tolle"),
        ("12 Rules for Life", "Jordan B. Peterson"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki"),
        ("The Psychology of Money", "Morgan Housel"),
        ("Start With Why", "Simon Sinek"),
        ("Hooked", "Nir Eyal"),
        ("The 5 AM Club", "Robin Sharma"),
    ]

    for title, author in books:
        db.session.add(Book(title=title, author=author))
    db.session.commit()
    print("✅ Seeded 15 books into the database.")
