# Kyler Olsen
# Mar 2024
import re

__LINKS = {
    '/ot/gen': ("Gen.", "Genesis", ),
    '/ot/ex': ("Ex.", "Exodus", ),
    '/ot/lev': ("Lev.", "Leviticus", ),
    '/ot/num': ("Num.", "Numbers", ),
    '/ot/deut': ("Deut.", "Deuteronomy", ),
    '/ot/josh': ("Josh.", "Joshua", ),
    '/ot/judg': ("Judg.", "Judges", ),
    '/ot/ruth': ("Ruth", ),
    '/ot/1-sam': ("1 Sam.", "1 Samuel", ),
    '/ot/2-sam': ("2 Sam.", "2 Samuel", ),
    '/ot/1-kgs': ("1 Kgs.", "1 Kings", ),
    '/ot/2-kgs': ("2 Kgs.", "2 Kings", ),
    '/ot/1-chr': ("1 Chr.", "1 Chronicles", ),
    '/ot/2-chr': ("2 Chr.", "2 Chronicles", ),
    '/ot/ezra': ("Ezra", ),
    '/ot/neh': ("Neh.", "Nehemiah", ),
    '/ot/esth': ("Esth.", "Esther", ),
    '/ot/job': ("Job", ),
    '/ot/ps': ("Ps.", "Psalm", "Psalms", ),
    '/ot/prov': ("Prov.", "Proverbs", ),
    '/ot/eccl': ("Eccl.", "Ecclesiastes", ),
    '/ot/song': ("Song", "Song of Solomon", ),
    '/ot/isa': ("Isa.", "Isaiah", ),
    '/ot/jer': ("Jer.", "Jeremiah", ),
    '/ot/lam': ("Lam.", "Lamentations", ),
    '/ot/ezek': ("Ezek.", "Ezekiel", ),
    '/ot/dan': ("Dan.", "Daniel", ),
    '/ot/hosea': ("Hosea", ),
    '/ot/joel': ("Joel", ),
    '/ot/amos': ("Amos", ),
    '/ot/obad': ("Obad.", "Obadiah", ),
    '/ot/jonah': ("Jonah", ),
    '/ot/micah': ("Micah", ),
    '/ot/nahum': ("Nahum", ),
    '/ot/hab': ("Hab.", "Habakkuk", ),
    '/ot/zeph': ("Zeph.", "Zephaniah", ),
    '/ot/hag': ("Hag.", "Haggai", ),
    '/ot/zech': ("Zech.", "Zechariah", ),
    '/ot/mal': ("Mal.", "Malachi", ),
    '/nt/matt': ("Matt.", "Matthew", ),
    '/nt/mark': ("Mark", ),
    '/nt/luke': ("Luke", ),
    '/nt/john': ("John", ),
    '/nt/acts': ("Acts", ),
    '/nt/rom': ("Rom.", "Romans", ),
    '/nt/1-cor': ("1 Cor.", "1 Corinthians", ),
    '/nt/2-cor': ("2 Cor.", "2 Corinthians", ),
    '/nt/gal': ("Gal.", "Galatians", ),
    '/nt/eph': ("Eph.", "Ephesians", ),
    '/nt/philip': ("Philip.", "Philippians", ),
    '/nt/col': ("Col.", "Colossians", ),
    '/nt/1-thes': ("1 Thes.", "1 Thessalonians", ),
    '/nt/2-thes': ("2 Thes.", "2 Thessalonians", ),
    '/nt/1-tim': ("1 Tim.", "1 Timothy", ),
    '/nt/2-tim': ("2 Tim.", "2 Timothy", ),
    '/nt/titus': ("Titus", ),
    '/nt/philem': ("Philem.", "Philemon", ),
    '/nt/heb': ("Heb.", "Hebrews", ),
    '/nt/james': ("James", ),
    '/nt/1-pet': ("1 Pet.", "1 Peter", ),
    '/nt/2-pet': ("2 Pet.", "2 Peter", ),
    '/nt/1-jn': ("1 Jn.", "1 John", ),
    '/nt/2-jn': ("2 Jn.", "2 John", ),
    '/nt/3-jn': ("3 Jn.", "3 John", ),
    '/nt/jude': ("Jude", ),
    '/nt/rev': ("Rev.", "Revelation", ),
    '/bofm/1-ne': ("1 Ne.", "1 Nephi", ),
    '/bofm/2-ne': ("2 Ne.", "2 Nephi", ),
    '/bofm/jacob': ("Jacob", ),
    '/bofm/enos': ("Enos", ),
    '/bofm/jarom': ("Jarom", ),
    '/bofm/omni': ("Omni", ),
    '/bofm/w-of-m': ("WofM", "W of M", "Words of Mormon", ),
    '/bofm/mosiah': ("Mosiah", ),
    '/bofm/alma': ("Alma", ),
    '/bofm/hel': ("Hel.", "Helaman", ),
    '/bofm/3-ne': ("3 Ne.", "3 Nephi", ),
    '/bofm/4-ne': ("4 Ne.", "4 Nephi", ),
    '/bofm/morm': ("Morm.", "Mormon", ),
    '/bofm/ether': ("Ether", ),
    '/bofm/moro': ("Moro.", "Moroni", ),
    '/dc-testament/dc': ("D&C", "D & C", "DandC", "D and C", "D+C", "D + C", "Doctrine and Covenants", ),
    '/dc-testament/od': ("OD", "Official Declaration", ),
    '/pgp/moses': ("Moses", ),
    '/pgp/abr': ("Abr.", "Abraham", ),
    '/pgp/js-m': ("JS—M", "Joseph Smith—Matthew", "JS-M", "JSM", "Joseph Smith-Matthew", ),
    '/pgp/js-h': ("JS—H", "Joseph Smith—History", "JS-H", "JSH", "Joseph Smith-History", ),
    '/pgp/a-of-f': ("A of F", "AofF", "Articles of Faith", ),
    '/ot': ("OT", "Old Testament", "The Old Testament", ),
    '/nt': ("NT", "New Testament", "The New Testament", ),
    '/bofm': ("BofM", "Book of Mormon", "The Book of Mormon", ),
    '/pgp': ("PGP", "PofGP", "Pearl of Great Price", "The Pearl of Great Price", ),
}

def __find_book(book: str) -> tuple[str, list[str]]:
    matches: dict[str, str] = {}
    for key, values in __LINKS.items():
        if book.lower().replace('.', '') in [i.lower().replace('.', '') for i in values]:
            return (key, [])
        else:
            for value in values:
                if value.lower().startswith(book.lower().replace('.', '')):
                    matches[key] = values[-1]
    if len(matches) == 1:
        return (list(matches.keys())[0], [])
    else:
        return ("", list(matches.values()))

def convert_reference(ref: str) -> tuple[str, list[str]]:
    pattern = re.findall(r'^.*\w\.?\s\d', ref)
    if pattern:
        i = len(pattern[-1])-1
        book, cv = ref[:i-1], \
            ref[i:].replace(' ', '').replace('–', '-').replace(':', '/')
        link, possible = __find_book(book)
        if link:
            return (f"{link}/{cv}", [])
        else:
            return ("", possible)
    else:
        return __find_book(ref)

def convert_url(url: str) -> str:
    parts = url.strip('/').split('/')

    if not parts:
        raise ValueError("Empty URL")

    book_key = f"/{'/'.join(parts[:2]) if len(parts) >= 2 else parts[0]}"
    remainder = parts[2:] if len(parts) > 2 else []

    if book_key not in __LINKS:
        raise ValueError(f"Book key not found: {book_key}")

    book_name = __LINKS[book_key][-1]

    if not remainder:
        return book_name
    elif len(remainder) == 1:
        return f"{book_name} {remainder[0]}"
    elif len(remainder) == 2:
        return f"{book_name} {remainder[0]}:{remainder[1]}"
    else:
        raise ValueError(f"Unexpected format in URL: {url}")

if __name__ == '__main__':
    # import json
    # with open('refs.json', 'w', encoding='utf-8') as file:
    #     json.dump(__LINKS, file, indent=4)
    with open('refs.txt', encoding='utf-8') as file:
        # for i in file.readlines():
        for i in file.readlines()[::50]:
            ref = convert_reference(i[:-1])[0]
            if ref:
                print(convert_url(ref))
