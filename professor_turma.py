from sqlalchemy import create_engine, String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class Professor(Base):
    __tablename__ = "tabela_professor"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    telefone: Mapped[str] = mapped_column(String(13))
    email: Mapped[str] = mapped_column(String(250))
    materia: Mapped[str] = mapped_column(String(50))

class Turma(Base):
    __tablename__ = "tabela_turma"
    id: Mapped[int] = mapped_column(primary_key=True)
    nivel: Mapped[str] = mapped_column(String(3))
    sala: Mapped[str] = mapped_column(String(3))
    quant_alunos: Mapped[str] = mapped_column(Integer)
    # chave estrangeira
    professor_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_professor.id"), 
        primary_key=True)
    professor: Mapped["Professor"] = relationship(
        back_populates="turma")  

    bd = int(input("Digite 1 para MySQL ou 2 para SQLite: "))

    if bd == 1:
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/curso")
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            #criar turmas e professores aqui
            nome_professor = input("Digite o nome do professor: ")
            telefone_professor = input("Digite o telefone do professor: ")
            email_professor = input("Digite o email do professor: ")
            materia_professor = input("Digite a materia do professor: ")

            novo_professor = Professor(nome = nome_professor, telefone = telefone_professor, email = email_professor, materia = materia_professor)

            # podemos adicionar apenas a receita, que já contém 
            # todos os outros objetos
            session.add(novo_professor)

            # salvar tudo!
            session.commit()

    if bd == 2:
        engine = create_engine("sqlite:///pessoas.db")
        Base.metadata.create_all(engine)


        with Session(engine) as session:
            #criar turmas e professores aqui
            nome_professor = input("Digite o nome do professor: ")
            telefone_professor = input("Digite o telefone do professor: ")
            email_professor = input("Digite o email do professor: ")
            materia_professor = input("Digite a materia do professor: ")

            novo_professor = Professor(nome = nome_professor, telefone = telefone_professor, email = email_professor, materia = materia_professor)

            # podemos adicionar apenas a receita, que já contém 
            # todos os outros objetos
            session.add(novo_professor)

            # salvar tudo!
            session.commit()
    




