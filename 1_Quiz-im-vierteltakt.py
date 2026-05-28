# 1_Quiz-im-Vierteltakt.py 28.05.2026 by R.Wurdack & Google-Gemini
from collections import Counter
import math
import os
import matplotlib.pyplot as plt


# --- 1. DATEN AUS TEXTDATEI EINLESEN ---
dateiname = "antworten.txt"
answers = []

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as file:
        answers = [line.strip() for line in file if line.strip()]
else:
    print(
        f"Fehler: Die Datei '{dateiname}' wurde nicht gefunden. Bitte erstelle sie."
    )
    # Demo-Daten mit einer künstlichen Verschiebung (z.B. viel 'b' am Anfang, viel 'c' am Ende)
    answers = (
        ["A.b"] * 20
        + ["A.a"] * 5
        + ["A.c"] * 5
        + ["A.d"] * 5  # 1. Viertel (Viel b)
        + ["A.a"] * 10
        + ["A.b"] * 10
        + ["A.c"] * 10
        + ["A.d"] * 5  # 2. Viertel (Gleichverteilt)
        + ["A.c"] * 25
        + ["A.a"] * 5
        + ["A.b"] * 5
        + ["A.d"] * 5  # Letztes Viertel (Viel c)
    )

# Buchstaben am Ende extrahieren
extracted = [line.split(".")[-1] for line in answers if "." in line]
total_count = len(extracted)

if total_count < 4:
    print("Nicht genügend Daten für eine Viertel-Aufteilung vorhanden.")
    exit()

# --- 2. DATEN IN VIERTEL AUFTEILEN ---
# Berechnung der exakten Trennpunkte
quarter_size = total_count / 4

# Die drei gewünschten Teilbereiche extrahieren
q1_data = extracted[: math.ceil(quarter_size)]
q2_data = extracted[math.ceil(quarter_size) : math.floor(quarter_size * 2)]
# Hinweis: "Letztes Viertel" entspricht dem 4. Viertel (von 75% bis zum Ende)
q4_data = extracted[math.ceil(quarter_size * 3) :]

# Liste der Datensätze und ihre Titel
datasets = [
    (extracted, f"1. ALLE Antworten\n(n = {len(extracted)})"),
    (q1_data, f"2. ERSTES Viertel\n(n = {len(q1_data)})"),
    (q2_data, f"3. ZWEITES Viertel\n(n = {len(q2_data)})"),
    (q4_data, f"4. LETZTES Viertel\n(n = {len(q4_data)})"),
]

# --- 3. MATPLOTLIB PROZENT-HISTOGRAMME ---
# Ein Fenster mit 1 Zeile und 4 Spalten erzeugen
fig, axes = plt.subplots(1, 4, figsize=(15, 5), sharey=True)
categories = ["a", "b", "c", "d"]
colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]  # Unterschiedliche Farben

for i, (data, title) in enumerate(datasets):
    ax = axes[i]
    counts = Counter(data)
    sub_total = len(data)

    # Prozentwerte berechnen
    percentages = [
        (counts[cat] / sub_total) * 100 if sub_total > 0 else 0
        for cat in categories
    ]

    # Balken zeichnen
    bars = ax.bar(categories, percentages, color=colors[i], edgecolor="black")

    # Layout und Beschriftungen
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    if i == 0:
        ax.set_ylabel("Anteil (%)", fontsize=12)

    # Prozentzahlen über die Balken schreiben
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

# Gesamtes Fenster optimieren
plt.suptitle(
    "Analyse auf Unregelmäßigkeiten / Manipulation",
    fontsize=14,
    fontweight="bold",
    y=1.05,
)
plt.tight_layout()
plt.show()
