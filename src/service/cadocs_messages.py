import json
from src.intent_handling.cadocs_intent import CadocsIntents
from src.service.language_handler import LanguageHandler


#Sistemare la classe
def build_cs_message(smells, entities, lang):
    #lang = LanguageHandler().get_current_language()
    

    print("\n\n\nSTAMPA STAMPA STAMPA Linguaggio",lang)
    print("\n\n\n")
    
    # Testo che verrà restituito
    text = ""

    if lang == "en":
        text += f"Hi 👋🏼\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"

    if len(entities) > 2:
        if lang == "en":
            text += f"These are the community smells we were able to detect in the repository {entities[0]} starting from {entities[1]}:\n"
        elif lang == "it":
            text += f"Questi sono i community smells che siamo stati in grado di rilevare nella repository {entities[0]} a partire da {entities[1]}:\n"
    else:
        if lang == "en":
            text += f"These are the community smells we were able to detect in the repository {entities[0]}:\n"
        elif lang == "it":
            text += f"Questi sono i community smells che siamo stati in grado di rilevare nella repository {entities[0]}:\n"

    if lang == "en":
        # Aggiunta del testo per ogni smell rilevato
        with open('src/community_smells.json') as fp:
            data = json.load(fp)
            for s in smells:
                smell_data = [sm for sm in data if sm["acronym"] == s]

                text += f"----------------------------\n"
                text += f"*{s}* {smell_data[0].get('name')} {smell_data[0].get('emoji')}\n_{smell_data[0].get('description')}_\n"
                strategies = smell_data[0].get("strategies")

                # Aggiunta delle strategie se presenti
                if len(strategies) > 0:
                    text += "Some possible mitigation strategies are:\n"
                    for st in strategies:
                        text += f">{st.get('strategy')}\n{st.get('stars')}\n"
    elif lang == "it":
        with open('src/community_smells_it.json') as fp:
            data = json.load(fp)
            for s in smells:
                smell_data = [sm for sm in data if sm["acronym"] == s]

                text += f"----------------------------\n"
                text += f"*{s}* {smell_data[0].get('name')} {smell_data[0].get('emoji')}\n_{smell_data[0].get('description')}_\n"
                strategies = smell_data[0].get("strategies")

                # Aggiunta delle strategie se presenti
                if len(strategies) > 0:
                    text += "Alcuni possibili strategie per la mitigazione sono:\n"
                    for st in strategies:
                        text += f">{st.get('strategy')}\n{st.get('stars')}\n"

    if lang == "en":
        text += "----------------------------\nSee you soon 👋🏼"
    elif lang == "it":
        text += "----------------------------\nA presto 👋🏼"

    return text

def build_report_message(exec_type, results, entities, lang):
    #lang = LanguageHandler().get_current_language()
    
    # Testo che verrà restituito
    text = ""

    if lang == "en":
        text += f"Hi 👋🏼\n"
        text += "This is a summary of your last execution\n"
        text += f"*Type:*\n{exec_type}\n"
        text += f"*Repository:*\n{entities[0]}\n"
        text += f"*Date:*\n{entities[1]}\n"
        text += "*Results:*\n" + "\n".join(results) + "\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"
        text += "Questo è una sintesi della tua ultima esecuzione\n"
        text += f"*Tipo:*\n{exec_type}\n"
        text += f"*Repository:*\n{entities[0]}\n"
        text += f"*Data:*\n{entities[1]}\n"
        text += "*Risultati:*\n" + "\n".join(results) + "\n"

    return text

def build_info_message(lang):
    #lang = LanguageHandler().get_current_language()

    # Testo che verrà restituito
    text = ""

    if lang == "en":
        text += f"Hi 👋🏼\n"
        text += "These are the *community smells* I can detect in your development communities:\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"
        text += "Questi sono i *community smells* che riesco a individuare nelle vostre community:\n"

    # Aggiunta del testo per ogni smell
    if lang == "en":
        with open('src/community_smells.json') as fp:
            data = json.load(fp)
            for i in data:
                text += f"----------------------------\n*{i.get('name')}*  -  {i.get('acronym')}  -  {i.get('emoji')}\n{i.get('description')}\n"

        if lang == "en":
            text += "----------------------------\nIf you want to remain up-to-date, please follow us on our social networks:\n"
            text += "- Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab>\n"
            text += "- Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab>\n"
            text += "- Website: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io>\n"
            text += "Also, feel free to get in touch with us to have a discussion about the subject by sending us an email at slambiase@unisa.it!"
        
    elif lang == "it":
        with open('src/community_smells_it.json') as fp:
            data = json.load(fp)
            for i in data:
                text += f"----------------------------\n*{i.get('name')}*  -  {i.get('acronym')}  -  {i.get('emoji')}\n{i.get('description')}\n"

            text += "----------------------------\nSe volete rimanere aggiornati, seguite i canali social:\n"
            text += "- Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab>\n"
            text += "- Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab>\n"
            text += "- Sito web: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io>\n"
            text += "Inoltre, sentitevi liberi di mettervi in contatto con noi per discutere dell'argomento inviandoci una mail a slambiase@unisa.it!"


    return text

def build_error_message(lang):
    #lang = LanguageHandler().get_current_language()

    # Testo che verrà restituito
    if lang == "en":
        text = f"Hi, I'm sorry but I did not understand your intent. Please be more specific!"
    elif lang == "it":
        text = f"Ciao, mi dispiace ma non sono riuscito a comprendere il suo intent. La prego di essere più specifico!"

    return text

# this function will format the message basing on the intent
def build_message(results, intent, entities, lang):
    
    if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
        response = build_cs_message(results, entities=entities, lang = lang)
        return response
    elif intent == CadocsIntents.Report:
        response = build_report_message(exec_type=entities[2], results=results, entities=entities, lang = lang)
        return response
    elif intent == CadocsIntents.Info:
        response = build_info_message(lang)
        return response