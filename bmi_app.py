import json
import os
from datetime import datetime
import csv
from fpdf import FPDF

translations = {
    'en': {
        'welcome': "Welcome to the BMI calculator!",
        'choose_option': "Please choose an option (1, 2, 3, 4, 5, or 6): ",
        'menu_option1': "1. Calculate BMI",
        'menu_option2': "2. View Calculation History",
        'menu_option3': "3. Export History to CSV",
        'menu_option4': "4. Export History to PDF",
        'menu_option5': "5. Change Language",
        'menu_option6': "6. Remove Entry from CSV History",
        'menu_option7': "7. Exit",
        'input_first_name': "\nEnter your first name: ",
        'input_last_name': "Enter your last name: ",
        'input_weight': "Enter your weight in kg: ",
        'input_height': "Enter your height in cm: ",
        'invalid_input': "\nInvalid input! Please enter a value between {min_value} and {max_value}.",
        'invalid_input_nv': "\nInvalid input! Please enter numeric values.",
        'bmi_result': "BMI: {rounded_result}\nInterpretation: {interpretation}",
        'export_success_csv': "History exported to bmi_history_en.csv.",
        'export_success_pdf': "History exported to bmi_history_en.pdf",
        'goodbye': "Thank you for using the BMI calculator. Goodbye!",
        'underweight': "Underweight",
        'normal_weight': "Normal weight",
        'overweight': "Overweight",
        'obesity': "Obesity",
        'no_history': "\nNo history available.",
        'bmi_history': "History of BMI calculations:",
        'history_entry': "Name: {name}, Weight: {weight} kg, Height: {height} cm, BMI: {bmi}, Interpretation: {interpretation}, Date: {date}",
        'invalid_option': "Invalid input! Please enter '1', '2', '3', '4', '5', or '6'.",
        'name_error_length': "Name should be between 2 and 20 characters long.",
        'name_error_invalid': "Name should only contain letters, apostrophes, and hyphens.",
        'saving_error': "Error saving the history to file.",
        'loading_error': "Error loading the history from file.",
        'csv_name': "Name",
        'csv_weight': "Weight",
        'csv_height': "Height",
        'csv_bmi': "BMI",
        'csv_interpretation': "Interpretation",
        'csv_date': "Date",
        'delete_entry_choice': "Please choose the number of the entry to delete (or 0 to cancel): ",
        'deletion_canceled': "\nOperation canceled.",
        'deletion_success': "\nEntry successfully deleted.",
        'invalid_deletion_option': "\nInvalid input!",
        'confirm_deletion': "\nDo you really want to delete this entry? (y/n)",
        'entry_deleted': "\nEntry deleted."
    },
    'pl':{
        'welcome': "Witamy w kalkulatorze BMI!",
        'choose_option': "Wybierz opcję (1, 2, 3, 4, 5 lub 6): ",
        'menu_option1': "1. Oblicz BMI",
        'menu_option2': "2. Wyświetl historię obliczeń",
        'menu_option3': "3. Eksportuj historię do CSV",
        'menu_option4': "4. Eksportuj historię do PDF",
        'menu_option5': "5. Zmień język",
        'menu_option6': "6. Usuń wpis z historii CSV",
        'menu_option7': "7. Wyjdź",
        'input_first_name': "\nPodaj swoje imię: ",
        'input_last_name': "Podaj swoje nazwisko: ",
        'input_weight': "Podaj swoją wagę w kg: ",
        'input_height': "Podaj swój wzrost w cm: ",
        'invalid_input': "\nNieprawidłowy wpis! Proszę podać wartości pomiędzy {min_value} a {max_value}.",
        'invalid_input_nv': "\nNieprawidłoy wpis! Proszę podać wartości numeryczne.",
        'bmi_result': "BMI: {rounded_result}\nInterpretacja: {interpretation}",
        'export_success_csv': "Historia wyeksportowana do pliku bmi_history_pl.csv.",
        'export_success_pdf': "Historia wyeksportowana do pliku bmi_history_pl.pdf",
        'goodbye': "Dziękujemy za skorzystanie z kalkulatora BMI. Do widzenia!",
        'underweight': "Niedowaga",
        'normal_weight': "Prawidłowa waga",
        'overweight': "Nadwaga",
        'obesity': "Otyłość",
        'no_history': "\nBrak dostępnej historii.",
        'bmi_history': "Historia obliczeń BMI:",
        'history_entry': "Imię: {name}, Waga: {weight} kg, Wzrost: {height} cm, BMI: {bmi}, Interpretacja: {interpretation}, Data: {date}",
        'invalid_option': "Nieprawidłowy wybór! Proszę wybrać '1', '2', '3', '4', '5', lub '6'.",
        'name_error_length': "Imię powinno mieć od 2 do 20 znaków.",
        'name_error_invalid': "Imię i nazwisko powinny zawierać tylko litery, apostrofy i myślniki.",
        'saving_error': "Error saving the history to file.",
        'loading_error': "Error loading the history from file.",
        'csv_name': "Imię",
        'csv_weight': "Waga",
        'csv_height': "Wzrost",
        'csv_bmi': "BMI",
        'csv_interpretation': "Interpretacja",
        'csv_date': "Data",
        'delete_entry_choice': "Wybierz numer wpisu do usunięcia (lub 0, aby anulować): ",
        'deletion_canceled': "\nOperacja przerwana.",
        'deletion_success': "\nWpis został usunięty pomyślnie.",
        'invalid_deletion_option': "\nNieprawidłowy wybór",
        'confirm_deletion': "\nCzy na pewno chcesz usunąć ten wpis? (y/n)",
        'entry_deleted': "\nWpis został usunięty."
    },
    'de':{
        'welcome': "Willkommen beim BMI-Rechner!",
        'choose_option': "Bitte wählen Sie eine Option (1, 2, 3, 4, 5 oder 6): ",
        'menu_option1': "1. BMI berechnen",
        'menu_option2': "2. Berechnungshistorie anzeigen",
        'menu_option3': "3. Historie in CSV exportieren",
        'menu_option4': "4. Historie in PDF exportieren",
        'menu_option5': "5. Sprache ändern",
        'menu_option6': "6. Eintrag aus der CSV-Historie entfernen",
        'menu_option7': "7. Beenden",
        'input_first_name': "\nGeben Sie Ihren Vornamen ein: ",
        'input_last_name': "Geben Sie Ihren Nachnamen ein: ",
        'input_weight': "Geben Sie Ihr Gewicht in kg ein: ",
        'input_height': "Geben Sie Ihre Größe in cm ein: ",
        'invalid_input': "\nUngültige Eingabe! Geben Sie einen Wert zwischen {min_value} und {max_value} ein.",
        'invalid_input_nv': "\nUngültige Eingabe! Bitte geben Sie numerische Werte ein.",
        'bmi_result': "BMI: {rounded_result}\nInterpretation: {interpretation}",
        'export_success_csv': "Historie in bmi_history_de.csv exportiert.",
        'export_success_pdf': "Historie in bmi_history_de.pdf exportiert.",
        'goodbye': "Vielen Dank für die Nutzung des BMI-Rechners. Auf Wiedersehen!",
        'underweight': "Untergewicht",
        'normal_weight': "Normalgewicht",
        'overweight': "Übergewicht",
        'obesity': "Fettleibigkeit",
        'no_history': "\nKeine Historie verfügbar.",
        'bmi_history': "Historie der BMI-Berechnungen:",
        'history_entry': "Name: {name}, Gewicht: {weight} kg, Größe: {height} cm, BMI: {bmi}, Interpretation: {interpretation}, Datum: {date}",
        'invalid_option': "Ungültige Eingabe! Bitte wählen Sie '1', '2', '3', '4', '5', oder '6' ein.",
        'name_error_length': "Der Name sollte zwischen 2 und 20 Zeichen lang sein",
        'name_error_invalid': "Der Name sollte nur Buchstaben, Apostrophe und Bindestriche enthalten.",
        'saving_error': "Fehler beim Speichern der Historie.",
        'loading_error': "Fehler beim Laden der Historie.",
        'csv_name': "Name",
        'csv_weight': "Gewicht",
        'csv_height': "Größe",
        'csv_bmi': "BMI",
        'csv_interpretation': "Interpretation",
        'csv_date': "Datum",
        'delete_entry_choice': "Wählen Sie die Nummer des Eintrags zum Löschen (oder 0, um abzubrechen): ",
        'deletion_canceled': "\nVorgang abgebrochen.",
        'deletion_success': "\nEintrag erfolgreich gelöscht.",
        'invalid_deletion_option': "\nUngüLtige Eingabe!",
        'confirm_deletion': "\nMöchten Sie wirklich diesen Eintrag entfernen? (y/n)",
        'entry_deleted': "\nEintrag entfernt."
    }
}

def choose_language():
    print("\nChoose a language / Wybierz język:")
    print("1. English / Angielski / Englisch")
    print("2. Polish / Polski / Polnisch")
    print("3. German / Niemiecki / Deutsch")

    while True:
        choice = input("\nEnter '1', '2', or '3 / Wpisz '1', '2' lub '3' / Geben Sie '1', '2', oder '3' ein: ").strip()
        if choice == "1":
            return 'en'
        elif choice == "2":
            return 'pl'
        elif choice == "3":
            return 'de'
        else:
            print("\nInvalid choice! / Nieprawidłowy wybór! / Ungültige Wahl! ")

def change_language():
    return choose_language()

def bmi_calculator(weight, height):
    return weight / ((height / 100) ** 2)

def bmi_interpretation(bmi, t):
    if bmi < 18.5:
        return t['underweight']
    elif 18.5 <= bmi < 25:
        return t['normal_weight']
    elif 25 <= bmi < 30:
        return t['overweight']
    else:
        return t['obesity']
    
def get_valid_input(prompt, min_value, max_value, t):
    while True:
        try:
            value = float(input(prompt).replace(',','.'))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"{t['invalid_input'].format(min_value=min_value, max_value=max_value)}")
        except ValueError:
            print(t['invalid_input_nv'])

def display_history(history, t):
    if not history:
        print(f"{t['no_history']}")
        return
    
    print(f"\n{t['bmi_history']}")
    for entry in history:
        print(t['history_entry'].format(
            name=entry['name'], 
            weight=entry['weight'], 
            height=entry['height'], 
            bmi=entry['bmi'], 
            interpretation=entry['interpretation'], 
            date=entry['date']
        ))

def validate_first_name(first_name, t):
    if len(first_name) < 2 or len(first_name) > 20:
        return False, t['name_error_length'] 
    
    for char in first_name:
        if not (char.isalpha() or char in "-'"):
            return False, t['name_error_invalid']
        
    return True, ""

def validate_last_name(last_name, t):
    if len(last_name) < 2 or len(last_name) > 20:
        return False, t['name_error_length'] 
    
    for char in last_name:
        if not (char.isalpha() or char in "-'"):
            return False, t['name_error_invalid']
        
    return True, ""

def input_first_name(t):
    while True:
        first_name = input(t['input_first_name']).strip().title()
        is_valid, error_message = validate_first_name(first_name, t)
        if is_valid:
            return first_name
        else:
            print(f"\n{error_message}")

def input_last_name(t):
    while True:
        last_name = input(t['input_last_name']).strip().title()
        is_valid, error_message = validate_last_name(last_name, t)
        if is_valid:
            return last_name
        else:
            print(f"\n{error_message}")

def calculate_bmi(history, t):
    first_name = input_first_name(t)
    last_name = input_last_name(t)
    weight = get_valid_input(t['input_weight'], 1, 250, t)
    height = get_valid_input(t['input_height'], 1, 250, t)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = bmi_calculator(weight, height)
    rounded_result = round(result, 2)
    interpretation = bmi_interpretation(rounded_result, t)

    print(f"\n{t['bmi_result'].format(rounded_result=rounded_result, interpretation=interpretation)}")
   
    history.append({
        'name': f"{first_name} {last_name}",
        'weight': weight,
        'height': height,
        'bmi': rounded_result,
        'interpretation': interpretation,
        'date': date
    })

def save_history_to_file(filename, history, t):
    try:
        with open(filename, 'w') as file:
            json.dump(history, file, indent=4)
    except IOError:
        print(t['saving_error'])

def load_history_from_file(filename, t):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
    except IOError:
        print(t['loading_error'])    
    return []

def export_history_to_csv(filename, history, t):
    fieldnames = [
        t['csv_name'],
        t['csv_weight'], 
        t['csv_height'],
        t['csv_bmi'],
        t['csv_interpretation'], 
        t['csv_date']
    ]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for entry in history:
            writer.writerow({
                t['csv_name']: entry['name'],
                t['csv_weight']: entry['weight'],
                t['csv_height']: entry['height'],
                t['csv_bmi']: entry['bmi'],
                t['csv_interpretation']: entry['interpretation'],
                t['csv_date']: entry['date']
            })
        
def export_history_to_pdf(filename, history, t):
    if not history:
        print(f"{t['no_history']}")
        return
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, t['bmi_history'], ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    for entry in history:
        entry_text = t['history_entry'].format(
            name=entry['name'],
            weight=entry['weight'],
            height=entry['height'],
            bmi=entry['bmi'],
            interpretation=entry['interpretation'],
            date=entry['date']
        )
        pdf.multi_cell(0, 10, entry_text)
        pdf.ln()

    try:
        pdf.output(filename)
        print(f"{t['export_success_pdf']}")
    except IOError:
        print(f"{t['saving_error']}")

def display_csv_entries(filename, t):
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            entries = list(reader)

        if not entries:
            print(f"{t['no_history']}")
            return []

        print(f"{t['bmi_history']}")
        for i, entry in enumerate(entries, 1):
            print(f"{i}. {t['history_entry'].format(name=entry[t['csv_name']], weight=entry[t['csv_weight']], height=entry[t['csv_height']], bmi=entry[t['csv_bmi']], interpretation=entry[t['csv_interpretation']], date=entry[t['csv_date']])}")
                
        return entries
    
    except IOError:
        print(f"{t['loading_error']}")

def delete_csv_entry(filename, t):
    entries = display_csv_entries(filename, t)

    if not entries:
        return
    
    while True:
        try:
            choice = int(input(f"{t['delete_entry_choice']}"))
            if choice == 0:
                print(f"{t['deletion_canceled']}")
                return
            elif 1 <= choice <= len(entries):
                confirm = input(f"{t['confirm_deletion']}")
                if confirm.lower() == 'y':
                    del entries[choice - 1]
                    break
                else:
                    print(f"{t['deletion_canceled']}")
                break
            else:
                print(f"{t['invalid_deletion_option']}")
        except ValueError:
            print(f"{t['invalid_deletion_option']}")

    fieldnames = [t['csv_name'], t['csv_weight'], t['csv_height'], t['csv_bmi'], t['csv_interpretation'], t['csv_date']]

    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(entries)
        print(f"{t['deletion_success']}")
    except IOError:
        print(f"{t['saving_error']}")

def main_menu(language):
    history_file = f'bmi_history_{language}.json'
    csv_file = f'bmi_history_{language}.csv'
    pdf_file = f'bmi_history_{language}.pdf'
    t = translations[language]
    history = load_history_from_file(history_file, t)

    while True:
        print(f"\n{t['welcome']}")
        print(f"{t['menu_option1']}")
        print(f"{t['menu_option2']}")
        print(f"{t['menu_option3']}")
        print(f"{t['menu_option4']}")
        print(f"{t['menu_option5']}")
        print(f"{t['menu_option6']}")
        print(f"{t['menu_option7']}")
        
        operation = input(f"\n{t['choose_option']}").strip()
        if operation == "1":
            calculate_bmi(history, t)
            save_history_to_file(history_file, history, t)
        elif operation == "2":
            display_history(history, t)
        elif operation == "3":
            export_history_to_csv(csv_file, history, t)
            print(f"\n{t['export_success_csv']}")
        elif operation == "4":
            export_history_to_pdf(pdf_file, history, t)
            print(f"\n{t['export_success_pdf']}")
        elif operation == "5":
            language = change_language()
            history_file = f'bmi_history_{language}.json'
            csv_file = f'bmi_history_{language}.csv'
            pdf_file = f'bmi_history_{language}.pdf'
            t = translations[language]
            history = load_history_from_file(history_file, t)
        elif operation == "6":
            delete_csv_entry(csv_file, t)
        elif operation == "7":
            print(f"\n{t['goodbye']}")
            save_history_to_file(history_file, history, t)
            break
        else:
            print(f"\n{t['invalid_option']}")

if __name__ == "__main__":
    language = choose_language()
    main_menu(language)
