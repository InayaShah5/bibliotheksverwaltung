import json
import os


FILE_NAME = "library.json"


def load_books():
    """Load books from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Die Bibliotheksdatei konnte nicht gelesen werden.")
        return []


def save_books(books):
    """Save books to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)
    except OSError:
        print("Die Bibliotheksdaten konnten nicht gespeichert werden.")


def get_next_book_id(books):
    """Generate the next available book ID."""
    if not books:
        return 1

    return max(book["id"] for book in books) + 1


def add_book(books):
    """Add a new book to the library."""
    title = input("Titel des Buches: ").strip()
    author = input("Name des Autors: ").strip()

    if not title or not author:
        print("Titel und Autor dürfen nicht leer sein.")
        return

    new_book = {
        "id": get_next_book_id(books),
        "title": title,
        "author": author,
        "borrowed": False
    }

    books.append(new_book)
    save_books(books)

    print(f"Buch wurde erfolgreich hinzugefügt. Buch-ID: {new_book['id']}")


def view_books(books):
    """Display all books."""
    if not books:
        print("Die Bibliothek enthält keine Bücher.")
        return

    print("\n--- Bücher in der Bibliothek ---")

    for book in books:
        status = "Verfügbar" if not book["borrowed"] else "Ausgeliehen"

        print(
            f"ID: {book['id']} | "
            f"{book['title']} von {book['author']} | "
            f"Status: {status}"
        )


def search_book(books):
    """Search for books by title or author."""
    search_term = input(
        "Suchbegriff (Titel oder Autor): "
    ).strip().lower()

    if not search_term:
        print("Bitte geben Sie einen Suchbegriff ein.")
        return

    found_books = [
        book for book in books
        if search_term in book["title"].lower()
        or search_term in book["author"].lower()
    ]

    if not found_books:
        print("Kein passendes Buch gefunden.")
        return

        print(
            f"ID: {book['id']} | "
            f"{book['title']} von {book['author']} | "
            f"Status: {status}"
        )


def borrow_book(books):
    """Borrow an available book."""
    try:
        book_id = int(input("Buch-ID zum Ausleihen: "))
    except ValueError:
        print("Bitte geben Sie eine gültige Buch-ID ein.")
        return

    for book in books:
        if book["id"] == book_id:
            if book["borrowed"]:
                print("Dieses Buch ist bereits ausgeliehen.")
                return

            book["borrowed"] = True
            save_books(books)

            print(f"'{book['title']}' wurde erfolgreich ausgeliehen.")
            return

    print("Kein Buch mit dieser ID gefunden.")


def return_book(books):
    """Return a borrowed book."""
    try:
        book_id = int(input("Buch-ID zum Zurückgeben: "))
    except ValueError:
        print("Bitte geben Sie eine gültige Buch-ID ein.")
        return

    for book in books:
        if book["id"] == book_id:
            if not book["borrowed"]:
                print("Dieses Buch ist nicht ausgeliehen.")
                return

            book["borrowed"] = False
            save_books(books)

            print(f"'{book['title']}' wurde erfolgreich zurückgegeben.")
            return

    print("Kein Buch mit dieser ID gefunden.")


def menu():
    """Display the main menu and run the program."""
    books = load_books()

    while True:
        print("\n========== Bibliotheksverwaltung ==========")
        print("1. Buch hinzufügen")
        print("2. Bücher anzeigen")
        print("3. Buch suchen")
        print("4. Buch ausleihen")
        print("5. Buch zurückgeben")
        print("6. Programm beenden")
        print("============================================")

        choice = input("Ihre Auswahl: ").strip()

        if choice == "1":
            add_book(books)

        elif choice == "2":
            view_books(books)

        elif choice == "3":
            search_book(books)

        elif choice == "4":
            borrow_book(books)

        elif choice == "5":
            return_book(books)

        elif choice == "6":
            print("Vielen Dank. Das Programm wird beendet.")
            break

        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")


if __name__ == "__main__":
    menu()