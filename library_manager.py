import json
import os
from tabulate import tabulate

LIBRARY_FILE = "library.txt"
BACKUP_FILE = "library_backup.txt"

def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return []
    try:
        with open(LIBRARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading library: {e}")
        return []

def save_library(library):
    try:
        with open(BACKUP_FILE, 'w', encoding='utf-8') as backup_f:
            json.dump(library, backup_f)  # Create a backup before saving
        with open(LIBRARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4)
    except Exception as e:
        print(f"Error saving library: {e}")

def print_menu():
    print("\nWelcome to your Personal Library Manager!")
    print(tabulate([
        ["1", "Add a book"],
        ["2", "Remove a book"],
        ["3", "Search for a book"],
        ["4", "Display all books"],
        ["5", "Sort books"],
        ["6", "Display statistics"],
        ["7", "Export library"],
        ["8", "Import library"],
        ["9", "Exit"]
    ], headers=["Option", "Action"], tablefmt="grid"))

def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    
    while True:
        try:
            year = int(input("Enter the publication year: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a valid integer.")

    genre = input("Enter the genre: ").strip()
    
    read_status = None
    while read_status not in ['yes', 'no']:
        read_status = input("Have you read this book? (yes/no): ").strip().lower()

    while True:
        try:
            rating = float(input("Rate the book (1-5 stars): ").strip())
            if 1 <= rating <= 5:
                break
            else:
                print("Rating must be between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    book = {
        'title': title,
        'author': author,
        'publication_year': year,
        'genre': genre,
        'read_status': (read_status == 'yes'),
        'rating': rating
    }
    library.append(book)
    print("✅ Book added successfully!")

def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip().lower()
    original_len = len(library)
    library[:] = [book for book in library if book['title'].lower() != title]
    
    if len(library) < original_len:
        print("✅ Book removed successfully!")
    else:
        print("❌ Book not found in the library.")

def search_books(library):
    query = input("Enter a title or author to search: ").strip().lower()
    results = [book for book in library if query in book['title'].lower() or query in book['author'].lower()]
    
    if results:
        print("\n🔍 Matching Books:")
        display_books(results)
    else:
        print("❌ No matching books found.")

def display_books(library):
    if not library:
        print("📚 Your library is empty.")
        return

    table = [[book['title'], book['author'], book['publication_year'], book['genre'], 'Read' if book['read_status'] else 'Unread', f"{book['rating']} ⭐"] for book in library]
    print(tabulate(table, headers=["Title", "Author", "Year", "Genre", "Status", "Rating"], tablefmt="fancy_grid"))

def sort_books(library):
    print("\nSort by:")
    print("1. Title (A-Z)")
    print("2. Author (A-Z)")
    print("3. Year (Newest First)")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        library.sort(key=lambda x: x['title'].lower())
    elif choice == '2':
        library.sort(key=lambda x: x['author'].lower())
    elif choice == '3':
        library.sort(key=lambda x: x['publication_year'], reverse=True)
    else:
        print("❌ Invalid choice.")
        return

    print("✅ Books sorted successfully!")
    display_books(library)

def display_statistics(library):
    total_books = len(library)
    if total_books == 0:
        print("📚 No books in the library.")
        return

    read_books = sum(1 for book in library if book['read_status'])
    avg_rating = sum(book['rating'] for book in library) / total_books

    print("\n📊 Library Statistics:")
    print(f"📚 Total Books: {total_books}")
    print(f"📖 Books Read: {read_books} ({(read_books/total_books)*100:.1f}%)")
    print(f"⭐ Average Rating: {avg_rating:.1f}/5")

def export_library(library):
    filename = input("Enter filename to export (e.g., my_library.json): ").strip()
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4)
        print(f"✅ Library exported successfully as {filename}!")
    except Exception as e:
        print(f"❌ Error exporting library: {e}")

def import_library(library):
    filename = input("Enter filename to import (e.g., my_library.json): ").strip()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            imported_books = json.load(f)
            library.extend(imported_books)
        print(f"✅ Library imported successfully from {filename}!")
    except Exception as e:
        print(f"❌ Error importing library: {e}")

def main():
    library = load_library()
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            display_books(library)
        elif choice == '5':
            sort_books(library)
        elif choice == '6':
            display_statistics(library)
        elif choice == '7':
            export_library(library)
        elif choice == '8':
            import_library(library)
        elif choice == '9':
            save_library(library)
            print("📖 Library saved. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-9.")

if __name__ == "__main__":
    main()
