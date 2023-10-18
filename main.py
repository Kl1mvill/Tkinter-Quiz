from tkinter import ttk
import tkinter as tk
import json

# Открывает файл “Quizzes.json” для чтения в кодировке “UTF-8”.
# Читает содержимое файла и сохраняет в словарь “quizzes”.
with open('Quizzes.json', "r", encoding="utf-8") as json_file:
    quizzes = json.load(json_file)


# Функция удаления радиокнопки.
# Каждую кнопку в списке "option_buttons" удаляет из интерфейса.
def removal_radiobutton(option_buttons):
    for button in option_buttons:
        button.pack_forget()


class Quiz:
    def __init__(self, root):
        "Настройки окна"
        self.root = root
        self.root.title('Викторина')
        self.root.geometry('500x400')
        self.root.configure(bg="#12335a")

        "Переменные"
        self.quiz_options = tk.StringVar()  # Будем использовать для выбора варианта викторины.

        # Перебирает все ключи словаря quizzes и устанавливаем значение переменной quiz_options.
        for i in quizzes.keys():
            self.quiz_options.set(i)

        "Стили"
        style = ttk.Style()

        style.configure("BigFont.TLabel", font=("Helvetica", 24), background='#12335a')
        style.configure("SmallFont.TLabel", font=("Helvetica", 13), background='#12335a')
        style.configure("Standard.TButton", font=("Helvetica", 15), background='#235481', activebackground="#326896")
        style.configure("Standard.TRadiobutton", font=("Helvetica", 20), background='#12335a')

        # Меню
        self.home_label = ttk.Label(text="Викторина", style="BigFont.TLabel")  # Выводится большое слово "Викторина"

        self.start_btn = ttk.Button(text="Начать", style="Standard.TButton",
                                    command=self.choosing_quiz)  # Кнопка для начала игры

        self.exit_btn = ttk.Button(text="Выход", style="Standard.TButton", command=self.root.quit)  # Кнопка выход

        # Выбор викторины
        self.quiz_dropdown = tk.OptionMenu(self.root, self.quiz_options, *quizzes.keys())  # Меню для выбора викторины
        self.quiz_dropdown.config(font=("Helvetica", 15), background='#235481', activebackground="#326896")

        self.show_button = ttk.Button(style="Standard.TButton",
                                      text="Вывести викторину")  # Кнопка которая запускает выбранную викторину

        # Викторина
        self.name_quiz_lbl = ttk.Label(style="BigFont.TLabel")  # Название викторины
        self.question_lbl = ttk.Label(text="Какой-то вопрос", style="SmallFont.TLabel")  # Вопрос викторины
        self.submit_button = ttk.Button(text="Далее",
                                        style="Standard.TButton")  # Кнопка для перехода на следующий вопрос

        self.option_buttons = []  # Список для хранения кнопок
        self.option_var = tk.IntVar()  # Целочисленная переменная для радиокнопок

        self.question_idx = 0  # Номер вопроса
        self.counter = 0  # Количество баллов

        # Вывод результата викторины
        self.end_lbl = ttk.Label(text="Количество баллов набранное в викторине", style="SmallFont.TLabel")
        self.repeat_btn = ttk.Button(text="Заново", style="Standard.TButton")  # Кнопка для перезапуска викторины
        self.home_btn = ttk.Button(text="Домой", style="Standard.TButton",
                                   command=self.menu)  # Кнопка для перехода в меню

        self.check = False  # Проверка на прохождение викторины.

        self.menu()

    def menu(self):
        # Проверка была ли пройдена викторина хотя бы раз. Если ДА то обновляем переменные и удаляем виджеты.
        if self.check:
            self.counter = 0  # Анулируем баллы
            self.question_idx = 0

            for object_name in [self.end_lbl, self.repeat_btn, self.home_btn, self.name_quiz_lbl]:
                object_name.pack_forget()

        # Создаем элементы интерфейса
        self.home_label.pack()
        self.start_btn.pack()
        self.exit_btn.pack()

    # Выбор викторины
    def choosing_quiz(self):
        # Удаление виджетов
        destroy_object = [self.home_label, self.start_btn, self.exit_btn]

        for object_name in destroy_object:
            object_name.pack_forget()

        self.quiz_dropdown.pack()  # Меню для выбора викторины

        # Кнопка, которая запускает выбранную викторину
        self.show_button.config(command=lambda: self.show_quiz(self.quiz_options.get()))
        self.show_button.pack()

    # Викторина
    def show_quiz(self, quiz_name: str, selected_response=None, answer=None, response_options=None):
        # Удаление виджетов
        destroy_object = [self.quiz_dropdown, self.show_button, self.home_btn, self.repeat_btn, self.end_lbl,
                          self.submit_button]

        for object_name in destroy_object:
            object_name.pack_forget()

        # Проверка ответов. И запись количества правильных ответов
        if self.question_idx != 0:
            if response_options[selected_response] == answer:
                self.counter += 1
            removal_radiobutton(self.option_buttons)  # Скрываем каждую радиокнопку

        # Проверка закончилась ли викторина
        if self.question_idx == len(quizzes[quiz_name]):
            self.end_quiz(quiz_name)
            return

        # Получаем вопрос, варианты ответа и ответ
        questions = quizzes[quiz_name][self.question_idx]["question"]
        response_options = quizzes[quiz_name][self.question_idx]["options"]
        answer = quizzes[quiz_name][self.question_idx]["answer"]

        # Название викторины
        self.name_quiz_lbl.config(text=f"{quiz_name}")
        self.name_quiz_lbl.pack()

        # Сам вопрос
        self.question_lbl.config(text=questions)
        self.question_lbl.pack()

        # Создание радиокнопок с вариантами ответа
        for i, option in enumerate(response_options):
            button = ttk.Radiobutton(text=option, variable=self.option_var, value=i, style="Standard.TRadiobutton")
            self.option_buttons.append(button)
            button.pack()

        self.question_idx += 1  # Для перехода на следующий вопрос

        # Кнопка далее
        self.submit_button.config(
            command=lambda: self.show_quiz(quiz_name, self.option_var.get(), answer, response_options))
        self.submit_button.pack()

    def end_quiz(self, quiz_name):
        # Удаление виджетов и радиокнопок
        destroy_object = [self.quiz_dropdown, self.show_button, self.question_lbl, self.submit_button]
        removal_radiobutton(self.option_buttons)

        for object_name in destroy_object:
            object_name.pack_forget()

        self.check = True  # Проверка была ли пройдена викторина хоть раз

        if self.counter == 0:
            self.end_lbl.config(text=f"В этой викторине вы набрали ноль баллов!")
        elif self.counter % 10 == 1:
            self.end_lbl.config(text=f"В этой викторине вы получили {self.counter} бал")
        elif self.counter % 10 < 5:
            self.end_lbl.config(text=f"В этой викторине вы получили {self.counter} балла")
        else:
            self.end_lbl.config(text=f"В этой викторине вы получили {self.counter} балов")

        # Добавляем строку с кол. баллов и кнопку домой
        self.end_lbl.pack()
        self.home_btn.pack()

        # Кнопка для повторения викторины
        self.repeat_btn.config(command=lambda: self.show_quiz(quiz_name))
        self.repeat_btn.pack()


if __name__ == "__main__":
    app = tk.Tk()  # Создаем экземпляр класса
    quiz = Quiz(app)  # Создаем экземпляр класса Quiz
    app.mainloop()  # Запускаем бесконечный цикл
