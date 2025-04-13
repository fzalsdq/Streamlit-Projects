import streamlit as st
import json
import json 
import streamlit as st
class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory."""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        """Store the current book collection to a JSON file."""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def create_new_book(self, title, author, year, genre, read):
        """Add a new book to the collection."""
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title):
        """Remove a book from the collection using its title."""
        for book in self.book_list:
            if book["title"].lower() == title.lower():
                self.book_list.remove(book)
                self.save_to_file()
                return "Book removed successfully!"
        return "Book not found!"

    def find_books(self, search_type, search_text):
        """Search for books in the collection by title or author name."""
        search_text = search_text.lower()
        found_books = [
            book
            for book in self.book_list
            if search_text in book[search_type].lower()
        ]
        return found_books

    def update_book(self, title, new_title, new_author, new_year, new_genre, read):
        """Modify the details of an existing book."""
        for book in self.book_list:
            if book["title"].lower() == title.lower():
                book["title"] = new_title or book["title"]
                book["author"] = new_author or book["author"]
                book["year"] = new_year or book["year"]
                book["genre"] = new_genre or book["genre"]
                book["read"] = read
                self.save_to_file()
                return "Book updated successfully!"
        return "Book not found!"

    def show_all_books(self):
        """Display all books in the collection with their details."""
        return self.book_list

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        return total_books, completion_rate

# Initialize the book manager
book_manager = BookCollection()

# Streamlit App
def main():
    st.title("Book Collection Manager")

    menu = ["Add a new book", "Remove a book", "Search for books", "Update book details", "View all books", "View reading progress"]
    choice = st.sidebar.selectbox("Choose an action", menu)

    # Add a new book
    if choice == "Add a new book":
        with st.form(key="add_book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.text_input("Publication Year")
            genre = st.text_input("Genre")
            read = st.radio("Have you read this book?", ["Yes", "No"])
            submit_button = st.form_submit_button("Add this Book")

        if submit_button:
            read = read == "Yes"
            book_manager.create_new_book(title, author, year, genre, read)
            st.success("Book added successfully!")

    # Remove a book
    elif choice == "Remove a book":
        book_title = st.text_input("Enter the title of the book to remove")
        remove_button = st.button("Remove this Book")
        
        if remove_button and book_title:
            result = book_manager.delete_book(book_title)
            st.info(result)

    # Search for books
    elif choice == "Search for books":
        search_type = st.radio("Search by", ["Title", "Author"])
        search_text = st.text_input(f"Enter {search_type.lower()} to search")
        
        if search_text:
            found_books = book_manager.find_books(search_type.lower(), search_text)
            if found_books:
                for book in found_books:
                    reading_status = "Read" if book["read"] else "Unread"
                    st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
            else:
                st.write("No matching books found.")

    # Update book details
    elif choice == "Update book details":
        book_title = st.text_input("Enter the title of the book to update")
        
        if book_title:
            book = next((book for book in book_manager.book_list if book["title"].lower() == book_title.lower()), None)
            if book:
                with st.form(key="update_book_form"):
                    new_title = st.text_input(f"New title ({book['title']})", book["title"])
                    new_author = st.text_input(f"New author ({book['author']})", book["author"])
                    new_year = st.text_input(f"New year ({book['year']})", book["year"])
                    new_genre = st.text_input(f"New genre ({book['genre']})", book["genre"])
                    new_read = st.radio(f"Have you read this book? ({'Yes' if book['read'] else 'No'})", ["Yes", "No"])
                    submit_button = st.form_submit_button("Update Book")
                
                if submit_button:
                    new_read = new_read == "Yes"
                    result = book_manager.update_book(book_title, new_title, new_author, new_year, new_genre, new_read)
                    st.info(result)
            else:
                st.write("Book not found.")

    # View all books
    elif choice == "View all books":
        books = book_manager.show_all_books()
        if books:
            for book in books:
                reading_status = "Read" if book["read"] else "Unread"
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
        else:
            st.write("No books in the collection.")

    # View reading progress
    elif choice == "View reading progress":
        total_books, completion_rate = book_manager.show_reading_progress()
        st.write(f"Total books in collection: {total_books}")
        st.write(f"Reading progress: {completion_rate:.2f}%")

if __name__ == "__main__":
    main()
