import oracledb

def connect():
    try:
        connection = oracledb.connect(
            user="KSIEGARNIA",
            password="haslo123",      # ← wpisz swoje hasło
            dsn="localhost:1521/XEPDB1"  # ← dopasuj jeśli inny service_name
        )
        return connection
    except Exception as e:
        print(" Błąd połączenia z bazą:", e)
        return None
