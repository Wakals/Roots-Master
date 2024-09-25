import random
import tkinter as tk
from tkinter import messagebox

class Review:
    def __init__(self, data, parent_frame):
        self.data = data['roots']
        self.errors = self.load_errors()
        self.parent_frame = parent_frame
        self.current_question = 0
        self.current_root = None

    def load_errors(self):
        try:
            with open('logs/errors.log', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []

    def start_review(self):
        if not self.errors:
            messagebox.showinfo("提示", "没有错题可以复习！")
            return

        self.current_question = 0
        self.show_next_question()

    def show_next_question(self):
        if self.current_question < len(self.errors):
            error_info = self.errors[self.current_question]
            root_info = self.parse_error_info(error_info)
            self.current_root = self.get_root_by_name(root_info['root'])
            self.ask_root_question(self.current_root)
        else:
            self.finish_review()

    def parse_error_info(self, error_info):
        parts = error_info.split(' - ')
        root = parts[0].split(': ')[1].strip()
        wrong_answer = parts[1].split(': ')[1].strip()
        return {'root': root, 'wrong_answer': wrong_answer}

    def get_root_by_name(self, root_name):
        return next((root for root in self.data if root['root'] == root_name), None)

    def ask_root_question(self, root):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        question_label = tk.Label(self.parent_frame, text=f"词根: {root['root']}", font=("Arial", 14), bg='#f0f0f0')
        question_label.pack(pady=10)

        options = self.get_meaning_options(root['meaning'])
        self.var = tk.StringVar(value=options[0])

        for option in options:
            radio = tk.Radiobutton(self.parent_frame, text=option, variable=self.var, value=option, bg='#f0f0f0', font=("Arial", 12))
            radio.pack(anchor='w')

        submit_button = tk.Button(self.parent_frame, text="提交", command=self.check_root_answer, width=15, height=2, font=("Arial", 12))
        submit_button.pack(pady=10)

    def check_root_answer(self):
        answer = self.var.get()
        if answer == self.current_root['meaning']:
            messagebox.showinfo("正确", "正确！")
            self.current_question += 1
            self.show_next_question()
        else:
            messagebox.showerror("错误", "错误，请再试一次。")

    def finish_review(self):
        messagebox.showinfo("完成", "复习结束！")
        self.parent_frame.destroy()

    def get_meaning_options(self, correct_meaning):
        meanings = [correct_meaning]
        while len(meanings) < 4:
            option = random.choice(self.data)['meaning']
            if option not in meanings:
                meanings.append(option)
        random.shuffle(meanings)
        return meanings
