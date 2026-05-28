# 7_Quiz-Branding-by-Interaction.py
from collections import Counter
import math
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# --- 1. DATEN AUS TEXTDATEI EINLESEN (Aufgestockt auf 160) ---
dateiname = "antworten.txt"
raw_answers = []

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as file:
        raw_answers = [line.strip() for line in file if line.strip()]
else:
    print(f"Datei '{dateiname}' nicht gefunden. Generiere 160 didaktische Demo-Antworten...")
    # 160 Antworten: Viertel 1-3 sauber gleichverteilt, Viertel 4 massiver b-Überhang
    raw_answers = (
        [f"A_{str(i).zfill(3)}.a" for i in range(1, 11)] +
        [f"A_{str(i).zfill(3)}.b" for i in range(11, 21)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(21, 31)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(31, 41)] + # V1: 1-40
        [f"A_{str(i).zfill(3)}.a" for i in range(41, 51)] +
        [f"A_{str(i).zfill(3)}.b" for i in range(51, 61)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(61, 71)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(71, 81)] + # V2: 41-80
        [f"A_{str(i).zfill(3)}.a" for i in range(81, 91)] +
        [f"A_{str(i).zfill(3)}.b" for i in range(91, 101)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(101, 111)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(111, 122)] + # V3: 81-120
        [f"A_{str(i).zfill(3)}.b" for i in range(121, 151)] + # V4: Extrem viel b!
        [f"A_{str(i).zfill(3)}.a" for i in range(151, 155)] +
        [f"A_{str(i).zfill(3)}.c" for i in range(155, 158)] +
        [f"A_{str(i).zfill(3)}.d" for i in range(158, 161)]   
    )

# Parsen der Daten: Liste von Dictionaries für schnellen Index-Zugriff
parsed_data = []
for line in raw_answers:
    if "." in line and "_" in line:
        parts = line.split(".")
        letter = parts[-1]
        num = parts[0].split("_")[-1]
        parsed_data.append({"num": num, "letter": letter})
    elif "." in line:
        parsed_data.append({"num": "???", "letter": line.split(".")[-1]})

# Sicherstellen, dass wir genau 160 Elemente für das Grid haben (Kappen oder Auffüllen)
while len(parsed_data) < 160:
    parsed_data.append({"num": "---", "letter": "a"})
parsed_data = parsed_data[:160]

# --- 2. SETUP FÜR DIE INTERAKTIVE MATRIX ---
# Zustandsspeicher: Welche der 160 Fragen sind aktiv? (True = Ausgewählt / Schwarz)
matrix_state = [False] * 160

# --- 3. GRAFISCHE OBERFLÄCHE (MATPLOTLIB) ---
fig = plt.figure(figsize=(16, 8))
# Oberer Bereich für die 4 Histogramme, unterer Bereich für das Kästchenfeld
plt.subplots_adjust(bottom=0.45, top=0.92, hspace=0.4)

# 4 Achsen für Histogramme manuell anlegen
axes = [fig.add_axes([0.06 + i*0.23, 0.52, 0.18, 0.35]) for i in range(4)]
categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]

bar_containers = []
text_elements = []

# Histogramme initialisieren
for i, ax in enumerate(axes):
    bars = ax.bar(categories, [0, 0, 0, 0], color=colors[i], edgecolor="black")
    bar_containers.append(bars)
    text_elements.append([])
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=11)

# --- 4. INTERAKTIVES UPDATE NACH KLICK ---
def update_plots():
    # Aufteilung der aktiven Daten in die 4 Viertel
    v1_selected = [parsed_data[idx]["letter"] for idx in range(0, 40) if matrix_state[idx]]
    v2_selected = [parsed_data[idx]["letter"] for idx in range(40, 80) if matrix_state[idx]]
    v3_selected = [parsed_data[idx]["letter"] for idx in range(80, 120) if matrix_state[idx]]
    v4_selected = [parsed_data[idx]["letter"] for idx in range(120, 160) if matrix_state[idx]]
    all_selected = v1_selected + v2_selected + v3_selected + v4_selected

    datasets = [
        (all_selected, "1. DEINE Auswahl (Gesamt)"),
        (v1_selected, "2. ERSTES Viertel (1-40)"),
        (v2_selected, "3. ZWEITES Viertel (41-80)"),
        (v3_selected, "4. DRITTES Viertel (81-120)"),
    ]
    # Korrektur des Titels/Inhalts für das 4. Diagramm auf das 4. Viertel
    datasets[3] = (v4_selected, "5. LETZTES Viertel (121-160)")
    # Wir passen das erste Diagramm an, sodass es alle ausgewählten zeigt, und daneben V1, V2, V4
    datasets = [
        (all_selected, "1. DEINE Auswahl (Gesamt)"),
        (v1_selected, "2. ERSTES Viertel (1-40)"),
        (v2_selected, "3. ZWEITES Viertel (41-80)"),
        (v4_selected, "4. LETZTES Viertel (121-160)"),
    ]

    for i, (selected_letters, base_title) in enumerate(datasets):
        ax = axes[i]
        n_selected = len(selected_letters)
        counts = Counter(selected_letters)
        
        percentages = [
            (counts[cat] / n_selected) * 100 if n_selected > 0 else 0 
            for cat in categories
        ]

        # Balken aktualisieren
        for bar, new_height in zip(bar_containers[i], percentages):
            bar.set_height(new_height)

        ax.set_title(f"{base_title}\n(Markiert n = {n_selected})", fontsize=10, fontweight="bold")

        # Prozent-Texte aktualisieren
        for txt in text_elements[i]:
            txt.remove()
        text_elements[i].clear()

        for bar in bar_containers[i]:
            height = bar.get_height()
            if n_selected > 0:
                txt = ax.annotate(f"{height:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, height),
                                  xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)
                text_elements[i].append(txt)

    fig.canvas.draw_idle()

# --- 5. MATRIX-BUTTONS GENERIEREN ---
button_objects = [] # Wichtig, um Referenzen im Speicher zu behalten!

# Erstelle ein 4x40 Grid aus kleinen Matplotlib-Buttons
# x-Bereich von 0.06 bis 0.94 nutzen
grid_left = 0.06
grid_width = 0.88
box_w = grid_width / 40
box_h = 0.04

def create_toggle_callback(index, btn):
    def callback(event):
        # Zustand invertieren
        matrix_state[index] = not matrix_state[index]
        if matrix_state[index]:
            btn.ax.set_facecolor("#2C3E50") # Nachgeschwärzt bei Aktivierung
            btn.label.set_color("white")
        else:
            btn.ax.set_facecolor("#EAEDED") # Standard Grau-Weiß
            btn.label.set_color("black")
        update_plots()
    return callback

# Zeichne das Kästchenfeld (4 Reihen, 40 Spalten)
for row in range(4):
    y_pos = 0.32 - (row * 0.06) # Vertikale Position der Reihe
    # Beschriftung für das Viertel links neben die Reihe setzen
    fig.text(0.01, y_pos + 0.01, f"Viertel {row+1}:", fontsize=10, fontweight="bold")
    
    for col in range(40):
        data_idx = (row * 40) + col
        fr_num = parsed_data[data_idx]["num"]
        
        # Koordinaten für das einzelne Kästchen berechnen
        x_pos = grid_left + (col * box_w)
        ax_box = plt.axes([x_pos, y_pos, box_w - 0.002, box_h])
        
        # Button erstellen (zeigt gekürzte Fragennummer)
        btn = Button(ax=ax_box, label=str(int(fr_num)), color="#EAEDED", hovercolor="#BDC3C7")
        btn.label.set_fontsize(7)
        
        # Event verknüpfen via Closure
        btn.on_clicked(create_toggle_callback(data_idx, btn))
        button_objects.append(btn)

# --- 6. BERICHT SPEICHERN BUTTON ---
def save_report(event):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ausgabe_name = f"branding_test_{timestamp}.png"
    # Speicher-Button kurz unsichtbar machen
    ax_save_btn.set_visible(False)
    plt.savefig(ausgabe_name, dpi=300, bbox_inches='tight')
    ax_save_btn.set_visible(True)
    fig.canvas.draw()
    print(f"[ERFOLG] Branding gespeichert: {ausgabe_name}")

ax_save_btn = plt.axes([0.44, 0.03, 0.12, 0.04])
btn_save = Button(ax=ax_save_btn, label="Exp-Bild speichern", color="#27AE60", hovercolor="#2ECC71")
btn_save.label.set_color("white")
btn_save.label.set_weight("bold")
btn_save.on_clicked(save_report)

# Titel und initialer Plot-Aufruf
plt.suptitle("Interaktives Pseudo-Quiz: experimentelle Antwort-Verteilung", fontsize=14, fontweight="bold", y=0.97)
update_plots()
plt.show()
