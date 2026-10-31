# OMSkan

Aplikacja służąca do podziału zeskanowanych prac uczniów oznaczonych odpowiednimi kodami QR.

## Pobieranie

Najnowsza wersja programu znajduje się na stronie wydań:

**[Pobierz najnowszą wersję](https://github.com/dartsakratus/OMSkan2/releases/latest)**

Na tej stronie, w sekcji **Assets** (na samym dole wydania), należy wybrać plik odpowiedni dla swojego systemu:

| System | Plik |
|--------|------|
| Windows | `OMSkan-Windows.exe` |
| macOS | `OMSkan-macOS.zip` |
| Linux | patrz sekcja [Linux](#linux) |

---

## Windows

1. Pobierz plik `OMSkan-Windows.exe`.
2. Kliknij go dwukrotnie, aby uruchomić program. Instalacja nie jest potrzebna.
3. Przy pierwszym uruchomieniu może pojawić się niebieskie okno **„System Windows ochronił ten komputer"**. Kliknij **Więcej informacji**, a następnie **Uruchom mimo to**.

Jeśli program antywirusowy zablokuje plik, dodaj go do wyjątków albo pobierz go ponownie.

---

## macOS

> Program działa na komputerach Mac z procesorem Apple (M1 i nowszymi).

1. Pobierz plik `OMSkan-macOS.zip`.
2. Kliknij go dwukrotnie, aby go rozpakować. Powstanie aplikacja **OMSkan**.
3. Przeciągnij **OMSkan** do folderu **Programy** (opcjonalnie, można też uruchamiać go z dowolnego miejsca).
4. Przy pierwszym uruchomieniu **nie klikaj dwukrotnie**. Kliknij aplikację prawym przyciskiem myszy (lub z klawiszem Control), wybierz **Otwórz**, a potem ponownie **Otwórz** w oknie z ostrzeżeniem.
5. Jeśli system nadal blokuje aplikację, wejdź w **Ustawienia systemowe → Prywatność i ochrona**, przewiń w dół do informacji o zablokowanej aplikacji OMSkan i kliknij **Otwórz mimo to**.

Ostrzeżenie pojawia się tylko za pierwszym razem, ponieważ aplikacja nie jest zweryfikowana przez firmę Apple.

---

## Linux

Na Linuksie program można uruchomić ponbierając to repozytorium i instalując odpowiednie pakiety.

1. Zainstaluj Pythona, pip i Tkinter:

   ```bash
   sudo apt install python3 python3-pip python3-venv python3-tk
   ```

2. Pobierz kod programu (zielony przycisk **Code → Download ZIP** na stronie repozytorium i rozpakuj go) albo użyj gita:

   ```bash
   git clone https://github.com/dartsakratus/OMSkan2.git
   cd OMSkan2
   ```

3. Utwórz środowisko i zainstaluj wymagane biblioteki:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Uruchom program:

   ```bash
   python3 content/app.py
   ```

Przy kolejnych uruchomieniach wystarczy wejść do folderu programu i wykonać:

```bash
source .venv/bin/activate
python3 content/app.py
```

---

## Użycie

1. Kliknij **Przeglądaj...** obok pola **Plik ze skanami** i wybierz plik PDF.
2. Wybierz **Folder końcowy**, w którym zostaną zapisane podzielone prace. Domyślnie ustawia się na ten sam folder w którym znajduje się wybrany plik.
3. Ustaw **Etap** na odpowiednią wartość.
4. Kliknij **Podziel plik** i poczekaj na komunikat **Gotowe**. W przypadku większych plików może to chwilę potrwać.