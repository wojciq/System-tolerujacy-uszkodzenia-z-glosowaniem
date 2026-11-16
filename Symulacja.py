import numpy as np
import random
import csv
import matplotlib.pyplot as plt


def stworz_wykresy(wyniki_mediana, wyniki_wiekszosc, wyniki_wazone, wartosc_prawdziwa):
    # Konwersja na numpy
    tablica_mediana = np.array(wyniki_mediana)
    tablica_wiekszosc = np.array(wyniki_wiekszosc)
    tablica_wazone = np.array(wyniki_wazone)

    bledy_mediana = np.abs(tablica_mediana - wartosc_prawdziwa)
    bledy_wiekszosc = np.abs(tablica_wiekszosc - wartosc_prawdziwa)
    bledy_wazone = np.abs(tablica_wazone - wartosc_prawdziwa)

    plt.style.use('seaborn-v0_8-whitegrid')

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(22, 7.6))

    ZOOM_RANGE = 100
    iteracje_zoom = range(1, ZOOM_RANGE +1)

    # WYKRES 1 - porównanie decyzji
    ax1.set_title(f'Porównanie decyzji algorytmów przesunięciu jednego czujnika', fontsize=14, fontweight='bold')

    # Linia odniesienia (dane prawdziwe)
    ax1.plot(iteracje_zoom, [wartosc_prawdziwa] * ZOOM_RANGE, 'k--', linewidth=2, label='Wartość Prawdziwa', alpha=0.6)

    ax1.plot(iteracje_zoom, tablica_mediana[:ZOOM_RANGE],
             color='green', marker='o', markersize=5, label='Mediana', alpha=0.9)

    ax1.plot(iteracje_zoom, tablica_wazone[:ZOOM_RANGE],
             color='blue', linestyle='--', label='Śr. Ważona', alpha=0.7)

    ax1.scatter(iteracje_zoom, tablica_wiekszosc[:ZOOM_RANGE],
                color='red', marker='x', s=80, label='Większość', zorder=5)

    ax1.set_ylabel('Wartość [porównanie]')
    ax1.legend(loc='upper right', frameon=True)
    ax1.set_xlim(1, ZOOM_RANGE)

    # WYKRES 2 - błąd bezwzględny
    ax2.set_title('Błąd bezwzględny algorytmów (Im bliżej 0 tym lepiej)', fontsize=12)

    ax2.bar(iteracje_zoom, bledy_wazone[:ZOOM_RANGE], color='blue', alpha=0.3, label='Błąd Ważony', width=0.8)
    ax2.plot(iteracje_zoom, bledy_mediana[:ZOOM_RANGE], color='green', linewidth=2, label='Błąd Mediana')
    ax2.plot(iteracje_zoom, bledy_wiekszosc[:ZOOM_RANGE], 'rx', label='Błąd Większość')

    ax2.set_ylabel('|Błąd|')
    ax2.set_xlim(1, ZOOM_RANGE)
    ax2.legend()

    # WYKRES 3 - pudelkowy dla calosci
    ax3.set_title(f'Statystyka błędów', fontsize=12)

    dane_do_pudelka = [
        bledy_mediana,
        bledy_wiekszosc[~np.isnan(bledy_wiekszosc)],
        bledy_wazone
    ]

    bp = ax3.boxplot(dane_do_pudelka,
                     tick_labels=['Mediana', 'Większość', 'Śr. ważona'],
                     patch_artist=True,
                     showfliers=True,
                     flierprops=dict(marker='o', markerfacecolor='red', markersize=6, linestyle='none'))

    colors = ['lightgreen', 'yellow', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ax3.yaxis.grid(True)
    ax3.set_ylabel('Wielkość błędu')

    plt.tight_layout()
    plt.show()

def run_simulation():
    # Konfiguracja
    ITERACJE = 100
    WARTOSC_PRAWDZIWA = 100.0
    SZUM = 2.0
    USZKODZENIE = 0.05
    PLIK_CSV = 'wyniki_symulacji.csv'
    TYP_BLEDU = 2

    wynikiMediana = []
    wynikiWiekszosc = []
    wynikiWazone = []

    danecsv = []

    for i in range(ITERACJE):
        # Generowanie odczytów
        czujniki = []
        for j in range(3):
            odczyt = WARTOSC_PRAWDZIWA + np.random.normal(0, SZUM)
            czujniki.append(odczyt)
            if TYP_BLEDU == 0:
                if random.random() < USZKODZENIE:
                    odczyt += np.random.choice([-20, 20])
            elif TYP_BLEDU == 1:
                czujniki[0] = WARTOSC_PRAWDZIWA + i * 0.5
            elif TYP_BLEDU == 2:
                czujniki[0] += 15

        # ALGORYTM 1
        wynikMediana = np.median(czujniki)
        wynikiMediana.append(wynikMediana)

        # ALGORYTM 2:
        wiekszosc = []
        tolerancja = 0.02
        pary = [(0, 1), (0, 2), (1, 2)]

        for j, k in pary:
            roznica = abs(czujniki[j] - czujniki[k])
            sredniaPary = (czujniki[j] + czujniki[k]) / 2.0
            if roznica <= (sredniaPary * tolerancja):
                wiekszosc.extend([czujniki[j], czujniki[k]])

        if wiekszosc:
            wynikWiekszosc = np.mean(np.unique(wiekszosc))
            wynikiWiekszosc.append(wynikWiekszosc)
        else:
            wynikWiekszosc = np.nan
            wynikiWiekszosc.append(np.nan)

        # ALGORYTM 3:
        wagi = []
        for j in range(3):
            odchylenie = 0
            for k in range(3):
                if j != k:
                    odchylenie += abs(czujniki[j] - czujniki[k])
            wagi.append(1.0 / odchylenie)

        wagi = np.array(wagi)
        wagi /= wagi.sum()
        wynikWazone = np.sum(czujniki * wagi)
        wynikiWazone.append(wynikWazone)

        # Dane do csv
        wiersz = [
            i + 1,
            round(czujniki[0], 3),
            round(czujniki[1], 3),
            round(czujniki[2], 3),
            round(wynikMediana, 3),
            round(wynikWiekszosc, 3) if not np.isnan(wynikWiekszosc) else "BRAK",
            round(wynikWazone, 3)
        ]
        danecsv.append(wiersz)

    # Zapis do csv
    try:
        with open(PLIK_CSV, mode='w', newline='') as file:
            zapisywanie = csv.writer(file, delimiter=';')
            naglowek = [
                "Iteracja",
                "Czujnik_1", "Czujnik_2", "Czujnik_3",
                "Wynik_Mediana", "Wynik_Wiekszosc", "Wynik_Wazone"
            ]
            zapisywanie.writerow(naglowek)
            zapisywanie.writerows(danecsv)
    except IOError as e:
        print(f"Błąd zapisu pliku CSV: {e}")

    stworz_wykresy(wynikiMediana, wynikiWiekszosc, wynikiWazone, WARTOSC_PRAWDZIWA)

if __name__ == "__main__":
    run_simulation()