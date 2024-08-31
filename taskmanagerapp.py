import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Application")
        self.root.geometry("600x500")

        self.list_of_tasks = []

        self.load_the_tasks()

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

        self.add_button = tk.Button(root, text="Add a Task", width=15, command=self.add_task)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete a Task", width=15, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update a Task", width=15, command=self.update_task)
        self.update_button.pack(pady=5)

        self.mark_complete_button = tk.Button(root, text="Mark the task as complete", width=15, command=self
                                              .mark_as_complete)
        self.mark_complete_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=70, height=10)
        self.task_listbox.pack(pady=10)
        self.task_listbox.bind('<<ListboxSelect>>', self.show_task_details)

        self.populateListbox()

    def add_task(self):
        task_name = self.task_entry.get().strip()
        priority = self.priority_combobox.get()
        due_date = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid date in YYYY-MM-DD format. (Year, Month, Day)")
            return

        if task_name:
            task = {
                "name": task_name,
                "priority": priority,
                "due_date": due_date,
                "status": "Incomplete"
            }
            self.list_of_tasks.append(task)
            self.save_the_tasks()
            self.populateListbox()

            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.task_entry.focus_set()
        else:
            messagebox.showwarning("Warning", "Enter a task name.")

    def delete_task(self):
        index_of_the_selected_task = self.task_listbox.curselection()
        if index_of_the_selected_task:
            del self.list_of_tasks[index_of_the_selected_task[0]]
            self.save_the_tasks()
            self.populateListbox()
        else:
            messagebox.showwarning("Warning", "You did not select a task to delete.")

    def update_task(self):
        index_of_the_selected_task = self.task_listbox.curselection()
        if index_of_the_selected_task:
            task = self.list_of_tasks[index_of_the_selected_task[0]]
            task["name"] = self.task_entry.get()
            task["priority"] = self.priority_combobox.get()
            due_date = self.due_date_entry.get()

            try:
                task["due_date"] = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid date in YYYY-MM-DD format.")
                return

            self.save_the_tasks()
            self.populateListbox()
        else:
            messagebox.showwarning("Warning", "You have not selected a task.")

    def mark_as_complete(self):
        index_of_the_selected_task = self.task_listbox.curselection()
        if index_of_the_selected_task:
            self.list_of_tasks[index_of_the_selected_task[0]]["status"] = "Complete"
            self.save_the_tasks()
            self.populateListbox()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as complete.")

    def show_task_details(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.list_of_tasks[selected_task_index[0]]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["name"])
            self.priority_combobox.set(task["priority"])
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, task["due_date"])

    def populateListbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.list_of_tasks:
            if self.filter_var.get() == "All" or self.filter_var.get() == task["status"]:
                self.task_listbox.insert(tk.END,
                                         f"{task['name']} - {task['priority']} - {task['due_date']} "
                                         f"- {task['status']}")

    def save_the_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.list_of_tasks, f, indent=4)

    def load_the_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.list_of_tasks = json.load(f)
        except FileNotFoundError:
            self.list_of_tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
