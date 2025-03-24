import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session


app = FastAPI()

DATABASE_URL = "postgresql://postgres:MNB1787mnb@localhost:5432/TaskManager"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
# This model defines the "tasks" table structure in the PostgreSQL database.
class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)  # Primary key for the task
    user_id = Column(String, index=True, nullable=False)  # User ID to which the task belongs
    name = Column(String, nullable=False)  # Task name
    description = Column(String, nullable=False)  # Task description
    priority = Column(Integer, default=5)  # Task priority (default is 5)
    start_date = Column(DateTime, default=datetime.now)  # Start date of the task
    finish_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))  # Finish date (default is 1 day after start)

# Create database tables
# This creates the "tasks" table in the database if it doesn't already exist.
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response validation
# Define how data will be validated and serialized/deserialized.
class Task(BaseModel):
    id: Optional[int] = Field(None, ge=0)  # Указываем по умолчанию None, и устанавливаем, что id >= 0
    user_id: str
    name: str
    description: str
    priority: int = 5
    start_date: datetime = datetime.now()
    finish_date: datetime = datetime.now() + timedelta(days=1)

    class Config:
        from_attributes = True  # Используем from_attributes вместо orm_mode

# Dependency for database session
# This function manages the database session lifecycle.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session to the route handler
    finally:
        db.close()  # Ensure the session is closed after use

# Routes
# Define API endpoints for CRUD operations.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/tasks", response_model=List[Task])
async def get_tasks(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all tasks for a specific user.
    :param user_id: The ID of the user whose tasks are being retrieved.
    :param db: Database session dependency.
    :return: List of tasks.
    """
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user.")
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single task by its ID and user ID.
    :param task_id: The ID of the task.
    :param user_id: The ID of the user.
    :param db: Database session dependency.
    :return: The task details.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user.")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
async def add_task(task: Task, db: Session = Depends(get_db)):
    # Создаём задачу в базе данных
    db_task = TaskModel(**task.dict())  # Преобразуем Pydantic в SQLAlchemy
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Получаем id, которое было сгенерировано
    return db_task  # Возвращаем задачу с id

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    """
    Update an existing task.
    :param task_id: The ID of the task to update.
    :param updated_task: Updated task data.
    :param db: Database session dependency.
    :return: The updated task details.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == updated_task.user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user.")

    # Update task fields
    task.name = updated_task.name
    task.description = updated_task.description
    task.priority = updated_task.priority
    task.start_date = updated_task.start_date
    task.finish_date = updated_task.finish_date

    db.commit()  # Commit the changes
    db.refresh(task)  # Refresh the instance to return updated data
    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, user_id: str, db: Session = Depends(get_db)):
    """
    Delete a task by its ID and user ID.
    :param task_id: The ID of the task to delete.
    :param user_id: The ID of the user.
    :param db: Database session dependency.
    :return: Success message.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user.")

    db.delete(task)  # Delete the task from the database
    db.commit()  # Commit the transaction
    return {"message": "Task successfully deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)