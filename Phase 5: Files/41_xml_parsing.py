import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os


def create_xml() -> ET.Element:
    """Create an XML document programmatically."""
    root = ET.Element("library")

    book1 = ET.SubElement(root, "book")
    book1.set("id", "1")
    book1.set("isbn", "978-0-13-468599-1")

    title1 = ET.SubElement(book1, "title")
    title1.text = "Python Programming"
    author1 = ET.SubElement(book1, "author")
    author1.text = "John Smith"
    year1 = ET.SubElement(book1, "year")
    year1.text = "2023"
    genres1 = ET.SubElement(book1, "genres")
    genre1 = ET.SubElement(genres1, "genre")
    genre1.text = "Programming"
    genre2 = ET.SubElement(genres1, "genre")
    genre2.text = "Computer Science"

    book2 = ET.SubElement(root, "book")
    book2.set("id", "2")
    book2.set("isbn", "978-0-596-51774-8")

    title2 = ET.SubElement(book2, "title")
    title2.text = "Learning Python"
    author2 = ET.SubElement(book2, "author")
    author2.text = "Jane Doe"
    year2 = ET.SubElement(book2, "year")
    year2.text = "2024"

    return root


def write_xml(filepath: str, root: ET.Element) -> None:
    """Write XML to file with pretty formatting."""
    rough_string = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(rough_string)
    pretty_xml = dom.toprettyxml(indent="  ")
    with open(filepath, "w") as f:
        f.write(pretty_xml)


def read_xml(filepath: str) -> ET.Element:
    """Parse XML from file."""
    tree = ET.parse(filepath)
    return tree.getroot()


def parse_xml_manually(root: ET.Element) -> None:
    """Parse XML by traversing elements."""
    print("=== Manual XML Parsing ===")
    for book in root.findall("book"):
        book_id = book.get("id")
        isbn = book.get("isbn")
        title = book.find("title").text
        author = book.find("author").text
        year = book.find("year").text
        print(f"  Book {book_id}: '{title}' by {author} ({year})")
        print(f"    ISBN: {isbn}")

        genres = book.find("genres")
        if genres is not None:
            genre_list = [g.text for g in genres.findall("genre")]
            print(f"    Genres: {', '.join(genre_list)}")


def parse_with_xpath(root: ET.Element) -> None:
    """Use XPath-like queries."""
    print("\n=== XPath Queries ===")
    titles = root.findall(".//title")
    print(f"  All titles: {[t.text for t in titles]}")

    authors = root.findall(".//author")
    print(f"  All authors: {[a.text for a in authors]}")

    programming_books = root.findall(".//book[genres/genre='Programming']")
    print(f"  Programming books: {[b.find('title').text for b in programming_books]}")


def modify_xml(root: ET.Element) -> None:
    """Modify XML document."""
    print("\n=== XML Modification ===")
    for book in root.findall("book"):
        year_text = book.find("year").text
        year = int(year_text)
        if year < 2024:
            book.find("year").text = str(year + 1)
            print(f"  Updated year for '{book.find('title').text}' to {year + 1}")

    # Add a new book
    new_book = ET.SubElement(root, "book")
    new_book.set("id", "3")
    new_book.set("isbn", "978-1-491-95035-3")
    ET.SubElement(new_book, "title").text = "Fluent Python"
    ET.SubElement(new_book, "author").text = "Luciano Ramalho"
    ET.SubElement(new_book, "year").text = "2022"


def main():
    tmpdir = "/tmp/xml_demo"
    os.makedirs(tmpdir, exist_ok=True)

    print("=== Create XML ===")
    root = create_xml()
    path = os.path.join(tmpdir, "library.xml")
    write_xml(path, root)
    print(f"  XML written to {path}")

    print("\n=== Parse XML ===")
    loaded_root = read_xml(path)
    parse_xml_manually(loaded_root)
    parse_with_xpath(loaded_root)

    print("\n=== Modify XML ===")
    modify_xml(loaded_root)
    write_xml(path, loaded_root)
    print(f"  Modified XML written to {path}")

    print("\n=== Final XML ===")
    with open(path, "r") as f:
        print(f.read())

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
