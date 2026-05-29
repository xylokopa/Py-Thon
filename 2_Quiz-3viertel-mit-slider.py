# 2_Quiz-3viertel-mit-slider.py 27.05.2026 
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
    # Demo-Daten mit simuliertem "b-Trend" 
    answers = (
        ["A.a"] * 15
        + ["A.b"] * 15
        + ["A.c"] * 15
        + ["A.d"] * 15  # 1. Viertel: Sauber
        + ["A.a"] * 15
        + ["A.b"] * 15
        + ["A.c"] * 15
        + ["A.d"] * 15  # 2. Viertel: Sauber
        + ["A.a"] * 5
        + ["A.b"] * 45
        + ["A.c"] * 5
        + ["A.d"] * 5  # Letztes Viertel: b-Überhang
    )

# Antworten extrahieren
extracted = [line.split(".")[-1] for line in answers if "." in line]
total_count = len(extracted)

if total_count < 10:
    print("Zu wenige Daten für eine sinnvolle Stichprobenanalyse.")
    exit()

# Daten in Abschnitte unterteilen
quarter_size = total_count / 4
q1_data = extracted[: math.ceil(quarter_size)]
q2_data = extracted[math.ceil(quarter_size) : math.floor(quarter_size * 2)]
q4_data = extracted[math.ceil(quarter_size * 3) :]

# --- 2. GRAFISCHE OBERFLÄCHE (MATPLOTLIB) EINRICHTEN ---
# Platz nach unten für den Slider lassen via 'subplots_adjust'
fig, axes = plt.subplots(1, 4, figsize=(15, 6), sharey=True)
plt.subplots_adjust(bottom=0.25)  # Schafft Platz für den Slider unten

categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]

# Globale Listen für den Zugriff in der Update-Funktion
bar_containers = []
text_elements = []


# --- 3. UPDATE-FUNKTION FÜR DEN SLIDER ---
def update(val):
    # Prozentsatz vom Slider holen (0.1 bis 1.0)
    percentage = val / 100.0

    # Datenquellen definieren
    datasets = [
        (extracted, "1. alle Antworten"),
        (q1_data, "2. erstes Viertel"),
        (q2_data, "3. zweites Viertel"),
        (q4_data, "4. letztes Viertel"),
    ]

    for i, (full_data, base_title) in enumerate(datasets):
        ax = axes[i]

        # Berechne den Stichprobenumfang (mindestens 1 Element)
        sample_size = max(1, round(len(full_data) * percentage))

        # ZUFÄLLIGE STICHPROBE ZIEHEN (at Random)
        sample_data = random.sample(full_data, sample_size)

        # Häufigkeiten berechnen
        counts = Counter(sample_data)
        percentages = [
            (counts[cat] / sample_size) * 100 if sample_size > 0 else 0
            for cat in categories
        ]

        # Diagramm-Balken aktualisieren
        for bar, new_height in zip(bar_containers[i], percentages):
            bar.set_height(new_height)

        # Titel mit aktueller Stichprobengröße aktualisieren
        ax.set_title(
            f"{base_title}\n(Stichprobe n = {sample_size})",
            fontsize=11,
            fontweight="bold",
            pad=10,
        )

        # Prozentzahlen über den Balken aktualisieren
        # Erst alte Texte löschen
        for txt in text_elements[i]:
            txt.remove()
        text_elements[i].clear()

        # Neue Texte zeichnen
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

    # Zeichne das Fenster neu
    fig.canvas.draw_idle()


# --- 4. INITIALISIERUNG DER DIAGRAMME ---
# Erster Durchlauf mit 100% als Standardwert
datasets_init = [
    (extracted, "1. alle Antworten"),
    (q1_data, "2. erstes Viertel"),
    (q2_data, "3. zweites Viertel"),
    (q4_data, "4. letztes Viertel"),
]

for i, (data, title) in enumerate(datasets_init):
    ax = axes[i]
    counts = Counter(data)
    sub_total = len(data)
    percentages = [
        (counts[cat] / sub_total) * 100 if sub_total > 0 else 0 for cat in categories
    ]

    bars = ax.bar(categories, percentages, color=colors[i], edgecolor="black")
    bar_containers.append(bars)
    text_elements.append([])  # Platzhalter für Texte

    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=12)

# --- 5. SLIDER HINZUFÜGEN UND VERKNÜPFEN ---
# Position des Slider-Bereichs: [links, unten, breite, höhe]
slider_ax = plt.axes([0.25, 0.08, 0.5, 0.04])
stichproben_slider = Slider(
    ax=slider_ax,
    label="Stichprobenumfang (%) ",
    valmin=10,
    valmax=100,
    valinit=100,
    valfmt="%1.0f%%",
    color="seagreen",
)

# Auf Slider-Bewegung reagieren
stichproben_slider.on_changed(update)

# Einmalig aufrufen, um die Prozent-Labels beim Start korrekt zu setzen
update(100)

plt.suptitle(
    "Quiz-im-3Vierteltakt",
    fontsize=12,
    fontweight="bold",
    y=0.98,
)
plt.show()
