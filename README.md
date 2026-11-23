# Symulator systemu tolerującego uszkodzenia z głosowaniem

Programowy model oraz symulator Monte Carlo służący do analizy niezawodności systemów krytycznych, bazujący na architekturze **potrajania z głosowaniem**. Projekt zrealizowany w języku **Python** z wykorzystaniem bibliotek **NumPy** oraz **Matplotlib**.

## Wprowadzenie i cel projektu

W systemach o podwyższonych rygorach bezpieczeństwa, np. w lotnictwie, motoryzacji czy medycynie, awaria pojedynczego czujnika nie może doprowadzić do błędnej decyzji sterującej. Rozwiązaniem tego problemu jest redundancja sprzętowa wspierana przez algorytmy głosujące, które na podstawie trzech niezależnych kanałów pomiarowych ($S_1, S_2, S_3$) wyznaczają jeden wiarygodny sygnał wyjściowy ($S_{out}$).

Celem projektu było stworzenie elastycznego środowiska symulacyjnego pozwalającego na wstrzykiwanie różnych typów zakłóceń do kanałów pomiarowych oraz ocenę statystyczną skuteczności trzech odmiennych strategii głosowania.

## Zaimplementowane algorytmy głosujące

1. **Uogólniony głosujący medianowy:** Sortuje odczyty z trzech kanałów i wybiera wartość środkową. Podejście bezprogowe, które naturalnie izoluje pojedyncze, skrajne błędy czujników bez konieczności kalibracji parametrów.
2. **Sformalizowany głosujący większościowy:** Wyszukuje podzbiór kanałów zgodnych ze sobą w granicach ustalonej tolerancji względnej (w symulacji przyjęto próg **2%**) i zwraca ich średnią. W przypadku braku konsensusu system zgłasza błąd.
3. **Algorytm średniej ważonej:** Wyznacza wyjście jako średnią wszystkich kanałów, gdzie wagi są dynamicznie obliczane jako odwrotność sumy odchyleń danego czujnika od pozostałych. Pozwala na wygładzanie szumu pomiarowego przy zachowaniu ciągłości sygnału.

## Model uszkodzeń i metodologia (Monte Carlo)

Symulator przeprowadza $N = 100$ iteracji dla sygnału odniesienia o wartości `100.0`, nakładając na wszystkie kanały szum gaussowski $\mathcal{N}(0, 2.0)$ oraz wstrzykując do jednego z czujników wybrane scenariusze awarii:

* **Błędy impulsowe:** Losowe „szpilki” o dużej amplitudzie ($\pm 20$), pojawiające się z prawdopodobieństwem $p = 0.05$.
* **Błąd przesunięcia:** Stałe odchylenie wartości odczytu o $+15$ względem wartości rzeczywistej.
* **Dryf pomiarowy:** Błąd systematyczny narastający liniowo w czasie (o $+0.5$ w każdej kolejnej iteracji).

## Kluczowe wnioski z symulacji

* **Odporność na błędy impulsowe i dryf:** Algorytm medianowy wykazuje najwęższy rozstęp międzykwartylowy błędów i najskuteczniej maskuje pojedyncze awarie o dowolnej amplitudzie oraz narastający dryf jednego z sensorów.
* **Precyzja vs Izolacja błędu:** Średnia ważona najlepiej redukuje szum gaussowski w warunkach nominalnych, jednak przy awarii kanału nie zapewnia jego pełnej izolacji – błąd częściowo „przecieka” do sygnału wyjściowego.
* **Dylemat dostępności i bezpieczeństwa:** Głosowanie medianowe maksymalizuje dostępność systemu - zawsze zwraca wynik, co jest kluczowe np. w układach sterowania lotem, natomiast głosowanie większościowe priorytetyzuje bezpieczeństwo, wstrzymując generowanie wyniku w sytuacji braku jednoznacznego konsensusu.

### Pliki w projekcie
* `Symulacja.py` – Kod źródłowy symulatora generujący wykresy przebiegów czasowych, wykresy błędów bezwzględnych oraz eksportujący surowe dane pomiarowe do pliku CSV.
* `sprawozdanie.pdf` – Pełna dokumentacja techniczna, schemat blokowy symulatora oraz szczegółowa analiza wykresów pudełkowych.

### Wymagania
Do uruchomienia symulacji wymagany jest Python 3 oraz biblioteki `numpy` i `matplotlib`:
```bash
pip install numpy matplotlib
