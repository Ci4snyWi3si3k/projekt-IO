import tkinter as tk
from tkinter import ttk, messagebox
from db import connect
import queries


# --- Okno logowania ---
def login_window(conn):
    def attempt_login():
        login = entry_login.get().strip()
        haslo = entry_password.get().strip()

        user = queries.login_user(conn, login, haslo)
        if not user:
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło!")
            return
        typ, osoba_id = user
        root.destroy()
        main_window(conn, typ, osoba_id)

    root = tk.Tk()
    root.title("Logowanie - Księgarnia")
    root.geometry("300x200")
    root.resizable(False, False)

    tk.Label(root, text="Login:").pack(pady=5)
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Hasło:").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Zaloguj", command=attempt_login).pack(pady=10)

    root.mainloop()


# --- Popup z egzemplarzami (tylko dostępne) ---
def show_egzemplarze_popup(conn, id_entry):
    popup = tk.Toplevel()
    popup.title("Dostępne egzemplarze")
    popup.geometry("700x400")

    frame = tk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    y_scroll = tk.Scrollbar(frame, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(
        frame,
        columns=("ID", "Tytuł", "Autor", "Wydawnictwo"),
        show="headings",
        yscrollcommand=y_scroll.set
    )
    tree.pack(fill="both", expand=True)
    y_scroll.config(command=tree.yview)

    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda c=col: sort_column(tree, c, not reverse))

    for col in ("ID", "Tytuł", "Autor", "Wydawnictwo"):
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
        tree.column(col, width=150)

    # Pobierz tylko dostępne egzemplarze
    egzemplarze = queries.get_egzemplarze_by_status(conn, 'DOSTEPNY')
    for e in egzemplarze:
        tree.insert("", "end", values=(e[0], e[1], e[2], e[3]))

    # Dwuklik = wybór egzemplarza
    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            id_entry.delete(0, tk.END)
            id_entry.insert(0, values[0])
            popup.destroy()

    tree.bind("<Double-1>", on_select)


# --- Popup z wypożyczonymi książkami (zwrot) ---
def show_wypozyczone_popup(conn, id_czyt_entry, bibliotekarz_id):
    czytelnik_id = id_czyt_entry.get().strip()
    if not czytelnik_id:
        messagebox.showerror("Błąd", "Najpierw wybierz czytelnika!")
        return

    popup = tk.Toplevel()
    popup.title("Wypożyczone książki czytelnika")
    popup.geometry("750x400")

    frame = tk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    y_scroll = tk.Scrollbar(frame, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    columns = ("ID wypożyczenia", "Tytuł", "Autor", "Data wypożyczenia", "Termin zwrotu")
    tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=y_scroll.set)
    y_scroll.config(command=tree.yview)
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    # Pobierz dane z widoku
    records = queries.get_wypozyczone_by_reader(conn, czytelnik_id)
    for r in records:
        tree.insert("", "end", values=r)

    # Dwuklik = zwrot książki
    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            wypozyczenie_id = values[0]
            confirm = messagebox.askyesno("Zwrot", f"Czy na pewno chcesz zwrócić książkę:\n\n{values[1]} ({values[2]})?")
            if confirm:
                try:
                    queries.return_book(conn, wypozyczenie_id, bibliotekarz_id)
                    messagebox.showinfo("Sukces", f"Książka '{values[1]}' została zwrócona.")
                    popup.destroy()
                except Exception as e:
                    messagebox.showerror("Błąd", str(e))

    tree.bind("<Double-1>", on_select)


# --- Główne okno aplikacji ---
def main_window(conn, typ, osoba_id):
    win = tk.Tk()
    win.title("System Księgarni")
    win.geometry("1000x600")

    tk.Label(win, text=f"Zalogowano jako: {typ}", font=("Arial", 12, "bold")).pack(pady=10)

    frame_books = tk.Frame(win)
    frame_books.pack(fill="both", expand=True, padx=10, pady=10)

    y_scroll = tk.Scrollbar(frame_books, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    x_scroll = tk.Scrollbar(frame_books, orient="horizontal")
    x_scroll.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        frame_books,
        columns=("ID", "Tytuł", "Autor", "Wydawnictwo", "Kategoria"),
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
    tree.pack(fill="both", expand=True)

    y_scroll.config(command=tree.yview)
    x_scroll.config(command=tree.xview)

    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda c=col: sort_column(tree, c, not reverse))

    for col in ("ID", "Tytuł", "Autor", "Wydawnictwo", "Kategoria"):
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
        tree.column(col, width=170)

    def show_books():
        for row in tree.get_children():
            tree.delete(row)
        for b in queries.get_books(conn):
            tree.insert("", "end", values=(b[0], b[1], b[2], b[3], b[4]))

    tk.Button(win, text="Odśwież książki", command=show_books).pack(pady=5)

    # --- Panel bibliotekarza ---
    if typ.lower() == "bibliotekarz":
        frame = tk.LabelFrame(win, text="Wypożycz / Zwróć książkę", padx=10, pady=10)
        frame.pack(pady=10)

        tk.Label(frame, text="ID czytelnika:").grid(row=0, column=0, padx=5, pady=5)
        id_czyt = tk.Entry(frame)
        id_czyt.grid(row=0, column=1)

        def open_reader_window():
            reader_win = tk.Toplevel(win)
            reader_win.title("Wybierz czytelnika")
            reader_win.geometry("500x300")

            tree_readers = ttk.Treeview(reader_win, columns=("ID", "Imię", "Nazwisko", "Nr karty"), show="headings")
            for col in ("ID", "Imię", "Nazwisko", "Nr karty"):
                tree_readers.heading(col, text=col)
                tree_readers.column(col, width=110)
            tree_readers.pack(fill="both", expand=True)

            scrollbar = tk.Scrollbar(reader_win, orient="vertical", command=tree_readers.yview)
            tree_readers.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            readers = queries.get_readers(conn)
            for row in readers:
                tree_readers.insert("", "end", values=row)

            def select_reader(event):
                selected = tree_readers.focus()
                if not selected:
                    return
                values = tree_readers.item(selected, "values")
                id_czyt.delete(0, tk.END)
                id_czyt.insert(0, values[0])
                reader_win.destroy()

            tree_readers.bind("<Double-1>", select_reader)
        tk.Button(frame, text="Wybierz czytelnika", command=open_reader_window).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="ID egzemplarza:").grid(row=1, column=0, padx=5, pady=5)
        id_egz = tk.Entry(frame)
        id_egz.grid(row=1, column=1)

        tk.Button(frame, text="Dostępne", command=lambda: show_egzemplarze_popup(conn, id_egz)).grid(row=1, column=2, padx=5)
        tk.Button(frame, text="Zwrot", command=lambda: show_wypozyczone_popup(conn, id_czyt, osoba_id)).grid(row=1, column=3, padx=5)
        def borrow():
            try:
                queries.borrow_book(conn, id_czyt.get(), id_egz.get(), osoba_id)
                messagebox.showinfo("Sukces", " Wypożyczono książkę!")
                id_czyt.delete(0, tk.END)
                id_egz.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Błąd", str(e))
        tk.Button(frame, text=" Wypożycz", command=borrow).grid(row=2, column=0, columnspan=4, pady=10)
    show_books()
    win.mainloop()


# --- Start programu ---
if __name__ == "__main__":
    conn = connect()
    if conn:
        login_window(conn)
