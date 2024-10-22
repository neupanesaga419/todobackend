import pandas as pd
from todos.models import Todo


def parse_todos(todos, user) -> list:
    todos_list = []
    print("Parsing todos")
    df = pd.read_excel(todos, sheet_name="Todos")

    for index, row in df.iterrows():
        todo = {
            "title": row["Title"],
            "description": row["Description"],
            "created_by": user.id,
        }
        if not pd.isna(row["Status"]):
            todo["status"] = row["Status"]

        if not pd.isna(row["Completed"]):
            todo["completed"] = row["Completed"]

        todos_list.append(todo)

    return todos_list
