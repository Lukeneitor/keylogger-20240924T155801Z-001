import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import keyboard
import os
from datetime import datetime
import calendar as cal
from fuzzywuzzy import fuzz

# Lista de malas palabras
BAD_WORDS = [
    'porno', 'sexo', 'pornografía', 'porn', 'xxx', 'desnudo', 'erótico', 'webcam',
    'hardcore', 'fetiche', 'masturbación', 'genitales', 'vagina', 'pene', 'sexooral',
    'orgía', 'sadomasoquismo', 'bdsm', 'prostitución', 'escorts', 'violación',
    'incesto', 'lencería', 'pedofilia', 'zoofilia', 'necrofilia', 'asesinato', 'homicidio',
    'suicidio', 'secuestro', 'mutilación', 'autolesiones', 'bullying', 'acoso', 'agresión',
    'tortura', 'golpear', 'matar', 'guerra', 'amenaza', 'terrorismo', 'bomba', 'disparar',
    'pistola', 'cuchillo', 'estrangular', 'drogas', 'sobredosis', 'tráficodedrogas',
    'armas', 'cocaína', 'marihuana', 'heroína', 'lsd', 'éxtasis', 'opio', 'anfetaminas',
    'metanfetamina', 'cristal', 'crack', 'narcóticos', 'pastillas', 'jeringa', 'inyectar',
    'alucinógeno', 'traficar', 'carteles', 'narcotráfico', 'cannabis', 'hashish', 'anorexia',
    'bulimia', 'depresión', 'ansiedad', 'cortes', 'vomitar', 'atracón', 'pérdidadepesoextrema',
    'trastornoalimenticio', 'trastornodeimagencorporal', 'sedantes', 'sobredosis',
    'mutilación', 'secta', 'culto', 'sacrificio', 'satanismo', 'ocultismo', 'magiablanca',
    'rituales', 'invocar', 'sacrificiohumano', 'illuminati', 'supremacía blanca', 'nazismo',
    'racismo', 'esclavitud', 'tratadepersonas', 'explotación', 'pandillas', 'crimenorganizado',
    'cartel', 'sicarios', 'hackear', 'hacking', 'phishing', 'virus', 'malware', 'ransomware',
    'piratería', 'robaridentidad', 'deepweb', 'darkweb', 'estafas', 'fraude', 'engañar',
    'violacióndelaprivacidad', 'criptojacking', 'tráficodedatos', 'extremismo', 'yihad',
    'al-qaeda', 'isis', 'estadoislámico', 'radicalismo', 'ataqueterrorista', 'mártir',
    'inmolación', 'bombasuicida', 'guerrasanta', 'decapitación', 'fanatismo', 'fundamentalismo',
    'pedofilia', 'abusoinfantil', 'explotacióninfantil', 'grooming', 'pederasta', 'depredadorsexual',
    'tráficodemenores', 'pornografíainfantil', 'violacióninfantil', 'secuestro', 'niñoperdido',
    'abusoemocional', 'abusosexual', 'esclavitudinfantil', 'maltratoinfantil', 'racismo', 'xenofobia',
    'homofobia', 'transfobia', 'sexismo', 'odio', 'supremacía', 'discriminación', 'segregación',
    'genocidio', 'holocausto', 'discursodeodio', 'neonazi', 'supremacistablanca', 'antisemita',
    'apuestas', 'casino', 'ruleta', 'blackjack', 'tragamonedas', 'póker', 'apuestassportivas',
    'lotería', 'bingo', 'juegocompulsivo', 'ludopatía', 'perderdinero', 'alcohol', 'bebida',
    'embriagarse', 'borracho', 'resaca', 'cerveza', 'vino', 'licor', 'whiskey', 'vodka', 'cóctel',
    'alcoholismo', 'bebedorcompulsivo', 'conducirebrio', 'cortar', 'ahorcar', 'suicidio', 'quemar',
    'tirarsealtren', 'tomarveneno', 'sufrir', 'desesperación', 'vacíoemotional', 'muerte'
]

current_word = ""

def get_filename_for_date(year, month, day):
    return f'{year}-{month:02d}-{day:02d}_badwords.txt'

def write_to_file(word):
    today = datetime.now()
    filename = get_filename_for_date(today.year, today.month, today.day)
    with open(filename, 'a') as file:
        file.write(word.replace(' ', '').lower() + '\n')  # Guardar sin espacios y en minúsculas

def write_new_bad_word(word):
    # Guardar la nueva mala palabra en un archivo para referencia futura
    with open('badwords_list.txt', 'a') as file:
        file.write(word.lower() + '\n')

def contains_bad_words(text):
    text = text.lower()  # Convertir a minúsculas
    for bad_word in BAD_WORDS:
        # Verificar si la palabra está en el texto o si hay coincidencias difusas
        if bad_word in text or fuzz.ratio(bad_word, text) > 80:  # Cambia el umbral si es necesario
            return True
    return False

def on_key_press(e):
    global current_word
    key = e.name

    if key in ('space', 'enter'):
        # Evitar guardar cadenas vacías o palabras con solo espacios
        current_word = current_word.strip()
        if current_word:  # Solo guardar si hay una palabra válida
            write_to_file(current_word)  # Guardar el texto actual
        current_word = ''  # Reiniciar la palabra
    elif key == 'backspace':
        current_word = current_word[:-1]  # Eliminar el último carácter
    elif len(key) == 1 and not key.isspace():  # Si es una letra y no un espacio
        current_word += key
    update_text_display()


def update_text_display():
    selected_date = calendar.selection_get()
    today_filename = get_filename_for_date(selected_date.year, selected_date.month, selected_date.day)
    if os.path.exists(today_filename):
        result_text.set('Esperando análisis...')
    else:
        result_text.set('Sin registros para esta fecha.')

def analyze_bad_words():
    selected_date = calendar.selection_get()
    today_filename = get_filename_for_date(selected_date.year, selected_date.month, selected_date.day)
    if os.path.exists(today_filename):
        with open(today_filename, 'r') as file:
            content = file.read()
        
        bad_words_found = []
        for line in content.splitlines():
            words = line.split()  # Dividir en palabras
            for i in range(len(words)):
                for j in range(i + 1, len(words) + 1):
                    phrase = ' '.join(words[i:j])  # Crear combinaciones de palabras
                    if contains_bad_words(phrase):
                        bad_words_found.append(phrase)
                        break  # Salir al encontrar una bad word

        if bad_words_found:
            unique_bad_words = list(set(bad_words_found))  # Eliminar duplicados
            messagebox.showinfo(f"Malas Palabras del {selected_date.strftime('%Y-%m-%d')}", "\n".join(unique_bad_words))
        else:
            messagebox.showinfo("Sin Registros", "No se han registrado malas palabras en esta fecha.")
    else:
        messagebox.showinfo("Sin Registros", "No se han registrado malas palabras en esta fecha.")

def add_bad_word():
    new_bad_word = new_bad_word_entry.get().strip()  # Obtener la nueva mala palabra
    if new_bad_word:  # Asegurarse de que no esté vacío
        BAD_WORDS.append(new_bad_word.lower())  # Agregar a la lista de malas palabras
        write_new_bad_word(new_bad_word)  # Guardar en el archivo
        messagebox.showinfo("Palabra Agregada", f"La palabra '{new_bad_word}' ha sido añadida a la lista de malas palabras.")
        new_bad_word_entry.delete(0, tk.END)  # Limpiar el campo de entrada
    else:
        messagebox.showwarning("Campo Vacío", "Por favor, introduce una palabra válida.")

def mark_calendar_days():
    today = datetime.now()
    for day in range(1, cal.monthrange(today.year, today.month)[1] + 1):
        filename = get_filename_for_date(today.year, today.month, day)
        if os.path.exists(filename):
            calendar.calevent_create(datetime(today.year, today.month, day), 'Registro', 'message')

def setup_gui():
    global calendar, result_text, new_bad_word_entry

    root = tk.Tk()
    root.title("SafeChildren - Monitoreo de Palabras Prohibidas")
    root.geometry("1024x768")
    root.config(bg="#f0f0f0")

    header_frame = tk.Frame(root, bg="#0078D7", height=80)
    header_frame.pack(fill="x")

    try:
        logo = tk.PhotoImage(file='logo.png')  # Asegúrate de tener un logo en el mismo directorio
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        logo = None  # Opcional: asignar una imagen predeterminada

    if logo:
        logo_label = tk.Label(header_frame, image=logo, bg="#0078D7")
        logo_label.image = logo  # Mantener una referencia al logo
        logo_label.pack(side="left", padx=20)

    title_label = tk.Label(header_frame, text="SafeChildren", font=("Segoe UI", 28, "bold"), bg="#0078D7", fg="#ffffff")
    title_label.pack(side="left", padx=10)

    body_frame = tk.Frame(root, bg="#f0f0f0")
    body_frame.pack(pady=20)

    result_text = tk.StringVar()
    result_text.set('Esperando análisis...')

    result_label = tk.Label(body_frame, textvariable=result_text, font=("Segoe UI", 16), bg="#f0f0f0", fg="#333333")
    result_label.pack(pady=10)

    calendar = Calendar(body_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    calendar.pack(pady=20)

    analyze_button = tk.Button(body_frame, text="Analizar", command=analyze_bad_words, bg="#007BFF", fg="#ffffff", font=("Segoe UI", 12))
    analyze_button.pack(pady=20)


    # Campo de entrada para nueva mala palabra
    new_bad_word_label = tk.Label(body_frame, text="Agregar Nueva Palabra Prohibida:", font=("Segoe UI", 14), bg="#f0f0f0")
    new_bad_word_label.pack(pady=10)

    new_bad_word_entry = tk.Entry(body_frame, font=("Segoe UI", 14), bd=2, relief="solid")
    new_bad_word_entry.pack(pady=10)

    # Función para hacer foco en el campo de entrada
    def focus_new_bad_word_entry(event):
        new_bad_word_entry.focus_set()  # Establecer el foco en el campo de entrada

    # Función para quitar el foco del campo de entrada
    def remove_focus(event):
        # Siempre quitar el foco cuando se hace clic en cualquier parte de la vista
        root.focus()  # Asegurar que el foco se quite del Entry

    # Asociar el clic en el label con el evento de foco
    new_bad_word_label.bind("<Button-1>", focus_new_bad_word_entry)

    # Asociar el clic en el body_frame con el evento para quitar el foco
    body_frame.bind("<Button-1>", remove_focus)

    # Función para agregar una nueva mala palabra y quitar el foco
    def add_bad_word():
        new_bad_word = new_bad_word_entry.get().strip()  # Obtener la nueva mala palabra
        if new_bad_word:  # Asegurarse de que no esté vacío
            BAD_WORDS.append(new_bad_word.lower())  # Agregar a la lista de malas palabras
            write_new_bad_word(new_bad_word)  # Guardar en el archivo
            messagebox.showinfo("Palabra Agregada", f"La palabra '{new_bad_word}' ha sido añadida a la lista de malas palabras.")
            new_bad_word_entry.delete(0, tk.END)  # Limpiar el campo de entrada
        else:
            messagebox.showwarning("Campo Vacío", "Por favor, introduce una palabra válida.")

        root.focus()  # Quitar el foco del campo de entrada después de agregar la palabra

    add_bad_word_button = tk.Button(body_frame, text="Agregar Palabra Prohibida", command=add_bad_word, bg="#007BFF", fg="#ffffff", font=("Segoe UI", 12))
    add_bad_word_button.pack(pady=10)

    

    mark_calendar_days()
    # Función para eliminar todas las malas palabras
    def clear_bad_words():
        global BAD_WORDS
        BAD_WORDS = []  # Vaciar la lista de malas palabras
        with open('badwords_list.txt', 'w') as file:  # Vaciar el archivo que guarda las malas palabras
            file.write('')  # Dejar el archivo vacío
        messagebox.showinfo("Lista Eliminada", "La lista de malas palabras ha sido eliminada.")

    # Crear el botón para eliminar todas las malas palabras
    clear_bad_words_button = tk.Button(body_frame, text="Eliminar palabras agregadas", command=clear_bad_words, bg="#FF0000", fg="#ffffff", font=("Segoe UI", 12))
    clear_bad_words_button.pack(pady=10)

    return root

def main():
    global calendar
    root = setup_gui()
    keyboard.on_press(on_key_press)
    root.mainloop()

if __name__ == "__main__":
    main()
    
