from typing import List
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    spotify_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    credits: Mapped[List["Credit"]] = relationship(back_populates="track")


class Credit(Base):
    __tablename__ = "credit"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column(nullable=False)
    track_id: Mapped[int] = mapped_column(ForeignKey("track.id"))
    contributor_id: Mapped[int] = mapped_column(ForeignKey("contributor.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    track: Mapped["Track"] = relationship(back_populates="credits")
    contributor: Mapped["Contributor"] = relationship(back_populates="credits")
    role: Mapped["Role"] = relationship()


class Contributor(Base):
    __tablename__ = "contributor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    spotify_id: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    image_uri: Mapped[str] = mapped_column(String(255), nullable=True)
    credits: Mapped[List["Credit"]] = relationship(back_populates="contributor")


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)




AAC3e6FPZtbuJUvPVx4E+yPahODfoOZgQwxOXv7vVcTcObajBm+fvyzZbcAK8br8DmoUoNc8D1jqpXIgXM94JFwqBZ/3FLpKITCKN1DY3zHQP8ZmjAwtui0dYUaffEOQDi1xnYMdoJxFI2kDuWawSgT3gbGxdhJLuRDT73CDkFw6hBlFpxIPdHVdss8hQJELCn3MaRiUs0IPwVRZlsWmnhQ50eDATK0h129MIzscjk32tsrtcCGoKG+/1o+ZvmxTZEY7v8CGxFyxVyIVCGzdgTNeiXu3H0tVapgd+v9Nswvy