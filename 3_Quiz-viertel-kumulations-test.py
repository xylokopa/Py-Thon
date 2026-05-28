# 3_Quiz-viertel-kumulations-test.py
from collections import Counter
import math
import os
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- 1. DATEN AUS TEXTDATEI EINLESEN ---
dateiname = "antworten.txt"
answers = []

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as file:
        answers = [line.strip() for line in file if line.strip()]
else:
    print(
        f"Fehler: Die Datei '{dateiname}' wurde nicht gefunden. Generiere Demo-Daten..."
    )
    # Demo-Daten mit "b-Trend" im letzten Viertel
    answers = (
        ["A.a"] * 20
        + ["A.b"] * 20
        + ["A.c"] * 20
        + ["A.d"] * 20  # 1. Viertel: Sauber
        + ["A.a"] * 20
        + ["A.b"] * 20
        + ["A.c"] * 20
        + ["A.d"] * 20  # 2. Viertel: Sauber
        + ["A.a"] * 5
        + ["A.b"] * 65
        + ["A.c"] * 5
        + ["A.d"] * 5  # Letztes Viertel: Test mit b-Überhang
    )

# Antworten extrahieren
extracted = [line.split(".")[-1] for line in answers if "." in line]
total_count = len(extracted)

if total_count < 20:
    print(
        "Die Datei enthält zu wenige Daten für diese stochastische Auswertung."
    )
    exit()

# Daten in Abschnitte unterteilen
quarter_size = total_count / 4
q1_data = extracted[: math.ceil(quarter_size)]
q2_data = extracted[math.ceil(quarter_size) : math.floor(quarter_size * 2)]
q4_data = extracted[math.ceil(quarter_size * 3) :]

# --- 2. GRAFISCHE OBERFLÄCHE (MATPLOTLIB) EINRICHTEN ---
fig, axes = plt.subplots(1, 4, figsize=(15, 6), sharey=True)
# Platz nach unten für zwei Slider vergrößern
plt.subplots_adjust(bottom=0.3)

categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]

bar_containers = []
text_elements = []


# --- 3. INTERAKTIVE UPDATE-FUNKTION ---
def update(val):
    # Aktuelle Werte der beiden Slider auslesen
    sample_size = int(slider_size.val)
    iterations = int(slider_iter.val)

    datasets = [
        (extracted, "1. ALLE Antworten"),
        (q1_data, "2. ERSTES Viertel"),
        (q2_data, "3. ZWEITES Viertel"),
        (q4_data, "4. LETZTES Viertel"),
    ]

    for i, (full_data, base_title) in enumerate(datasets):
        ax = axes[i]

        # Wenn der Abschnitt kleiner ist als die gewünschte Stichprobengröße,
        # begrenzen wir die maximale Größe für diesen spezifischen Plot.
        current_size = min(sample_size, len(full_data))

        # K-malige Ziehung einer Stichprobe vom Umfang N
        combined_sample = []
        for _ in range(iterations):
            if current_size > 0:
                # random.choices erlaubt das Ziehen mit Zurücklegen für die Iterationen
                combined_sample.extend(random.choices(full_data, k=current_size))

        total_sampled = len(combined_sample)

        # Häufigkeiten berechnen
        counts = Counter(combined_sample)
        percentages = [
            (counts[cat] / total_sampled) * 100 if total_sampled > 0 else 0
            for cat in categories
        ]

        # Diagramm-Balken aktualisieren
        for bar, new_height in zip(bar_containers[i], percentages):
            bar.set_height(new_height)

        # Titel aktualisieren (zeigt die effektive Gesamtanzahl ausgewerteter Daten)
        ax.set_title(
            f"{base_title}\nGesamt-N = {total_sampled} ({iterations}x{current_size})",
            fontsize=10,
            fontweight="bold",
            pad=10,
        )

        # Prozentzahlen über den Balken aktualisieren
        for txt in text_elements[i]:
            txt.remove()
        text_elements[i].clear()

        for bar in bar_containers[i]:
            height = bar.get_height()
            txt = ax.annotate(
                f"{height:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )
            text_elements[i].append(txt)

    fig.canvas.draw_idle()


# --- 4. INITIALISIERUNG DER DIAGRAMME ---
for i, _ in enumerate(axes):
    ax = axes[i]
    # Platzhalter-Balken erzeugen
    bars = ax.bar(categories, [0, 0, 0, 0], color=colors[i], edgecolor="black")
    bar_containers.append(bars)
    text_elements.append([])

    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=12)

# --- 5. ZWEI SLIDER HINZUFÜGEN ---
# Slider 1: Absolute Stichprobengröße (10 bis 20)
ax_size = plt.axes([0.25, 0.13, 0.5, 0.03])
slider_size = Slider(
    ax=ax_size,
    label="Stichprobengröße (n) ",
    valmin=10,
    valmax=20,
    valinit=15,
    valfmt="%1.0f",
    color="purple",
)

# Slider 2: Anzahl der Ziehungen / Wiederholungen (1 bis 20)
ax_iter = plt.axes([0.25, 0.06, 0.5, 0.03])
slider_iter = Slider(
    ax=ax_iter,
    label="Anzahl Ziehungen (k) ",
    valmin=1,
    valmax=20,
    valinit=1,
    valfmt="%1.0f",
    color="orange",
)

# Beide Slider mit der Update-Funktion verknüpfen
slider_size.on_changed(update)
slider_iter.on_changed(update)

# Initialen Aufruf erzwingen, um Diagramme zu füllen
update(None)

plt.suptitle(
    "Kumulierter Stichproben-Vergleich",
    fontsize=14,
    fontweight="bold",
    y=0.98,
)
plt.show()
