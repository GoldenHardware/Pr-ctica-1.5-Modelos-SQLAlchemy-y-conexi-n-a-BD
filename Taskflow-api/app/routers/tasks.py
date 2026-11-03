"""Router del recurso /tasks (persistido en la base de datos)."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.deps import DbSession
from app.models import Category, Project, Task
from app.schemas import ErrorResponse, TaskCreate, TaskRead

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={422: {"model": ErrorResponse, "description": "Datos no válidos"}},
)


@router.get("", response_model=list[TaskRead], summary="Listar tareas")
def list_tasks(db: DbSession, project_id: int | None = None, completed: bool | None = None):
    """Lista las tareas. Filtros opcionales: `?project_id=` y `?completed=true|false` (RF-14)."""
    query = select(Task).order_by(Task.id)
    if project_id is not None:
        query = query.where(Task.project_id == project_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    return db.scalars(query).all()


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una tarea",
    description="Crea una tarea. Proyecto y categoría son opcionales; si se indican y no existen devuelve 404.",
    responses={404: {"model": ErrorResponse, "description": "Proyecto o categoría no encontrados"}},
)
def create_task(data: TaskCreate, db: DbSession):
    if data.project_id is not None and db.get(Project, data.project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    if data.category_id is not None and db.get(Category, data.category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
