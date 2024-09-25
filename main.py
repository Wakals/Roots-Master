import json
import tkinter as tk
from tkinter import messagebox
from quiz import Quiz
from review import Review

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("词根记忆助手")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        self.load_data()

        self.label = tk.Label(root, text="选择操作:", font=("Arial", 16), bg='#f0f0f0')
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="开始测试", command=self.start_quiz, width=40, height=4, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.review_button = tk.Button(root, text="复习错题", command=self.start_review, width=40, height=4, font=("Arial", 12))
        self.review_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="退出", command=root.quit, width=40, height=4, font=("Arial", 12))
        self.quit_button.pack(pady=10)

    def load_data(self):
        with open('data/roots_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def start_quiz(self):
        quiz = Quiz(self.data, self.root, self.return_to_main)
        quiz.start_quiz()

    def start_review(self):
        review = Review(self.data, self.root)
        review.start_review()

    def return_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.label = tk.Label(root, text="选择操作:", font=("Arial", 16), bg='#f0f0f0')
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="开始测试", command=self.start_quiz, width=20, height=2, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.review_button = tk.Button(root, text="复习错题", command=self.start_review, width=20, height=2, font=("Arial", 12))
        self.review_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="退出", command=root.quit, width=20, height=2, font=("Arial", 12))
        self.quit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
