# 4_Quiz-viertelung-mit-bild.py
from collections import Counter
import math
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- 1. DATEN AUS TEXTDATEI EINLESEN ---
dateiname = "antworten.txt"
answers = []

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as file:
        answers = [line.strip() for line in file if line.strip()]
else:
    print(f"Fehler: Die Datei '{dateiname}' wurde nicht gefunden. Generiere Demo-Daten...")
    # Demo-Daten mit Exp-b-Trend im letzten Viertel
    answers = (
        ["A.a"] * 20 + ["A.b"] * 20 + ["A.c"] * 20 + ["A.d"] * 20  # 1. Viertel
        + ["A.a"] * 20 + ["A.b"] * 20 + ["A.c"] * 20 + ["A.d"] * 20  # 2. Viertel
        + ["A.a"] * 5 + ["A.b"] * 65 + ["A.c"] * 5 + ["A.d"] * 5   # Letztes Viertel
    )

extracted = [line.split(".")[-1] for line in answers if "." in line]
total_count = len(extracted)

if total_count < 20:
    print("Die Datei enthält zu wenige Daten für diese Auswertung.")
    exit()

# Daten in Abschnitte unterteilen
quarter_size = total_count / 4
q1_data = extracted[:math.ceil(quarter_size)]
q2_data = extracted[math.ceil(quarter_size):math.floor(quarter_size * 2)]
q4_data = extracted[math.ceil(quarter_size * 3):]

# --- 2. GRAFISCHE OBERFLÄCHE (MATPLOTLIB) EINRICHTEN ---
fig, axes = plt.subplots(1, 4, figsize=(15, 6), sharey=True)
plt.subplots_adjust(bottom=0.35)  # Platz für Slider und Button vergrößert

categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]

bar_containers = []
text_elements = []

# --- 3. INTERAKTIVE UPDATE-FUNKTION ---
def update(val):
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
        current_size = min(sample_size, len(full_data))

        combined_sample = []
        for _ in range(iterations):
            if current_size > 0:
                combined_sample.extend(random.choices(full_data, k=current_size))

        total_sampled = len(combined_sample)
        counts = Counter(combined_sample)
        percentages = [
            (counts[cat] / total_sampled) * 100 if total_sampled > 0 else 0 
            for cat in categories
        ]

        for bar, new_height in zip(bar_containers[i], percentages):
            bar.set_height(new_height)

        ax.set_title(
            f"{base_title}\nGesamt-N = {total_sampled} ({iterations}x{current_size})",
            fontsize=10, fontweight="bold", pad=10
        )

        for txt in text_elements[i]:
            txt.remove()
        text_elements[i].clear()

        for bar in bar_containers[i]:
            height = bar.get_height()
            txt = ax.annotate(
                f"{height:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=9
            )
            text_elements[i].append(txt)

    fig.canvas.draw_idle()

# --- 4. SPEICHER-FUNKTION (BUTTON ACTION) ---
def save_report(event):
    # Generiere einen Zeitstempel für den Dateinamen, um Überschreiben zu verhindern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ausgabe_name = f"Grafik_{timestamp}.png"
    
    # Vorübergehend die Steuerelemente aus Grafik ausblenden
    ax_size.set_visible(False)
    ax_iter.set_visible(False)
    ax_button.set_visible(False)
    
    # Bild mit hoher Qualität exportieren (300 DPI)
    plt.savefig(ausgabe_name, dpi=300, bbox_inches='tight')
    print(f"[ERFOLG] Bericht erfolgreich gespeichert unter: {ausgabe_name}")
    
    # Steuerelemente wieder einblenden
    ax_size.set_visible(True)
    ax_iter.set_visible(True)
    ax_button.set_visible(True)
    fig.canvas.draw()

# --- 5. INITIALISIERUNG DER DIAGRAMME ---
for i, _ in enumerate(axes):
    ax = axes[i]
    bars = ax.bar(categories, [0, 0, 0, 0], color=colors[i], edgecolor="black")
    bar_containers.append(bars)
    text_elements.append([])
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=12)

# --- 6. STEUERELEMENTE (SLIDER & BUTTON) PLATZIEREN ---
# Slider 1: Stichprobengröße (n)
ax_size = plt.axes([0.25, 0.16, 0.45, 0.03])
slider_size = Slider(ax=ax_size, label="Stichprobengröße (n)  ", valmin=10, valmax=20, valinit=15, valfmt="%1.0f", color="purple")

# Slider 2: Anzahl Ziehungen (k)
ax_iter = plt.axes([0.25, 0.08, 0.45, 0.03])
slider_iter = Slider(ax=ax_iter, label="Anzahl Ziehungen (k)  ", valmin=1, valmax=20, valinit=1, valfmt="%1.0f", color="orange")

# Verknüpfungen für Slider
slider_size.on_changed(update)
slider_iter.on_changed(update)

# Button: Bericht als PNG exportieren
ax_button = plt.axes([0.78, 0.08, 0.12, 0.11]) # Rechter Hand neben den Slidern platziert
btn_save = Button(ax=ax_button, label="Grafik\nspeichern", color="#F0FFFF", hovercolor="#F00FFF")
btn_save.label.set_color("white")
btn_save.label.set_weight("bold")
btn_save.on_clicked(save_report)

# Startkonfiguration laden
update(None)

plt.suptitle("Kumulierte Stichproben-Analyse", fontsize=14, fontweight="bold", y=0.98)
plt.show()
