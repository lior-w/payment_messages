import tkinter as tk
from tkinter import filedialog, messagebox
from data import *
from owner_controller import OwnerController
from datetime import datetime
import os
from tkinter import Toplevel
from id_list import *


def sanitize_filename(filename):
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename


def create_and_save_files(dir_path, data, dfs, messages, output):
    current_time = datetime.now().strftime("%d_%m_%Y")
    new_dir_path = os.path.join(dir_path, f"הודעות לבעלים {current_time}")

    try:
        os.makedirs(new_dir_path, exist_ok=True)

        output_path = os.path.join(new_dir_path, 'output.xlsx')
        data.to_excel(output_path, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in saving output file: {e}")

    try:  
        for owner in dfs.keys():
            file_path = os.path.join(new_dir_path, f'{sanitize_filename(owner)}.xlsx')
            dfs[owner].to_excel(file_path, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in generating owners excel files: {e}")

    try:
        whatsapp_messages_file_path = os.path.join(new_dir_path, 'הודעות לוואטסאפ.txt')
        with open(whatsapp_messages_file_path, "w", encoding="utf-8") as f:
            for owner in messages.keys():
                print(f"####################\n{owner}\n####################\n\n{messages[owner]}\n\n", file=f)

        messagebox.showinfo("Success", f"{new_dir_path}הקבצים נשמרו בהצלחה בתיקייה ")
        os.startfile(new_dir_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in generating messages txt file: {e}")
    
    try:
        file_path = os.path.join(new_dir_path, 'טבלת בעלים-הודעות (ללא בעלים גדולים).xlsx')
        output.to_excel(file_path, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in generating output_msg file: {e}")




class FileHandler:
    def __init__(self, root):
        self.root = root
        self.owner_controller = OwnerController()
        self.data = None
        self.label = None
        self.entry = None
        self.button_import = None
        self.button_columns = None
        self.button_process = None
        self.vehicles_threshold_label = None
        self.vehicles_threshold_entry = None
        self.vehicles_threshold = 10
        self.sapak_check_box = None
        self.sapak_bool = tk.BooleanVar(value=True)
        self.id_lists = []
        self.label_lists = None
             
        self.cols_translate = {'מסגרת': "misgeret",
                               'מספר רישוי': "license",
                               'סוג רכב': "type",
                               'תאריך גיוס': "draft_date",
                               'תאריך שחרור': "release_date",
                               'תשלום אחרון': "last_pay_date",
                               'תחילת תשלום': "pay_from_date",
                               'תשלום עד': "pay_until_date",
                               'סכום לתשלום': "payment_amount",
                               'ח.פ. בעלים': "id_original",
                               'שם בעלים': "owner_name_original",
                               'ח.פ. חוכר': "id_rent",
                               'שם חוכר': "owner_name_rent",
                               'מספר ספק': "sapak"}
        
        self.cols_index = {'מסגרת': 2,
                               'מספר רישוי': 3,
                               'סוג רכב': 5,
                               'תאריך גיוס': 6,
                               'תאריך שחרור': 7,
                               'תשלום אחרון': 8,
                               'תחילת תשלום': 9,
                               'תשלום עד': 10,
                               'סכום לתשלום': 13,
                               'ח.פ. בעלים': 15,
                               'שם בעלים': 16,
                               'ח.פ. חוכר': 17,
                               'שם חוכר': 18,
                               'מספר ספק': 22}


    def create_widgets(self):
        self.label = tk.Label(self.root, text="קובץ פעימה")
        self.label.grid(row=0, column=2, pady=20, sticky='e')

        self.entry = tk.Entry(self.root, width=60)
        self.entry.grid(row=0, column=1, padx=10, pady=20)

        self.button_import = tk.Button(self.root, text="בחר קובץ",
                                              command=lambda entry=self.entry: self.import_file(entry))
        self.button_import.grid(row=0, column=0, padx=10, pady=20)

        self.vehicles_threshold_label = tk.Label(self.root, text="מספר כלים מינימלי לייצוא קובץ אקסל לבעלים")
        self.vehicles_threshold_label.grid(row=1, column=1, pady=10, sticky='e', columnspan=2)

        self.vehicles_threshold_entry = tk.Entry(self.root, width=5)
        self.vehicles_threshold_entry.insert(0, self.vehicles_threshold)
        self.vehicles_threshold_entry.grid(row=1, column=1, padx=(0, 250), pady=10, sticky='e', columnspan=2)
        self.vehicles_threshold_entry.bind("<KeyRelease>", self.on_entry_change)

        self.sapak_check_box = tk.Checkbutton(self.root, text='    הודעת "לקוח חדש" לבעלים ללא מספר ספק', variable=self.sapak_bool)
        self.sapak_check_box.grid(row=2, column=1, pady=10, sticky='e', columnspan=2)

        self.label_lists = tk.Label(self.root, text="")
        self.label_lists.grid(row=3, column=1, pady=(30, 0))

        self.button_columns = tk.Button(self.root, text="צביעת בעלים", command=self.open_new_list_window)
        self.button_columns.grid(row=4, column=0, pady=(10, 0), columnspan=3)

        self.button_columns = tk.Button(self.root, text="תיאום עמודות", command=self.open_columns_window)
        self.button_columns.grid(row=5, column=0, pady=(10, 0), columnspan=3)

        self.button_process = tk.Button(self.root, text="יצירת הודעות אוטומטית",
                                       command=self.load_data)
        self.button_process.grid(row=6, column=0, pady=(10, 0), columnspan=3)


    def open_new_list_window(self):
        window = Toplevel(self.root)
        window.title("צביעת בעלים")
        window.geometry("580x380")

        # Label for the Entry field
        label = tk.Label(window, text="רשימת חפ")
        label.grid(row=0, column=2, pady=20, sticky='e')

        # Entry field
        entry = tk.Entry(window, width=60)
        entry.grid(row=0, column=1, padx=10, pady=20)

        # Button to import file
        button_import = tk.Button(window, text="בחר קובץ",
                                command=lambda entry=entry: self.import_file(entry))
        button_import.grid(row=0, column=0, padx=(20,10), pady=20)

        label_header = tk.Label(window, text="שם הרשימה")
        label_header.grid(row=1, column=2, pady=20, sticky='e')

        # Entry field for header
        entry_header = tk.Entry(window, width=60)
        entry_header.grid(row=1, column=1, padx=10, pady=20)

        label_text = tk.Label(window, text="גוף ההודעה")
        label_text.grid(row=2, column=2, padx=(0, 0), sticky='e')

        # Text box for message
        text = tk.Text(window, wrap="word", width=45, height=10, border=1)
        text.grid(row=2, column=1, padx=(20, 20), sticky='e')

        # Complete button
        def complete():
            file_path = entry.get()
            header = entry_header.get()
            msg = text.get("1.0", tk.END).strip()  # Retrieve text from Text widget and remove trailing newline
            
            # Read Excel file into a DataFrame
            try:
                df = pd.read_excel(file_path, header=None)
                df.columns = ["id"]
                id_list = ID_list(df, header, msg)  # Create an instance of ID_list
                self.id_lists.append(id_list)
                headers = [l.get_header() for l in self.id_lists]
                self.label_lists.config(text="רשימות חפ: " + ", ".join(headers))
                print("ID_list created:", id_list.get_header())  # For debugging
                
            except Exception as e:
                print(f"Error: {e}")
            
            window.destroy()

        complete_button = tk.Button(window, text="הוסף", command=complete)
        complete_button.grid(row=3, column=0, padx=(0, 0), pady=40)

    def open_columns_window(self):
        window = Toplevel(self.root)
        window.title("עמודות")
        window.geometry("440x380")
        labels_cols = {}
        entries_cols = {}

        for i, col in enumerate(self.cols_index):
            r = i
            c = 3
            pad_r = 0
            if i >= 7:
                r -= 7
                c -= 2
                pad_r = 80

            labels_cols[col] = tk.Label(window, text=col)
            labels_cols[col].grid(row=r, column=c, padx=(0, pad_r), pady=10, sticky="e")
            entries_cols[col] = tk.Entry(window, width=5)
            entries_cols[col].grid(row=r, column=(c-1), padx=(30, 30), pady=10, sticky="e")
            entries_cols[col].insert(0, self.cols_index[col])

        def update_cols():
            for col, entry in entries_cols.items():
                try:
                    self.cols_index[col] = int(entry.get())
                except Exception:
                    messagebox.showwarning("Warning", "מספרי עמודות לא תקינים")
            window.destroy()

        compelte_button = tk.Button(window, text="עדכון מספרי עמודות", command=update_cols)
        compelte_button.grid(row=14, column=0, padx=(0,0), pady=40, columnspan=4)
        

    def on_entry_change(self, event):
        entry_widget = event.widget
        self.vehicles_threshold = entry_widget.get()


    def import_file(self, entry):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xls;*.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            entry.config(fg="black")


    def load_data(self):
        if self.entry.get() == "":
            messagebox.showwarning("Warning", "בחר קובץ כדי ליצור הודעות אוטומטיות")
        else:
            treshold = -1
            try:
                treshold = int(self.vehicles_threshold_entry.get())
                if treshold > 0:
                    try:
                        self.data = load_data(self.entry.get())
                        self.process_data(treshold)
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred: {e}")
                else:
                    messagebox.showwarning("Warning", "הכנס מספר גדול מאפס")
            except Exception:
                messagebox.showwarning("Warning", "מספר לא תקין")


    def process_data(self, treshold):
        if self.data is None:
            messagebox.showerror("Error", "יצירת ההודעות נכשלה")
            return
            
        try:
            self.data = prepare_data(self.data, self.cols_index, self.cols_translate)
        except Exception as e:
            messagebox.showerror("Error", "הקובץ לא בפורמט המתאים")
            return

        try:
            self.owner_controller.generate_owners(self.data, self.id_lists)
            dfs = {}
            messages = {}
            output = pd.DataFrame(columns=["id", "owner_name", "message"])
            for o in self.owner_controller.get_owners():
                if o.number_of_vehicles() >= treshold:
                    dfs[o.get_name()] = o.get_df()
                else:
                    messages[o.get_name()] = o.get_message(self.sapak_bool.get())
                    new_row = {"id": o.get_id(), "owner_name": o.get_name(), "message": o.get_message(self.sapak_bool.get())}
                    output.loc[len(output)] = new_row
            dir_path = filedialog.askdirectory()
            if dir_path:
                create_and_save_files(dir_path, self.data, dfs, messages, output)
                self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"process data {e}")