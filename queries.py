def login_user(conn, login, haslo):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT typ_uzytkownika, osoba_id
        FROM konto
        WHERE login = :login AND haslo = :haslo
    """, {'login': login, 'haslo': haslo})
    return cursor.fetchone()


def get_books(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, tytul, autor, wydawnictwo, kategoria
        FROM widok_ksiazki_rozszerzone
        ORDER BY tytul
    """)
    return cursor.fetchall()


def borrow_book(conn, czytelnik_id, egzemplarz_id, bibliotekarz_id):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status FROM egzemplarz WHERE id_egzemplarza = :eid
    """, {"eid": egzemplarz_id})
    row = cursor.fetchone()
    if not row:
        raise Exception("Nie znaleziono egzemplarza o podanym ID.")

    status = row[0].upper()
    if status not in ("DOSTEPNY", "ZAREZERWOWANY"):
        raise Exception(f"Egzemplarz nie może być wypożyczony — aktualny status: {status}")

    cursor.execute("""
        INSERT INTO wypozyczenie (id_wypozyczenia, czytelnik_id, egzemplarz_id, bibliotekarz_id, data_wypozyczenia)
        VALUES (seq_wypozyczenie.NEXTVAL, :cid, :eid, :bid, SYSDATE)
    """, {"cid": czytelnik_id, "eid": egzemplarz_id, "bid": bibliotekarz_id})

    cursor.execute("""
        UPDATE egzemplarz SET status = 'WYPOZYCZONY' WHERE id_egzemplarza = :eid
    """, {"eid": egzemplarz_id})

    conn.commit()


def return_book(conn, wypozyczenie_id, bibliotekarz_id, uwagi=None):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id_egzemplarza
        FROM wypozyczenie w
        JOIN egzemplarz e ON w.egzemplarz_id = e.id_egzemplarza
        WHERE w.id_wypozyczenia = :wid
          AND NOT EXISTS (SELECT 1 FROM zwrot z WHERE z.wypozyczenie_id = w.id_wypozyczenia)
    """, {"wid": wypozyczenie_id})

    row = cursor.fetchone()
    if not row:
        raise Exception("Nie znaleziono wypożyczenia lub zostało już zwrócone.")

    egzemplarz_id = row[0]

    cursor.execute("""
        INSERT INTO zwrot (id_zwrotu, wypozyczenie_id, bibliotekarz_id, data_zwrotu, uwagi)
        VALUES (zwrot_seq.NEXTVAL, :wid, :bid, SYSDATE, :uwagi)
    """, {"wid": wypozyczenie_id, "bid": bibliotekarz_id, "uwagi": uwagi})

    cursor.execute("""
        UPDATE egzemplarz SET status = 'DOSTEPNY' WHERE id_egzemplarza = :eid
    """, {"eid": egzemplarz_id})

    conn.commit()


def get_readers(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_czytelnika, o.imie, o.nazwisko, c.nr_karty
        FROM czytelnik c
        JOIN osoba o ON c.osoba_id = o.id_osoby
        ORDER BY o.nazwisko
    """)
    return cursor.fetchall()


def get_egzemplarze_by_status(conn, status):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id_egzemplarza, k.tytul, a.imie || ' ' || a.nazwisko AS autor, w.nazwa AS wydawnictwo
        FROM egzemplarz e
        JOIN ksiazka k ON e.ksiazka_id = k.id_ksiazki
        JOIN autor a ON k.autor_id = a.id_autora
        JOIN wydawnictwo w ON k.wydawnictwo_id = w.id_wydawnictwa
        WHERE UPPER(e.status) = :status
        ORDER BY k.tytul, a.nazwisko
    """, {"status": status.upper()})
    return cursor.fetchall()


def get_wypozyczone_by_reader(conn, czytelnik_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id_wypozyczenia,
            tytul,
            autor,
            TO_CHAR(data_wypozyczenia, 'YYYY-MM-DD'),
            TO_CHAR(termin_zwrotu, 'YYYY-MM-DD')
        FROM vw_wypozyczone_czytelnika_detal
        WHERE id_czytelnika = :cid
        ORDER BY data_wypozyczenia DESC
    """, {"cid": czytelnik_id})
    return cursor.fetchall()
