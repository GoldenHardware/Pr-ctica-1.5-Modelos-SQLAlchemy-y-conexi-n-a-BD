"""Router del recurso /projects (persistido en la base de datos)."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.deps import DbSession
from app.models import Project
from app.schemas import ErrorResponse, ProjectCreate, ProjectRead

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={422: {"model": ErrorResponse, "description": "Datos no válidos"}},
)


@router.get("", response_model=list[ProjectRead], summary="Listar proyectos")
def list_projects(db: DbSession):
    return db.scalars(select(Project).order_by(Project.id)).all()


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Obtener un proyecto",
    responses={404: {"model": ErrorResponse, "description": "Proyecto no encontrado"}},
)
def get_project(project_id: int, db: DbSession):
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, summary="Crear un proyecto")
def create_project(data: ProjectCreate, db: DbSession):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)  # carga id y created_at generados por la BD
    return project
