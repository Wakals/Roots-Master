import random
import json
import tkinter as tk
from tkinter import simpledialog, messagebox

class Quiz:
    def __init__(self, data, parent_frame, return_to_main):
        self.data = data['roots']
        self.errors = []
        self.parent_frame = parent_frame
        self.current_root = None
        self.current_question = 0
        self.selected_roots = []
        self.return_to_main = return_to_main

    def start_quiz(self):
        self.ask_initial()

    def ask_initial(self):
        letter = simpledialog.askstring("输入首字母或页面数字", "请输入首字母（a-z）或页面数字：")
        if letter is None:
            return

        num_words = simpledialog.askinteger("输入词数", "请输入测试的词数（例如30）：")
        if num_words is None:
            return

        filtered_roots = [root for root in self.data if root['letter'] == letter or str(root['page']) == letter]
        random.shuffle(filtered_roots)
        self.selected_roots = filtered_roots[:num_words]

        self.current_question = 0
        self.show_next_question()

    def show_next_question(self):
        if self.current_question < len(self.selected_roots):
            root = self.selected_roots[self.current_question]
            self.ask_root_question(root)
        else:
            self.finish_quiz()

    def ask_root_question(self, root):
        self.current_root = root
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        question_label = tk.Label(self.parent_frame, text=f"词根: {root['root']}", font=("Arial", 14), bg='#f0f0f0')
        question_label.pack(pady=10)

        options = self.get_meaning_options(root['meaning'])
        self.var = tk.StringVar(value=options[0])

        for option in options:
            radio = tk.Radiobutton(self.parent_frame, text=option, variable=self.var, value=option, bg='#f0f0f0', font=("Arial", 20))
            radio.pack(anchor='w')

        submit_button = tk.Button(self.parent_frame, text="提交", command=self.check_root_answer, width=25, height=3, font=("Arial", 18))
        submit_button.pack(pady=10)

    def check_root_answer(self):
        answer = self.var.get()
        if answer == self.current_root['meaning']:
            self.ask_example_question(self.current_root, self.current_root['examples'])
        else:
            messagebox.showerror("错误", "错误，请再试一次。")
            self.errors.append(f"词根: {self.current_root['root']} - 选择了错误的释义: {answer}")

    def ask_example_question(self, root, rest_examples):
        random.shuffle(rest_examples)
        example = rest_examples[0]
        rest_examples = rest_examples[1:]
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        example_label = tk.Label(self.parent_frame, text=f"例子: {example['word']}", font=("Arial", 14), bg='#f0f0f0')
        example_label.pack(pady=10)

        options = self.get_meaning_options(example['meaning_cn'], is_root=False)
        self.var = tk.StringVar(value=options[0])

        for option in options:
            radio = tk.Radiobutton(self.parent_frame, text=option, variable=self.var, value=option, bg='#f0f0f0', font=("Arial", 20))
            radio.pack(anchor='w')

        submit_button = tk.Button(self.parent_frame, text="提交", command=lambda: self.check_example_answer(example, rest_examples), width=25, height=3, font=("Arial", 18))
        submit_button.pack(pady=10)

    def check_example_answer(self, example, rest_examples):
        answer = self.var.get()
        if answer == example['meaning_cn']:
            if len(rest_examples) == 0:
                self.current_question += 1
                self.show_next_question()
            else:
                self.ask_example_question(self.current_root, rest_examples)
        else:
            messagebox.showerror("错误", "错误，请再试一次。")
            self.errors.append(f"例子: {example['word']} - 选择了错误的释义: {answer}")

    def finish_quiz(self):
        if self.errors:
            with open('logs/errors.log', 'w', encoding='utf-8') as f:
                for error in self.errors:
                    f.write(f"{error}\n")
        messagebox.showinfo("完成", "测试结束！")

        self.return_to_main()


    def get_meaning_options(self, correct_meaning, is_root=True):
        meanings = [correct_meaning]
        while len(meanings) < 4:
            if is_root:
                option = random.choice(self.data)['meaning']
            else:
                option = random.choice(self.data[0]['examples'])['meaning_cn']
            if option not in meanings:
                meanings.append(option)
        random.shuffle(meanings)
        return meanings
