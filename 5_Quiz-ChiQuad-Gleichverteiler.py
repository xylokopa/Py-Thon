# 5_Quiz-ChiQuad-Gleichverteiler.py
from collections import Counter
import math
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- 1. DATEN AUS TEXTDATEI EINLESEN ---
dateiname = "antworten.txt"
raw_answers = []

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as file:
        raw_answers = [line.strip() for line in file if line.strip()]
else:
    print(f"Fehler: Die Datei '{dateiname}' wurde nicht gefunden. Generiere Demo-Daten...")
    # Demo-Daten mit manipuliertem b-Trend im letzten Viertel
    raw_answers = (
        [f"A_{str(i).zfill(3)}.a" for i in range(1, 21)] +
        [f"A_{str(i).zfill(3)}.b" for i in range(21, 41)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(41, 61)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(61, 81)] + # 1. & 2. Viertel (Gleichverteilt)
        [f"A_{str(i).zfill(3)}.b" for i in range(81, 141)] +
        [f"A_{str(i).zfill(3)}.a" for i in range(141, 146)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(146, 151)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(151, 156)]   # Letztes Viertel (Massiver b-Überhang)
    )

# Parsen der Daten in Tuples: (Fragen-Nummer, Antwort-Buchstabe)
# Beispiel: "A_001.b" -> ("001", "b")
parsed_data = []
for line in raw_answers:
    if "." in line and "_" in line:
        parts = line.split(".")
        letter = parts[-1]
        num = parts[0].split("_")[-1]
        parsed_data.append((num, letter))
    elif "." in line: # Fallback falls kein Unterstrich existiert
        parts = line.split(".")
        letter = parts[-1]
        parsed_data.append(("???", letter))

total_count = len(parsed_data)
if total_count < 20:
    print("Die Datei enthält zu wenige Daten für diese Auswertung.")
    exit()

# Daten in Abschnitte unterteilen
quarter_size = total_count / 4
q1_data = parsed_data[:math.ceil(quarter_size)]
q2_data = parsed_data[math.ceil(quarter_size):math.floor(quarter_size * 2)]
q4_data = parsed_data[math.ceil(quarter_size * 3):]

# --- 2. HILFSFUNKTION: ABWEICHUNG ZUR GLEICHVERTEILUNG BERECHNEN ---
def berechne_ungleichgewicht(sample):
    """ Berechnet die quadratische Abweichung zur perfekten Gleichverteilung """
    counts = Counter([item[1] for item in sample])
    n = len(sample)
    ideal = n / 4.0
    
    quadratische_abweichung = 0
    for cat in ["a", "b", "c", "d"]:
        quadratische_abweichung += (counts[cat] - ideal) ** 2
    return quadratische_abweichung

# --- 3. GRAFISCHE OBERFLÄCHE EINRICHTEN ---
fig, axes = plt.subplots(1, 4, figsize=(16, 7), sharey=True)
# Platz nach unten für Slider, Button UND Text-Ausgabe vergrößert
plt.subplots_adjust(bottom=0.42)  

categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]

bar_containers = []
text_elements = []
info_texts = [] # Für die Anzeige der Fragen-Nummern unter den Plots

# --- 4. INTERAKTIVE UPDATE-FUNKTION ---
def update(val):
    sample_size = int(slider_size.val)
    iterations = int(slider_iter.val)

    datasets = [
        (parsed_data, "1. ALLE Antworten"),
        (q1_data, "2. ERSTES Viertel"),
        (q2_data, "3. ZWEITES Viertel"),
        (q4_data, "4. LETZTES Viertel"),
    ]

    for i, (full_data, base_title) in enumerate(datasets):
        ax = axes[i]
        current_size = min(sample_size, len(full_data))

        best_sample = None
        best_score = float('inf')
        all_sampled_letters = []

        # Wir simulieren k Ziehungen und suchen die "beste" (fairste) Stichprobe heraus
        for _ in range(iterations):
            if current_size > 0:
                # Ziehen ohne Zurücklegen pro Einzeldurchgang, um echte Kombis zu simulieren
                # (Falls current_size > len(full_data), nehmen wir max. verfügbare Menge)
                k_size = min(current_size, len(full_data))
                current_sample = random.sample(full_data, k=k_size)
                
                # Alle gezogenen Buchstaben für das Gesamt-Histogramm sammeln
                all_sampled_letters.extend([item[1] for item in current_sample])
                
                # Prüfen, ob diese Stichprobe der Gleichverteilung am nächsten liegt
                score = berechne_ungleichgewicht(current_sample)
                if score < best_score:
                    best_score = score
                    best_sample = current_sample

        total_sampled = len(all_sampled_letters)
        counts = Counter(all_sampled_letters)
        percentages = [
            (counts[cat] / total_sampled) * 100 if total_sampled > 0 else 0 
            for cat in categories
        ]

        # 1. Histogramm-Balken aktualisieren
        for bar, new_height in zip(bar_containers[i], percentages):
            bar.set_height(new_height)

        # 2. Titel aktualisieren
        ax.set_title(
            f"{base_title}\nGesamt-N = {total_sampled} ({iterations}x{current_size})",
            fontsize=10, fontweight="bold", pad=10
        )

        # 3. Prozentzahlen über den Balken aktualisieren
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

        # 4. Ausgabe-Text für die "fairste" Stichprobe aktualisieren
        if best_sample:
            # Sortiere die Fragenummern aufsteigend für bessere Lesbarkeit
            best_numbers = sorted([item[0] for item in best_sample])
            # Formatierung: Max 5 Nummern pro Zeile, damit es ins Layout passt
            chunks = [best_numbers[x:x+5] for x in range(0, len(best_numbers), 5)]
            formatted_text = "\n".join(["/".join(chunk) for chunk in chunks])
        else:
            formatted_text = "Keine Daten"
            
        info_texts[i].set_text(f"Beste stochastische\nKombination (n={current_size}):\n{formatted_text}")

    fig.canvas.draw_idle()

# --- 5. SPEICHER-FUNKTION ---
def save_report(event):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ausgabe_name = f"exp-verteilung_{timestamp}.png"
    
    ax_size.set_visible(False)
    ax_iter.set_visible(False)
    ax_button.set_visible(False)
    
    plt.savefig(ausgabe_name, dpi=300, bbox_inches='tight')
    print(f"[ERFOLG] experiment gespeichert unter: {ausgabe_name}")
    
    ax_size.set_visible(True)
    ax_iter.set_visible(True)
    ax_button.set_visible(True)
    fig.canvas.draw()

# --- 6. INITIALISIERUNG DER DIAGRAMME UND TEXTFELDER ---
for i, _ in enumerate(axes):
    ax = axes[i]
    bars = ax.bar(categories, [0,0,0,0], color=colors[i], edgecolor="black")
    bar_containers.append(bars)
    text_elements.append([])
    
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=12)
        
    # Textfeld unterhalb des jeweiligen Plots platzieren
    # Nutzen von relativen Achsen-Koordinaten (y < 0 platziert Text unter die X-Achse)
    t = ax.text(0.5, -0.22, "", transform=ax.transAxes, ha="center", va="top",
                fontsize=9, color="#2C3E50", style='italic',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8F9F9", edgecolor="#BDC3C7"))
    info_texts.append(t)

# --- 7. STEUERELEMENTE (SLIDER & BUTTON) PLATZIEREN ---
# Weiter nach unten verschoben, um Kollisionen mit dem Text zu vermeiden
ax_size = plt.axes([0.25, 0.12, 0.45, 0.03])
slider_size = Slider(ax=ax_size, label="Stichprobengröße (n)  ", valmin=10, valmax=20, valinit=15, valfmt="%1.0f", color="purple")

ax_iter = plt.axes([0.25, 0.05, 0.45, 0.03])
slider_iter = Slider(ax=ax_iter, label="Anzahl Ziehungen (k)  ", valmin=1, valmax=20, valinit=5, valfmt="%1.0f", color="orange")

slider_size.on_changed(update)
slider_iter.on_changed(update)

ax_button = plt.axes([0.78, 0.05, 0.12, 0.10])
btn_save = Button(ax=ax_button, label="Näherung\nspeichern", color="#27AE60", hovercolor="#2ECC71") # Grün für Ehrenrettung
btn_save.label.set_color("white")
btn_save.label.set_weight("bold")
btn_save.on_clicked(save_report)

# Startkonfiguration laden
update(None)

plt.suptitle("Quiz-im-Vierteltakt: Stochastische Näherung lokaler Gleichverteilungen", fontsize=14, fontweight="bold", y=0.98)
plt.show()
