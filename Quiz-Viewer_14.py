# Quiz-Viewer_14.py 20-05-26 Idee R.Wurdack Script Google-Gemini
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
#-------------------Start-Bedingungen----------------------------
load_index = 0      # 0: Learn-Modus mit Loesung  1: Quiz-Modus
startzeile = 11     # Verschiebbarer Zeiger auf die erste Frage 
#-------------------Quiz-Ablauf---------------------------------
def load_data(fragen_file, antworten_file,start_zeile):
    questions = []
    #start_zeile = 1
    try:
        with open(fragen_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            lines = lines[(start_zeile-1)*12:]            
        for i in range(0, len(lines), 12):                      # 5
            questions.append(lines[i:i+12])                     # 5
        with open(antworten_file, 'r', encoding='utf-8') as f:
            answers = [line.strip() for line in f if line.strip()]
            answers = answers[(start_zeile-1):]
    except: return []
    return [{"q_lines": q, "a": a, "id": i} for i, (q, a) in enumerate(zip(questions, answers))]

class QuizViewer:
    def __init__(self, all_data):
        self.all_data = all_data
        self.num_to_pick = min(len(all_data), 155)      # 152
        self.level = 0 # 0,1=Linear, 2=Zufall, 3=Streng, 4=Kein Zurück!
        
        self.index = 0
        self.guess = "?"
        self.show_answer = False
        self.score = 0
        self.answered_ids = set()
        self.current_pool = []

        self.fig, self.ax = plt.subplots(figsize=(11, 5.5)) # 11,8
        plt.subplots_adjust(left=0.2, bottom=0.25)
        self.ax.axis('off')

        self.txt_q = self.ax.text(0.05, 0.99, "", va='top', fontsize=11, family='monospace')
        self.txt_feedback1 = self.ax.text(0.75, 0.01, "", va='top', fontsize=12, fontweight='bold')
        self.txt_feedback2 = self.ax.text(0.75, 0.99, "", va='top', fontsize=12, fontweight='bold')       
        self.txt_score = self.ax.text(0.05, 0.00, "", va='top', fontsize=13, color='darkblue', fontweight='black')

        # Antwort-Buttons
        self.btn_choices = []
        for i, label in enumerate(['a', 'b', 'c', 'd']):
            ax_c = plt.axes([0.10, 0.675 - (i * 0.06), 0.04, 0.05]) # 0.05
            btn = Button(ax_c, label)
            btn.on_clicked(lambda e, l=label: self.make_guess(l))
            self.btn_choices.append(btn)

        # Navigation mit Buttons
        self.btn_prev = Button(plt.axes([0.05, 0.50, 0.04, 0.22]), '<<')   
        self.btn_num = Button(plt.axes([0.05, 0.40, 0.14, 0.06]), f'Anzahl: {self.num_to_pick}')
        self.lvl_txt = ["tafel","geloest","zufall","streng","kein zurueck"]
        self.btn_lvl = Button(plt.axes([0.05, 0.33, 0.14, 0.06]), f'Modus:{self.lvl_txt[self.level]}')

        self.btn_next = Button(plt.axes([0.15, 0.50, 0.04, 0.22]), '>>')

        self.btn_prev.on_clicked(lambda x: self.move(-1))
        self.btn_next.on_clicked(lambda x: self.move(1))
        self.btn_num.on_clicked(self.toggle_num)
        self.btn_lvl.on_clicked(self.toggle_level)

        self.reset_quiz()
        plt.show()

    def toggle_num(self, event):
        self.num_to_pick = (self.num_to_pick % len(self.all_data)) + 1
        self.btn_num.label.set_text(f'Anzahl: {self.num_to_pick}')
        self.reset_quiz()

    def toggle_level(self, event):
        # Zahlenring 0,1 -> 2 -> 3 -> 4 -> 0
        # self.lvl_txt = ["geloest","01","02","03","04"]
        self.level = (self.level + 1) % 5
        self.btn_lvl.label.set_text(f'Modus:{self.lvl_txt[self.level]}')
        self.reset_quiz()

    def reset_quiz(self):
        self.score = 0
        self.answered_ids = set()
        self.index = 0
        
        if self.level == 0:
            self.current_pool = self.all_data[:self.num_to_pick]
            self.txt_q.set_fontsize(15)
            # 0. GROSSSCHRIFT Redraw the canvas to see the update
            self.ax.figure.canvas.draw_idle()            
        if self.level == 1:
            self.current_pool = self.all_data[:self.num_to_pick]
            self.txt_q.set_fontsize(11)
            # 1. KLEINSCHRIFT Redraw the canvas to see the update
            self.ax.figure.canvas.draw_idle()            
        elif self.level == 2:
            self.current_pool = random.sample(self.all_data, self.num_to_pick)
        elif self.level >= 3:
            # Stufe 3 und 4 nutzen beide den strengen Zufall (shuffled)
            temp_pool = list(self.all_data)
            random.shuffle(temp_pool)
            self.current_pool = temp_pool[:self.num_to_pick]
            
        self.update_display()

    def make_guess(self, label):
        if not self.show_answer:
            item = self.current_pool[self.index]
            correct = item['a'].split('.')[-1].strip().lower()
            if label.lower() == correct and item['id'] not in self.answered_ids:
                self.score += 1
                self.answered_ids.add(item['id'])
            self.guess, self.show_answer = label, True
            self.update_display()

    def update_display(self):
        item = self.current_pool[self.index]
        lvl_names = ["Tafel_0","Geloest_1", "Zufall_2", "Streng_3", "KEIN ZURUECK!_4"]
        mode_text = lvl_names[self.level]
        
        self.txt_q.set_text(f"Modus: {mode_text} | Frage {self.index+1}/{len(self.current_pool)}\n\n" + "\n".join(item['q_lines']))
        self.txt_score.set_text(f"ERGEBNIS: {self.score} von {len(self.current_pool)} richtig")
        
        # Zurück-Button ausgrauen/sperren in Stufe 4
        if self.level == 4:
            self.btn_prev.ax.set_facecolor('gray')
            self.btn_prev.label.set_color('white')
        else:
            self.btn_prev.ax.set_facecolor('0.85')
            self.btn_prev.label.set_color('black')

        if self.show_answer:
            correct = item['a'].split('.')[-1].strip().lower()
            is_correct = self.guess.lower() == correct
            self.txt_feedback1.set_text(f"Vermutung: {self.guess}\nLösung: {item['a']}\n{'RICHTIG' if is_correct else 'FALSCH'}")
            self.txt_feedback1.set_color("green" if is_correct else "red")
        else:
            self.txt_feedback2.set_text("deine Antwort?")
            self.txt_feedback2.set_color("black")
        self.fig.canvas.draw_idle()

    def move(self, step):
        # In Stufe 4 blockieren wir den Rückwärtsschritt
        if self.level == 4 and step < 0:
            return 
            
        if len(self.current_pool) > 0:
            self.index = (self.index + step) % len(self.current_pool)
            self.guess, self.show_answer = "?", False
            self.update_display()
#-------------------Daten-Auswahl--------------------------------
quiz_data0 = load_data('geloest.txt', 'antworten.txt',startzeile)
quiz_data1 = load_data('fragen.txt', 'antworten.txt',startzeile)
if load_index == 0:
   QuizViewer(quiz_data0)
if load_index == 1:
   QuizViewer(quiz_data1)
#-------------------Ende_des_Scripts-----------------------------
            
