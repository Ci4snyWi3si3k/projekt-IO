📚 System informatyczny Biblioteki (Projekt Inżynieria Oprogramowania)

Desktopowa aplikacja dla Bibliotekarza i Czytelnika, stworzona w ramach projektu zaliczeniowego z Inżynierii Oprogramowania na Politechnice Koszalińskiej. 



✨ Cel Projektu
Głównym celem projektu jest stworzenie aplikacji desktopowej do wypożyczania książek w Bibliotece. Aplikacja ma za zadanie efektywnie zarządzać księgozbiorem, ułatwiać pracę bibliotekarzom oraz zapewniać czytelnikom intuicyjny dostęp do katalogu i ich konta.

Kluczowe Funkcjonalności (MVP)
W pierwszej fazie implementacji skupiono się na podstawowym rdzeniu systemu:


F-01 Przegląd księgozbioru: Szybkie wyszukiwanie pozycji/egzemplarza po tytule, autorze, ISBN, gatunku i dziale.


F-04 Wypożyczenie / F-05 Wydanie/Odbiór: Kluczowa logika biznesowa rejestracji wypożyczeń i przyjmowania zwrotów przez Bibliotekarza.


F-03 Status książki: Jednoznaczne zarządzanie stanem egzemplarzy (dostępny, wypożyczony, zarezerwowany, uszkodzony, archiwalny).


F-08 Logowanie i role: System logowania identyfikujący Aktorów (Czytelnik, Bibliotekarz) i nadający uprawnienia.


F-26 Widok "Moje konto": Podgląd aktualnych wypożyczeń dla Czytelnika.

Aktorzy Systemu
System obsługuje trzy główne role:


Bibliotekarz: Zarządza kontami i katalogiem, realizuje wypożyczenia/zwroty, nalicza kary, opisuje uszkodzenia.


Czytelnik: Posiada konto, loguje się, przegląda katalog, rezerwuje, sprawdza statusy.


System: Pilnuje reguł (limity, terminy), wysyła powiadomienia, prowadzi historię.



🖼️ Interfejs Użytkownika (GUI)
Interfejs użytkownika (GUI) został zaprojektowany z myślą o prostocie i intuicyjności. Zespół wybrał Widok minimalistyczny (GUI 1) oparty na tabelach, który jest zoptymalizowany pod kątem szybkości obsługi danych.

Kluczowe widoki:


Ekran Logowania (F-08): Dla Czytelnika i Bibliotekarza.


Widok Katalogu (F-01/F-20): Lista książek z możliwością filtrowania i paginacją (domyślnie 20 wierszy/stronę).


Stanowisko Bibliotekarza (F-05): Centralny punkt do szybkiego wypożyczania i przyjmowania zwrotów.


Moje Konto (F-26): Widok z danymi użytkownika i aktualnymi wypożyczeniami.



📅 Harmonogram i Zespół
Projekt realizowany jest w ramach przedmiotu Inżynieria Oprogramowania na Politechnice Koszalińskiej.

Kluczowe Terminy:

Data rozpoczęcia: 05.10.2025 

Data zakończenia: 23.11.2025

Przewidywana data zakończenia: 2x.1.2026


@Projekt zrealizowany na Politechnice Koszalińskiej, 2025/2026.
🛠️ Stos Technologiczny (Tech Stack)
Aplikacja jest zaprojektowana jako proste, niezależne rozwiązanie desktopowe.
