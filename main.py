from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

# Taskクラス
class Task:
    next_task_id = 1
    
    def __init__(self, title: str):
        self.task_id = self.next_task_id
        Task.next_task_id += 1
        self.title = title
        self.isDone = False
        
app = FastAPI()
tasks: dict[int, Task] = {1: Task("洗濯物"), 2: Task("掃除機")}

# Depends
def task_db():
    return tasks

# GET（単）
@app.get("/todo/{task_id}")
def get_todo_byId(task_id: int, db: dict = Depends(task_db)):
    if task_id not in db:
        raise HTTPException(status_code=404, detail=f"id:{task_id}のタスクは見つかりません")
    return db[task_id]

# GET（複）
@app.get("/todo")
def get_todos(db: dict = Depends(task_db)):
    return db

# POST
class todoCreate(BaseModel):
    title :str

@app.post("/todo")
def create_todo(task: todoCreate, db: dict = Depends(task_db)):
    new_task = Task(task.title)
    db[new_task.task_id] = new_task
    return new_task

# PUT
@app.put("/todo/{task_id}")
def update_todo(task_id: int, db: dict = Depends(task_db)):
    if task_id not in db:
        raise HTTPException(status_code=404, detail=f"task_id: {task_id}は見つかりません")
    existing_task = db[task_id]
    existing_task.isDone = not existing_task.isDone
    return existing_task

# DELETE
@app.delete("/todo/{task_id}")
def delete_task(task_id: int, db: dict = Depends(task_db)):
    if task_id not in db:
        raise HTTPException(status_code=404, detail=f"task_id: {task_id}は見つかりません")
    del db[task_id]
    return {"message": f"task_id: {task_id}のタスクを削除しました", "todo": db}
