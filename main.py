from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Task API", version="1.0.0")

# --- DATA MODEL (Validation) ---
class TaskCreate(BaseModel):
    title: str
    done: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# Helper class representing a new task with useful methods
class NewTask:
    def __init__(self, title: str, done: bool = False):
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        self.title = title.strip()
        self.done = bool(done)

    def save(self):
        """Persist the task into the in-memory tasks_db and return the created dict."""
        new_id = max([t["id"] for t in tasks_db], default=0) + 1
        task_record = {"id": new_id, "title": self.title, "done": self.done}
        tasks_db.append(task_record)
        return task_record

    def to_dict(self):
        return {"title": self.title, "done": self.done}

    def set_done(self, value: bool = True):
        self.done = bool(value)

    def update_title(self, new_title: str):
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title.strip()

# --- IN-MEMORY DATABASE ---
tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False}
]

# --- STAGE 1: Root & Health Check ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- STAGE 2: Read Endpoints ---
@app.get("/tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# --- STAGE 3: Create Endpoint ---
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Validation check: title must not be empty or blank whitespace
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task.title.strip(),
        "done": task.done
    }
    tasks_db.append(new_task)
    return new_task

# --- STAGE 4: Update & Delete Endpoints ---
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_update.title.strip()
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")