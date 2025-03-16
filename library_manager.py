import json
import csv

# Load library from a text file (JSON format)
def load_library():
    try:
        with open('library.txt', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"❌ Error loading library: {e}")
        return []

# Save library back to the text file
def save_library(library):
    try:
        with open('library.txt', 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving library: {e}")

# Import books from a CSV file
def import_library_from_csv(library):
    filename = input("Enter CSV filename to import (e.g., library_sample.csv): ").strip()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                library.append({
                    'title': row['title'],
                    'author': row['author'],
                    'publication_year': int(row['publication_year']),
                    'genre': row['genre'],
                    'read_status': row['read_status'].lower() == 'yes',
                    'rating': float(row['rating'])
                })
        print(f"✅ Library imported successfully from {filename}!")
    except Exception as e:
        print(f"❌ Error importing CSV file: {e}")

# Export books to a CSV file
def export_library_to_csv(library):
    filename = input("Enter CSV filename to export (e.g., export_library.csv): ").strip()
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['title', 'author', 'publication_year', 'genre', 'read_status', 'rating']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for book in library:
                writer.writerow({
                    'title': book['title'],
                    'author': book['author'],
                    'publication_year': book['publication_year'],
                    'genre': book['genre'],
                    'read_status': 'yes' if book['read_status'] else 'no',
                    'rating': book.get('rating', 'N/A')
                })
        print(f"✅ Library exported successfully to {filename}!")
    except Exception as e:
        print(f"❌ Error exporting CSV file: {e}")

# Print menu options
def print_menu():
    print("""
Welcome to your Personal Library Manager!
1. Add a book
2. Remove a book
3. Search for a book
4. Display all books
5. Display statistics
6. Import books from CSV
7. Export books to CSV
8. Exit
    """.strip())

# Add a new book
def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    
    while True:
        year_str = input("Enter the publication year: ").strip()
        try:
            year = int(year_str)
            break
        except ValueError:
            print("❌ Invalid year. Please enter a valid integer.")
    
    genre = input("Enter the genre: ").strip()
    
    read_status = None
    while read_status not in ['yes', 'no']:
        read_status = input("Have you read this book? (yes/no): ").strip().lower()
        if read_status not in ['yes', 'no']:
            print("❌ Please enter 'yes' or 'no'.")
    
    while True:
        rating_str = input("Enter book rating (1-5, or leave blank): ").strip()
        if rating_str == "":
            rating = None
            break
        try:
            rating = float(rating_str)
            if 1 <= rating <= 5:
                break
            else:
                print("❌ Please enter a rating between 1 and 5.")
        except ValueError:
            print("❌ Invalid rating. Please enter a number between 1 and 5.")
    
    book = {
        'title': title,
        'author': author,
        'publication_year': year,
        'genre': genre,
        'read_status': (read_status == 'yes'),
        'rating': rating if rating is not None else "N/A"
    }
    library.append(book)
    print("✅ Book added successfully!")

# Remove a book
def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip()
    removed = False
    for i in range(len(library)-1, -1, -1):
        if library[i]['title'].lower() == title.lower():
            del library[i]
            removed = True
    if removed:
        print("✅ Book removed successfully!")
    else:
        print("❌ Book not found in the library.")

# Search books
def search_books(library):
    print("Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice: ").strip()
    
    if choice == '1':
        search_term = input("Enter the title: ").strip()
        matching = [book for book in library if book['title'].lower() == search_term.lower()]
    elif choice == '2':
        search_term = input("Enter the author: ").strip()
        matching = [book for book in library if book['author'].lower() == search_term.lower()]
    else:
        print("❌ Invalid choice.")
        return
    
    if not matching:
        print("❌ No matching books found.")
        return
    
    print("\n📚 Matching Books:")
    for idx, book in enumerate(matching, 1):
        read_status = '✅ Read' if book['read_status'] else '❌ Unread'
        print(f"{idx}. {book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']} - {read_status} - Rating: {book.get('rating', 'N/A')}")

# Display all books
def display_all_books(library):
    if not library:
        print("📖 Your library is empty.")
        return
    print("\n📚 Your Library:")
    for idx, book in enumerate(library, 1):
        read_status = '✅ Read' if book['read_status'] else '❌ Unread'
        print(f"{idx}. {book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']} - {read_status} - Rating: {book.get('rating', 'N/A')}")

# Display library statistics
def display_statistics(library):
    total = len(library)
    print(f"\n📊 Total books: {total}")
    if total == 0:
        return
    read_count = sum(1 for book in library if book['read_status'])
    percentage = (read_count / total) * 100
    print(f"📖 Percentage read: {percentage:.1f}%")

# Main function
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
            display_all_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            import_library_from_csv(library)
        elif choice == '7':
            export_library_to_csv(library)
        elif choice == '8':
            save_library(library)
            print("📂 Library saved. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-8.")

# Run the program
if __name__ == "__main__":
    main()
