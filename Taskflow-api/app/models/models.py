"""
Modelos de base de datos (SQLAlchemy, estilo declarativo).

Siguen el modelo de dominio del documento "Qué vamos a construir" (apartado 6).
Un modelo describe una TABLA: sus columnas, claves y relaciones. No es lo
mismo que un schema (app/schemas/), que es el contrato de la API.

Relaciones (apartado 6.2):
    Project 1 ── N Task      (opcional: una tarea puede no tener proyecto)
    Category 1 ── N Task     (opcional: una tarea puede no tener categoría)

Variante simple (apartado 6.3): todos los usuarios autenticados comparten el
mismo espacio de proyectos y tareas, así que NO hay owner_id y User no se
relaciona con Project ni con Task.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    # Nunca se guarda la contraseña en texto plano, solo su hash (RNF-01).
    hashed_password: Mapped[str] = mapped_column(String(255))


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    # No aparece en el modelo de dominio, pero ProjectRead lo incluye desde la práctica 1.2.
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # RF-12: al eliminar un proyecto se eliminan sus tareas (borrado en cascada).
    # cascade="all, delete" hace que session.delete(project) borre también sus
    # tareas, y ondelete="CASCADE" en la FK hace lo mismo a nivel de BD.
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        cascade="all, delete",
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    color: Mapped[str] = mapped_column(String(20))  # código hex ("#FF8800") o nombre ("red")

    # Sin cascade de borrado: si se elimina una categoría, sus tareas siguen
    # existiendo con category_id = NULL (ondelete="SET NULL" en Task).
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # FK a Project (opcional según el modelo de dominio).
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    # FK a Category (opcional).
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), index=True
    )

    # back_populates enlaza cada lado de la relación con el del otro modelo,
    # así task.project y project.tasks se mantienen sincronizados.
    project: Mapped["Project | None"] = relationship(back_populates="tasks")
    category: Mapped["Category | None"] = relationship(back_populates="tasks")
