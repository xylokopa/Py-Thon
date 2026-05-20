# Quiz-Viewer_15.py 20-05-26 Idee R.Wurdack 200_Zeilen-Script Google-Gemini
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import random
#-------------------Start-Bedingungen----------------------------
load_index = 0     # 0: Learn-Modus mit Loesung  1: Quiz-Modus
startzeile = 1     # Verschiebbarer Zeiger auf die erste Frage
#-------------------Quiz-Ablauf---------------------------------
def load_data(fragen_file, antworten_file,start_zeile):
    questions = []
    try:
        with open(fragen_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            lines = lines[(start_zeile-1)*12:]            
        for i in range(0, len(lines), 12):                      
            questions.append(lines[i:i+12])                     
        with open(antworten_file, 'r', encoding='utf-8') as f:
            answers = [line.strip() for line in f if line.strip()]
            answers = answers[(start_zeile-1):]
    except: return []
    return [{"q_lines": q, "ans": a, "id": i} for i, (q, a) in enumerate(zip(questions, answers))]

class QuizViewer:
    def __init__(self, quiz_data, load_index, startzeile):
        self.quiz_data = quiz_data
        self.load_index = load_index
        self.startzeile = startzeile
        self.num_to_pick = min(len(quiz_data), 155)      # 152
        self.level = 0 # 0,1=Geloest, 2=Zufall, 3=Streng, 4=Kein Zurück!
        self.index = 0
        self.guess = "?"
        self.show_answer = False
        self.score = 0
        self.answered_ids = set()
        self.current_pool = []
        self.fig, self.ax = plt.subplots(figsize=(11, 5.5)) 
        plt.subplots_adjust(left=0.01, bottom=0.05)                                                                #00
        self.ax.axis('off')
        self.txt_q = self.ax.text(0.01, 0.99, "", va='top', fontsize=11, family='monospace')
        self.txt_feedback1 = self.ax.text(0.17, 0.11, "", va='top', fontsize=12, fontweight='bold')                #01
        self.txt_feedback2 = self.ax.text(0.17, 0.16, "", va='top', fontsize=12, fontweight='bold')                #02
        self.txt_score1 = self.ax.text(0.01, 0.06, "", va='top', fontsize=13, color='darkblue', fontweight='black')#03
        self.txt_score2 = self.ax.text(0.01, 0.01, "", va='top', fontsize=13, color='darkblue', fontweight='black')#04
        # Antwort-Buttons
        self.btn_choices = []
        for i, label in enumerate(['a', 'b', 'c', 'd']):
            ax_c = plt.axes([0.655, 0.185 - (i * 0.06), 0.04, 0.05])                                               #05
            btn = Button(ax_c, label)
            btn.on_clicked(lambda e, l=label: self.make_guess(l))
            self.btn_choices.append(btn)
        # Navigation mit Buttons
        self.btn_prev = Button(plt.axes([0.57, 0.052, 0.07, 0.132]), '<<')                                         #06
        self.btn_num = Button(plt.axes([0.42, 0.122, 0.14, 0.06]), f'Anzahl: {self.num_to_pick}')                  #07
        self.lvl_txt = ["tafel","geloest","zufall","streng","kein zurueck"]
        self.btn_lvl = Button(plt.axes([0.42, 0.055, 0.14, 0.06]), f'Modus:{self.lvl_txt[self.level]}')            #08
        self.btn_next = Button(plt.axes([0.71, 0.052, 0.07, 0.132]), '>>')                                         #09
        ax_box = self.fig.add_axes([0.01, 0.11, 0.10, 0.06])                                                       #10
        self.text_box = TextBox(ax_box, '', initial=str(startzeile))
        self.text_box.label.set_text('Startzeile:')
        self.text_box.label.set_position((1.3, 1.3))
        ax_btn = self.fig.add_axes([0.12, 0.11, 0.03, 0.06])                                                       #11
        self.btn_submit = Button(ax_btn, 'OK')
        self.text_box.on_submit(self.zeilen_eingabe) # submit-trigger
        self.btn_submit.on_clicked(self.eingabe_absenden)
        self.btn_prev.on_clicked(lambda x: self.move(-1))
        self.btn_next.on_clicked(lambda x: self.move(1))
        self.btn_num.on_clicked(self.toggle_num)
        self.btn_lvl.on_clicked(self.toggle_level)
        self.reset_quiz()
        plt.show()

    def zeilen_eingabe(self, text):
        try:
            wert = int(text)
            # Prüfen, ob die Zahl im erlaubten Bereich liegt
            if 1 <= wert <= 155:
                self.startzeile = wert
                self.reload_data(self)
                print(self.startzeile)
            else:
                raise ValueError("Zahl außerhalb des Bereichs.")
        except ValueError:
            self.startzeile = 1
        plt.draw()
    def eingabe_absenden(self, event):
           """Absenden, falls User nicht Enter drückt."""
           self.zeilen_eingabe(self.text_box.text)     

    def reload_data(self, *args):
        # 1. Daten neu aus der Datei laden
        if self.load_index == 0:
           self.quiz_data = load_data('geloest.txt', 'antworten.txt', self.startzeile)
        elif self.load_index == 1:
           self.quiz_data = load_data('fragen.txt', 'antworten.txt', self.startzeile)
        # 2. Pool für Anzeige neu überschreiben
        self.current_pool = self.quiz_data 
        # 3. Index auf die erste Frage (0)
        self.index = 0   
        # 4. Anzeige neu
        if len(self.current_pool) > 0:
           self.update_display()
        else:
           print("Konsole: neuer Fragen-Pool leer!")        

    def toggle_num(self, event):
        self.num_to_pick = (self.num_to_pick % len(self.quiz_data)) + 1
        self.btn_num.label.set_text(f'Anzahl: {self.num_to_pick}')
        self.reset_quiz()

    def toggle_level(self, event):
        # Zahlenring 0,1 -> 2 -> 3 -> 4 -> 0
        self.level = (self.level + 1) % 5
        self.btn_lvl.label.set_text(f'Modus:{self.lvl_txt[self.level]}')
        self.reset_quiz()

    def reset_quiz(self):
        self.score = 0
        self.answered_ids = set()
        self.index = 0       
        if self.level == 0:
            self.load_index = 0
            self.startzeile = 1
            self.reload_data(self)
            self.current_pool = self.quiz_data[:self.num_to_pick]
            self.txt_q.set_fontsize(15)
            # 0. GROSSSCHRIFT Redraw the canvas to see the update
            self.ax.figure.canvas.draw_idle()            
        if self.level == 1:
            self.load_index = 0
            self.startzeile = 1
            self.reload_data(self)
            self.current_pool = self.quiz_data[:self.num_to_pick]
            self.txt_q.set_fontsize(11)
            # 1. KLEINSCHRIFT Redraw the canvas to see the update
            self.ax.figure.canvas.draw_idle()            
        elif self.level == 2:
            self.load_index = 0
            self.startzeile = 1
            self.reload_data(self)
            self.current_pool = random.sample(self.quiz_data, self.num_to_pick)
        elif self.level >= 3:
            self.load_index = 1
            self.startzeile = 1
            self.reload_data(self)
            # Stufe 3 und 4 nutzen beide den strengen Zufall (shuffled)
            temp_pool = list(self.quiz_data)
            random.shuffle(temp_pool)
            self.current_pool = temp_pool[:self.num_to_pick]
        self.update_display()

    def make_guess(self, label):
        if not self.show_answer:
            item = self.current_pool[self.index]
            correct = item['ans'].split('.')[-1].strip().lower()
            if label.lower() == correct and item['id'] not in self.answered_ids:
                self.score += 1
                self.answered_ids.add(item['id'])
            self.guess, self.show_answer = label, True
            self.update_display()

    def update_display(self):
        item = self.current_pool[self.index]
        lvl_names = ["Tafel_0","Geloest_1", "Zufall_2", "Streng_3", "KEIN ZURUECK!_4"]
        mode_text = lvl_names[self.level]
        self.txt_q.set_text(f"Modus:{mode_text}|Frage {self.index+1}/{len(self.current_pool)}\n\n"+"\n".join(item['q_lines']))
        self.txt_score1.set_text(f"richtig:")
        self.txt_score2.set_text(f"{self.score} von {len(self.current_pool)}")
        # Zurück-Button ausgrauen/sperren in Stufe 4
        if self.level == 4:
            self.btn_prev.ax.set_facecolor('gray')
            self.btn_prev.label.set_color('white')
        else:
            self.btn_prev.ax.set_facecolor('0.85')
            self.btn_prev.label.set_color('black')
        if self.show_answer:
            correct = item['ans'].split('.')[-1].strip().lower()
            is_correct = self.guess.lower() == correct
            self.txt_feedback1.set_text(f"Vermutung: {self.guess}\nLösung: {item['ans']}\n{'RICHTIG' if is_correct else 'FALSCH'}")
            self.txt_feedback1.set_color("green" if is_correct else "red")
        else:
            self.txt_feedback2.set_text("deine Antwort?")
            self.txt_feedback2.set_color("black")
        self.fig.canvas.draw_idle()

    def move(self, step):
        # In Stufe 4 blockieren wir den Rückwärtsschritt
        self.txt_feedback1.set_text(f"Nächste Frage: \n             \n               ")
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
   QuizViewer(quiz_data0,load_index,startzeile)
if load_index == 1:
   QuizViewer(quiz_data1,load_index,startzeile)
#-------------------Ende_des_Scripts-----------------------------
            
