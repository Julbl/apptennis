import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# создание базы данных
conn = sqlite3.connect('players.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS players
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fio TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS matches
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 player1 INTEGER NOT NULL,
                 player2 INTEGER NOT NULL,
                 result TEXT NOT NULL,
                 FOREIGN KEY(player1) REFERENCES players(id),
                 FOREIGN KEY(player2) REFERENCES players(id))''')
conn.commit()

# создание окна
root = Tk()
root.title("Игроки и матчи")

img = Image.open("background.jpg")
img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
img = ImageTk.PhotoImage(img)

# создание фона
bg_label = Label(root, image=img)
bg_label.place(x=0, y=0)

# задание прозрачности фона
bg_label.configure(bg='gray50')

# функция для добавления нового игрока
def add_player():
    fio = fio_entry.get()
    cursor.execute('''INSERT INTO players (fio) VALUES (?)''', (fio,))
    conn.commit()
    fio_entry.delete(0, END)


# функция для удаления игрока из базы данных и таблицы
def delete_player(tree):
    selected_item = tree.focus()
    if selected_item:
        player_id = tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players WHERE id=?", (player_id,))
        conn.commit()
        conn.close()
        # Обновить таблицу, чтобы она отображала актуальные данные
        update_players_table(tree)

# функция для вывода списка всех игроков в таблицу
def update_players_table(tree):
    # очищаем таблицу от старых данных
    tree.delete(*tree.get_children())

    # Заполняем таблицу из базы данных
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    data = c.fetchall()
    # добавляем данные в таблицу
    for player in data:
        tree.insert('', 'end', values=(player[0], player[1], 'Удалить'), tags=('player',))

    # Назначить функцию удаления записи на кнопку в каждой строке таблицы
    tree.tag_bind('player', '<Button-1>', lambda event: delete_player(tree))

# функция для вывода списка всех игроков
def show_players():
    # создание нового окна
    players_window = Toplevel(root)
    players_window.title("Список игроков")

    tree = ttk.Treeview(players_window, columns=('ID Players', 'FIO', 'Delete'))
    tree.heading('#0', text='ID участника')
    tree.heading('#1', text='ФИО')
    tree.heading('#2', text='Удалить')

    # заполнение таблицы
    update_players_table(tree)

    tree.pack()


# функция для добавления результата матча
def add_match():
    player1_id = player1_entry.get()
    player2_id = player2_entry.get()
    result = result_entry.get()
    cursor.execute('''INSERT INTO matches (player1, player2, result) VALUES (?, ?, ?)''',
                   (player1_id, player2_id, result))
    conn.commit()
    player1_entry.delete(0, END)
    player2_entry.delete(0, END)
    result_entry.delete(0, END)


def delete_match(tree):
    selected_item = tree.focus()
    if selected_item:
        match_number = tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matches WHERE id=?", (match_number,))
        conn.commit()
        conn.close()
        # очистить виджет tree от старых данных
        for item in tree.get_children():
            tree.delete(item)
        # обновить таблицу, чтобы она отображала актуальные данные
        view_matches()


# Функция для отображения таблицы с историей матчей
def view_matches():
    # Создать окно для таблицы истории матчей
    match_window = Toplevel(root)
    match_window.title("История матчей")

    # Создать таблицу
    tree = ttk.Treeview(match_window, columns=(
        'Match ID', 'Player 1', 'Player 2', 'Result', 'Delete'))
    tree.heading('#0', text='Номер матча')
    tree.heading('#1', text='Игрок 1')
    tree.heading('#2', text='Игрок 2')
    tree.heading('#3', text='Результат матча')
    tree.heading('#4', text='Удалить')

    # Заполнить таблицу данными из базы данных
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute("SELECT * FROM matches")
    data = c.fetchall()
    for match in data:
        result = match[3]
        if result.split(':')[0] > result.split(':')[1]:
            result = 'Победа первого'
        elif result.split(':')[0] < result.split(':')[1]:
            result = 'Победа второго'
        else:
            result = 'Ничья'
            # Получить ФИО игроков по их ID
        #c.execute("SELECT name FROM players WHERE id=?", (match[1],))
        #player1 = c.fetchone()[0]
        #c.execute("SELECT name FROM players WHERE id=?", (match[2],))
        #player2 = c.fetchone()[0]

        tree.insert('', 'end', values=(match[0], match[1], match[2], result, 'Удалить'), tags=('match',))

    # Назначить функцию удаления записи на кнопку в каждой строке таблицы
    tree.tag_bind('match', '<Button-1>', lambda event: delete_match(tree))

    tree.pack()


# создание элементов интерфейса
player_frame = LabelFrame(root, text="Новый игрок")
player_frame.pack(padx=10, pady=10)
fio_label = Label(player_frame, text="ФИО:")
fio_label.grid(row=0, column=0, padx=5, pady=5)
fio_entry = Entry(player_frame)
fio_entry.grid(row=0, column=1, padx=5, pady=5)
add_button = Button(player_frame, text="Добавить игрока", command=add_player)
add_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

show_frame = LabelFrame(root, text="Список игроков")
show_frame.pack(padx=10, pady=10)
show_button = Button(show_frame, text="Показать список игроков", command=show_players)
show_button.pack(padx=5, pady=5)


match_frame = LabelFrame(root, text="Новый матч")
match_frame.pack(padx=10, pady=10)
player1_label = Label(match_frame, text="Игрок 1 (ID):")
player1_label.grid(row=0, column=0, padx=5, pady=5)
player1_entry = Entry(match_frame)
player1_entry.grid(row=0, column=1, padx=5, pady=5)
player2_label = Label(match_frame, text="Игрок 2 (ID):")
player2_label.grid(row=1, column=0, padx=5, pady=5)
player2_entry = Entry(match_frame)
player2_entry.grid(row=1, column=1, padx=5, pady=5)
result_label = Label(match_frame, text="Результат:")
result_label.grid(row=2, column=0, padx=5, pady=5)
result_entry = Entry(match_frame)
result_entry.grid(row=2, column=1, padx=5, pady=5)
add_match_button = Button(match_frame, text="Добавить матч", command=add_match)
add_match_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

history_frame = LabelFrame(root, text="История матчей")
history_frame.pack(padx=10, pady=10)
history_button = tk.Button(root, text="Посмотреть историю матчей", command=view_matches)
history_button.pack(padx=10, pady=10)

root.mainloop()