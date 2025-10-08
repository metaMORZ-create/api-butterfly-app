from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Float, Text, func
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

# ======================
# User
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)

    # Gegenbeziehung zu ButterflyPhoto
    photos = relationship(
        "ButterflyPhoto",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ======================
# Butterfly
# ======================
class Butterfly(Base):
    __tablename__ = "butterflies"

    id = Column(Integer, primary_key=True, index=True)

    # Basis-Anzeigeinfos
    common_name = Column(String, nullable=False, index=True)       # z.B. "Tagpfauenauge"
    scientific_name = Column(String, nullable=True, index=True)    # z.B. "Aglais io"

    description = Column(Text, nullable=True)      # Kurzbeschreibung
    reproduction = Column(Text, nullable=True)     # "Ei → Raupe → Puppe → Falter"
    habitat = Column(Text, nullable=True)          # Lebensraum
    season = Column(String, nullable=True)         # Flugsaison, z.B. "Mai–Sep"

    # Maße/Angaben
    wingspan_min_mm = Column(Integer, nullable=True)
    wingspan_max_mm = Column(Integer, nullable=True)

    # Medien (z.B. Referenzbilder für die Detailseite)
    image_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)

    # Optionale strukturierte Felder
    tags = Column(JSONB, nullable=True)            # z.B. ["Nektartrinker","Wiese"]
    regions = Column(JSONB, nullable=True)         # z.B. ["Mitteleuropa","Südeuropa"]
    protection_status = Column(String, nullable=True)  # z.B. "nicht gefährdet"

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Verknüpfung zu Fotos (ORM-Komfort)
    photos = relationship(
        "ButterflyPhoto",
        back_populates="butterfly",
        cascade="all, delete-orphan",
    )


# ======================
# ButterflyPhoto
# ======================
class ButterflyPhoto(Base):
    __tablename__ = "butterfly_photos"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    butterfly_id = Column(
        Integer,
        ForeignKey("butterflies.id", ondelete="CASCADE"),  # <-- ForeignKey ergänzt
        nullable=False,
        index=True,
    )

    taken_at = Column(DateTime(timezone=True), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Medieninfo für dein Cloudinary-Upload
    image_url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)

    # Beziehungen
    user = relationship("User", back_populates="photos")
    butterfly = relationship("Butterfly", back_populates="photos")
