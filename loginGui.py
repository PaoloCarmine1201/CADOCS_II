import tkinter as tk
import os
import requests
import webbrowser
from dotenv import load_dotenv, set_key
load_dotenv('src/.env')
dot_env_path = "src/.env"

BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BG_GRAY = "#ABB2B9"

FONT = "Helvetica 24"
FONT_BOLD = "Helvetica 13 bold"

class LoginCadocs:
    def __init__(self, master):
        self.master = master
        master.title("Benvenuto su CADOCS")
        master.geometry("700x500")

        # Frame che riempie tutta la finestra
        frame = tk.Frame(master, bg=BG_COLOR)
        frame.pack_propagate(False)
        frame.pack(expand=True, fill=tk.BOTH)

        # Aggiunta del Label con la scritta grande centrata in alto
        label_welcome = tk.Label(frame, text="Benvenuto su CADOCS", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        label_welcome.pack(anchor="n")

        # Aggiunta del Button sotto la scritta
        button_start = tk.Button(frame, text="Login", font=FONT, command=lambda: self.get_access_token())
        button_start.pack(anchor="s")

        self.label_info1 = tk.Label(frame, text="Retrieving Personal Access Token from GitHub", bg=BG_COLOR, fg=TEXT_COLOR)
        self.label_info2 = tk.Label(frame, text="")
        self.textCode = tk.Text(frame, wrap="word",height=3, width=10)
        self.textCode.config(state="normal")

        self.buttonCopy = tk.Button(frame, command=lambda: self.copyCode(), text="Copy", bg=BG_COLOR)

        self.ButtonLogin = tk.Button(frame, text="Confirm Login", font=FONT)
        self.isClicked = tk.BooleanVar(value=False)  # Variabile di Tkinter per tracciare il clic del pulsante
        #[bold magenta]Retrieving Personal Access Token from GitHub
        #[bold magenta]To authorize this app, go to https://github.com/login/device and enter the code 44A2-10F6
        #[bold magenta]Press any key to continue once you have input the code successfully

    def start_action(self):
        self.get_access_token()


    def copyCode(self):
        text_content = self.textCode.get("1.0", "end-1c")
        self.master.clipboard_clear()
        self.master.clipboard_append(text_content)

    def openBrowser(self, uri, user_code):
        self.label_info1.pack(anchor="sw")

        self.label_info2.config(text="To authorize this app, go to {} and enter the code below".format(uri), bg=BG_COLOR, fg=TEXT_COLOR)
        self.label_info2.pack(anchor="sw")

        self.textCode.insert(tk.END, "{}".format(user_code))
        self.textCode.config(state="disabled")
        self.textCode.pack(anchor="center")

        self.buttonCopy.pack(anchor="center")
        self.ButtonLogin.config(command=lambda: self.confirmCode())
        self.ButtonLogin.pack(anchor="center")
        webbrowser.open_new(uri)
        self.master.wait_variable(self.isClicked)
        print("\n\ndopo conferma codice\n\n")
        

        

    def confirmCode(self):
        print("\n\nConfirm code\n\n")
        self.isClicked.set(True)  # Imposta la variabile su True quando il pulsante viene cliccato
        print("stato: ", self.isClicked)
        return


    def execute_oauth2(self,header, payload):
        """
        This function allows the user to authenticate with his GitHub account.
        It is used to ask the oauth2 system to produce a device code in order to get the access token.

        :param header: the http header to make a request
        :param payload: the payload containing the secret client id
        :return: the device code needed to complete the authentication
        """
        self.flag = False
        r = requests.post('https://github.com/login/device/code',headers=header,json=payload)
        data = r.json()
        device_code = data['device_code']
        uri = data['verification_uri']
        user_code = data['user_code']
        self.openBrowser(uri, user_code)
        if self.isClicked:
            print("Sono in execute")
            return device_code
    
    def generate_new_token(self,header, payload):
        """
        This function is used to generate a new Personal Access Token through the GitHub API.
        It also stores the token in the environment.

        :param header: the http header to make a request
        :param payload: the payload containing the secret client id and the device code obtained with the authentication
        :return: the personal access token
        """ 
        r = requests.post( "https://github.com/login/oauth/access_token", headers=header, json=payload)
        set_key(dot_env_path, "PAT", r.json()['access_token'])   
        return r.json()['access_token']

    def get_access_token(self):
        """
        This function is used to retrieve the personal access token either from the environment if stored or through a new GitHub authentication.

        :return: the personal access token
        """ 
        pat = os.environ.get('PAT',"")
        print("Retrieving Personal Access Token from GitHub")
        if not pat:
            print("[bold magenta]Retrieving Personal Access Token from GitHub")
            client_id = os.environ.get('CLIENT_ID',"")
            header = {"Content-Type": "application/json", "Accept": "application/json"}
            payload1 = {"client_id": client_id,}
            device_code = self.execute_oauth2(header, payload1)
            payload2 = {
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            }
            pat = self.generate_new_token(header, payload2)
        else:
            self.label_info1.config(text="Retrieving stored Personal Access Token")
            self.label_info1.pack(anchor="sw")
            self.ButtonLogin.config(command=lambda: self.openTool(pat))
            self.ButtonLogin.pack(anchor="center")

        if self.isClicked:
            self.openTool()
            print("Prima del return di pat")
            return pat 

    def openTool(self):
        print("Sono in openTool")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginCadocs(root)
    root.mainloop()
