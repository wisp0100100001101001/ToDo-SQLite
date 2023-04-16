import datetime
import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS todos
            (id INTEGER PRIMARY KEY, text TEXT, date TEXT, deadline TEXT)''')
        self.conn.commit()

    def add_db(self, todo):
        self.cur.execute("INSERT INTO todos(text, date, deadline) VALUES (?, ?, ?)", (todo.text, todo.date, todo.deadline))
        self.conn.commit()
        print("\nToDo Successfully Added!")

    def edit_db(self, id, newTodo):
        self.cur.execute("UPDATE todos SET text = ?, deadline = ? WHERE id = ?", (newTodo.text, newTodo.deadline, id))
        self.conn.commit()
        print("\nToDo Successfully Edited!")

    def delete_db(self, id):
        self.cur.execute("DELETE FROM todos WHERE id=?", (id,))
        self.conn.commit()
        print("\nToDo Successfully Deleted!")

    def getAll(self):
        self.cur.execute("SELECT * FROM todos")
        rows = self.cur.fetchall()
        return rows


class Manager:
    def __init__(self, database):
        self.database = database

    def add(self, todo, deadline):
        try:
           deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
        except ValueError:
           print("Enter the deadline correctly!")
           return

        todo = Todo(todo, datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), deadline)
        self.database.add_db(todo)

    def edit(self, id, newTodo):
        self.database.edit_db(id, newTodo)

    def delete(self, id):
        self.database.delete_db(id)

    def checkData(self):
        return len(self.database.getAll())

    def showAll(self):
        entries = self.database.getAll()

        for index, item in enumerate(entries, 1):
            print("\n")
            print("-" * 25 + str(index) + "-" * 25)
            print(Todo.from_row(item))
            print("-" * 51)


class Todo:
    def __init__(self, text, date, deadline):
        self.text = text
        self.date = date
        try:
            self.deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
        except ValueError:
            print("Enter the deadline correctly!")
            self.deadline = None

    @classmethod
    def from_row(cls, row):
        return cls(row[1], row[2], row[3])

    def __str__(self):
        if self.deadline:
            return f"Date: {self.date}\nToDo: {self.text}\nDeadline: {self.deadline}"
        else:
            return f"Date: {self.date}\nToDo: {self.text}\nDeadline: Invalid deadline format"


def menu():
    choice = None
    database = Database("todos.db")
    manager = Manager(database)

    while choice != "q":
        print("\nToDo App Menu:")
        print("a) Add")
        print("e) Edit")
        print("d) Delete")
        print("s) Show All")
        print("q) Quit")

        choice = input("\nAction: ")

        if choice == "a":
            text = input("ToDo: ")
            deadline = input("Deadline (dd/mm/yyyy hh:mm): ")
            manager.add(text, deadline)

        elif choice == "e":
            
            if manager.checkData():
                
                manager.showAll()
                while True:
                    
                    todoIndex = input("Choose the index: ")
                    if not todoIndex.isdigit() or int(todoIndex) not in range(1, len(manager.database.entries)+1):
                         print("Enter a valid index!")
                         continue

                    text = input("Text for new ToDo for edit: ")
                    deadline = input("Deadline (dd/mm/yyyy hh:mm): ")
                    newTodo = Todo(text, deadline)

                    oldTodoIndex = int(todoIndex) - 1

                    manager.edit(oldTodoIndex, newTodo)
                    break


            else:
                print("There is no DATA in DB!")

            

        elif choice == "d":
          if manager.checkData():
             manager.showAll()
             while True:
                 try:
                    todoIndex = int(input("Choose the index for delete: "))
                    if todoIndex not in range(1, len(manager.database.entries)+1):
                       print("Enter a valid index!")
                       continue
                    manager.delete(todoIndex-1)
                    break
                 except ValueError:
                    print("Enter a valid index!")
                    continue
          else:
             print("There is no DATA in DB!")
 

        elif choice == "s":
            manager.showAll()
        
        elif choice == "q":
            print("See you soon!")
            	
        else:
            print("Unknown command!")


menu()
