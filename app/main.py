import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@db:5432/notesdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Note(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True, index=True)
	text = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class NoteCreate(BaseModel):
	text: str

@app.get ("/health")
def health():
	return {"status" : "ok"}

@app.get("/notes")
def list_notes():
	db = SessionLocal()
	notes = db.query(Note).all()
	db.close()
	return notes

@app.post("/notes")
def create_note(note: NoteCreate):
	db = SessionLocal()
	new_note = Note(text=note.text)
	db.add (new_note)
	db.commit()
	db.refresh(new_note)
	db.close()
	return new_note
