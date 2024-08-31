import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Application")
        self.root.geometry("600x500")

        self.tasks = []

        self.load_tasks()

        tk.Label(root, text="Task Name:").pack(pady=5)
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=5)

        tk.Label(root, text="Priority:").pack(pady=5)
        self.priority_combobox = ttk.Combobox(root, values=["High", "Medium", "Low"], state="readonly", width=37)
        self.priority_combobox.current(1)
        self.priority_combobox.pack(pady=5)

        tk.Label(root, text="Due Date (YYYY-MM-DD):").pack(pady=5)
        self.due_date_entry = tk.Entry(root, width=40)
        self.due_date_entry.pack(pady=5)

        self.filter_var = tk.StringVar(value="All")
        tk.Label(root, text="Filter by Status:").pack(pady=5)
        ttk.Combobox(root, textvariable=self.filter_var, values=["All", "Complete", "Incomplete"], state="readonly",
                     width=37).pack(pady=5)

        # Buttons
        self.add_button = tk.Button(root, text="Add Task", width=15, command=self.add_task)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", width=15, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Task", width=15, command=self.update_task)
        self.update_button.pack(pady=5)

        self.mark_complete_button = tk.Button(root, text="Mark as Complete", width=15, command=self.mark_as_complete)
        self.mark_complete_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=70, height=10)
        self.task_listbox.pack(pady=10)
        self.task_listbox.bind('<<ListboxSelect>>', self.show_task_details)

        self.populate_listbox()

    def add_task(self):
        task_name = self.task_entry.get().strip()
        priority = self.priority_combobox.get()
        due_date = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")
            return

        if task_name is not None:
            task = {
                "name": task_name,
                "priority": priority,
                "due_date": due_date,
                "status": "Incomplete"
            }
            self.tasks.append(task)
            self.save_tasks()
            self.populate_listbox()

            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.task_entry.focus_set()
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.save_tasks()
            self.populate_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task["name"] = self.task_entry.get()
            task["priority"] = self.priority_combobox.get()
            due_date = self.due_date_entry.get()

            try:
                task["due_date"] = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")
                return

            self.save_tasks()
            self.populate_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to update.")

    def mark_as_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]["status"] = "Complete"
            self.save_tasks()
            self.populate_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.")

    def show_task_details(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["name"])
            self.priority_combobox.set(task["priority"])
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, task["due_date"])

    def populate_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if self.filter_var.get() == "All" or self.filter_var.get() == task["status"]:
                self.task_listbox.insert(tk.END,
                                         f"{task['name']} - {task['priority']} - {task['due_date']} - {task['status']}")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
