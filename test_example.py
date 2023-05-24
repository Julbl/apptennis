import unittest
import sqlite3
from tkinter import ttk

# Импортируйте функции, которые нужно протестировать
from main import add_player, delete_player, update_players_table, show_players, add_match, delete_match, view_matches


class TestPlayerManagement(unittest.TestCase):

    def setUp(self):
        # Подготовка к тестированию: создание временной базы данных
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE players
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               fio TEXT NOT NULL)''')

    def tearDown(self):
        # Завершение тестирования: закрытие соединения с базой данных
        self.cursor.close()
        self.conn.close()

    def test_add_player(self):
        # Проверка функции добавления нового игрока
        add_player()
        self.cursor.execute("SELECT COUNT(*) FROM players")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 1)

    def test_delete_player(self):
        # Проверка функции удаления игрока
        # Предварительно добавляем игрока в базу данных
        self.cursor.execute("INSERT INTO players (fio) VALUES ('John Doe')")
        self.conn.commit()

        # Создаем Treeview и вставляем игрока
        tree = ttk.Treeview()
        tree.insert('', 'end', values=(1, 'John Doe', 'Удалить'), tags=('player',))

        # Вызываем функцию удаления игрока
        delete_player(tree)

        # Проверяем, что игрок был удален из базы данных и таблицы
        self.cursor.execute("SELECT COUNT(*) FROM players")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 0)

        self.cursor.execute("SELECT COUNT(*) FROM players WHERE id=1")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 0)

    def test_update_players_table(self):
        # Проверка функции обновления таблицы игроков
        # Добавляем несколько игроков в базу данных
        self.cursor.execute("INSERT INTO players (fio) VALUES ('John Doe')")
        self.cursor.execute("INSERT INTO players (fio) VALUES ('Jane Smith')")
        self.conn.commit()

        # Создаем Treeview и вызываем функцию обновления таблицы
        tree = ttk.Treeview()
        update_players_table(tree)

        # Проверяем, что таблица была заполнена данными
        self.assertEqual(tree.get_children(), ('',))
        self.assertEqual(tree.item('', 'values'), (1, 'John Doe', 'Удалить'))

    def test_add_match(self):
        # Проверка функции добавления нового матча
        add_match()
        self.cursor.execute("SELECT COUNT(*) FROM matches")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 1)

    def test_delete_match(self):
        # Проверка функции удаления матча
        # Предварительно добавляем матч в базу данных
        self.cursor.execute("INSERT INTO matches (player1, player2, result) VALUES (1, 2, '2:0')")
        self.conn.commit()

        # Создаем Treeview и вставляем матч
        tree = ttk.Treeview()
        tree.insert('', 'end', values=(1, 1))

    def test_show_players(self):
        # Проверка функции отображения списка игроков
        # Добавляем несколько игроков в базу данных
        self.cursor.execute("INSERT INTO players (fio) VALUES ('John Doe')")
        self.cursor.execute("INSERT INTO players (fio) VALUES ('Jane Smith')")
        self.conn.commit()

        # Создаем Toplevel окно и вызываем функцию отображения списка игроков
        players_window = ttk.tkinter.Toplevel()
        show_players()

        # Проверяем, что окно открылось и таблица была заполнена данными
        self.assertEqual(players_window.winfo_exists(), 1)
        self.assertEqual(len(players_window.winfo_children()),
                         1)  # Проверка наличия только одного дочернего элемента (Treeview)

    def test_view_matches(self):
        # Проверка функции отображения истории матчей
        # Добавляем несколько матчей в базу данных
        self.cursor.execute("INSERT INTO matches (player1, player2, result) VALUES (1, 2, '2:0')")
        self.cursor.execute("INSERT INTO matches (player1, player2, result) VALUES (3, 4, '1:1')")
        self.conn.commit()

        # Создаем Toplevel окно и вызываем функцию отображения истории матчей
        match_window = ttk.tkinter.Toplevel()
        view_matches()

        # Проверяем, что окно открылось и таблица была заполнена данными
        self.assertEqual(match_window.winfo_exists(), 1)
        self.assertEqual(len(match_window.winfo_children()),
                         1)  # Проверка наличия только одного дочернего элемента (Treeview)
