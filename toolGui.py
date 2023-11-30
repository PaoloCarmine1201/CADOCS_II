import tkinter as tk
from tkinter import ttk
from src.chatbot.intent_manager import IntentManager
from src.intent_handling.cadocs_intent import CadocsIntents
from src.intent_handling.intent_resolver import IntentResolver
from src.service.cadocs_messages import build_message, build_error_message
from loginGui import LoginCadocs
import os
from dotenv import load_dotenv
load_dotenv('src/.env')

BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BG_GRAY = "#ABB2B9"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

pat = os.environ.get('PAT',"")
prova = False


class CADOCS:
    def __init__(self, master):
        self.last_repo = ""
        self.asked_user = ""
        # the conversation queue will be used to check whether or not a message has already been answered
        self.conversation_queue = []

        self.master = master
        self.master.title("CADOCS")

        # Imposta la larghezza e l'altezza dello schermo
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calcola le dimensioni per la finestra sinistra (20% dello schermo)
        left_width = int(screen_width * 0.2)
        left_height = screen_height

        # Crea la finestra sinistra
        self.left_frame = tk.Frame(self.master, width=left_width, height=left_height, bg=BG_GRAY)
        self.left_frame.pack_propagate(False)  # Impedisce al frame di restringersi ai widget interni
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Calcola le dimensioni per la finestra destra (80% dello schermo)
        right_width = int(screen_width * 0.8)
        right_height = screen_height

        # Crea la finestra destra
        self.right_frame = tk.Frame(self.master, width=right_width, height=right_height, bg=BG_COLOR)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # TextWidget
        self.textWidget = tk.Text(self.right_frame, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.textWidget.pack(expand=True, fill=tk.BOTH)
        self.textWidget.configure(state=tk.DISABLED)

        # Scrollbar
        self.scrollBar = tk.Scrollbar(self.right_frame, command=self.textWidget.yview)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.textWidget.configure(yscrollcommand=self.scrollBar.set)

        # messageEntryBox
        self.messageEntry = tk.Entry(self.right_frame, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.messageEntry.focus()
        self.messageEntry.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)
        self.messageEntry.bind("<Return>", self.onEnteredPress)

        # sendButton
        self.sendButton = tk.Button(self.right_frame, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self.onEnteredPress(None))
        self.sendButton.pack(side=tk.RIGHT, padx=10, pady=10)

        self.progressBar = ttk.Progressbar(self.right_frame,orient='horizontal',mode='indeterminate',length=280)

        

    def onEnteredPress(self, event):
        msg = self.messageEntry.get()
        self.insertMessage(msg, "You")

    def insertMessage(self, msg, sender):
        if not msg:
            return
        
        self.textWidget.configure(state=tk.NORMAL)
        
        if sender == "You":
            # Messaggi dell'utente (a destra)
            self.textWidget.tag_configure("user_tag", justify="right")
            #self.textWidget.tag_add("user_tag", "insert linestart", "insert lineend")
            self.messageEntry.delete(0, tk.END)
            msg1 = f"{msg} :{sender}"
            self.textWidget.insert(tk.END, msg1+"\n", "user_tag" if sender == "You" else "bot")
            self.textWidget.configure(state=tk.DISABLED)

        intent, result,entities, lang ,sender = self.newMessage(msg)
        if sender == "CADOCS":
            self.insertCadocsMessage(result, intent, entities, lang)
            
        self.textWidget.see(tk.END)

    def insertCadocsMessage(self, msg, intent, entities, lang):
        self.textWidget.configure(state=tk.NORMAL)
        self.textWidget.tag_configure("CADOCS", justify="left")
        self.messageEntry.delete(0, tk.END)
        if (intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate) and msg[1] == 890:
            if msg[1] == 890:
                text = msg[0]
        elif intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
            text = build_message(msg, intent, entities, lang)
        elif intent == CadocsIntents.Info:
            text = build_message(msg, intent, entities, lang)
        elif intent == CadocsIntents.Report:
            text = build_message(msg, intent, entities, lang)
        else:
            text = build_error_message(lang)

        msg2 = f"CADOCS: {text}"
        self.textWidget.insert(tk.END, msg2 + "\n", "CADOCS")
        self.textWidget.configure(state= tk.DISABLED)

    def newMessage(self, msg):
        result = None
        # instantiate the manager which will tell us the intent
        manager = IntentManager()
        # detect the intent
        intent, entities, confidence, lang = manager.detect_intent(msg)
        print("INTENT:", intent)

        if entities:
            print("Entities: ", entities[0])
            # instantiate the resolver
            resolver = IntentResolver()
            # run tool
            result = resolver.resolve_intent(intent, entities)
            print("RESULT", result)

        return intent, result, entities,lang,"CADOCS"


def onCreate():
    load_dotenv('src/.env')
    pat = os.environ.get('PAT',"")
    if pat:
        root = tk.Tk()
        app = CADOCS(root)
        root.mainloop()
    
def login():
    load_dotenv('src/.env')
    pat = os.environ.get('PAT',"")
    if pat:
        onCreate()
    else:
        login_window = tk.Tk()
        login_app = LoginCadocs(login_window)
        login_window.mainloop()
        onCreate()

if __name__ == "__main__":
    if not pat:
        login()
    else:
        onCreate()