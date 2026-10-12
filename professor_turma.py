from sqlalchemy import create_engine, String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List, Optional

class Base(DeclarativeBase): #Apelidando a base
    pass

class Professor(Base): #Criando a classe professor
    __tablename__ = "tabela_professor"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(250))
    telefone: Mapped[str] = mapped_column(String(13))
    email: Mapped[str] = mapped_column(String(250))
    materia: Mapped[str] = mapped_column(String(50))
    # Relacionando com as turmas
    turmas: Mapped[List["Turma"]] = relationship(back_populates="professor")

class Turma(Base):
    __tablename__ = "tabela_turma"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nivel: Mapped[str] = mapped_column(String(3))
    sala: Mapped[str] = mapped_column(String(3))
    quant_alunos: Mapped[int] = mapped_column(Integer)
    #Chave estrangeira
    professor_email: Mapped[str] = mapped_column(
        String(250), ForeignKey("tabela_professor.email")
    )
    #Relacionando com o professor pelo email dele
    professor: Mapped["Professor"] = relationship(back_populates="turmas")

def escolher_conexao(): # Função para o usuário escolher o banco de dados que vai querer usar
    bd = int(input("Digite 1 para MySQL ou 2 para SQLite: "))

    if bd == 1:
        engine = create_engine("mysql+pymysql://root:@localhost:3306/curso")
    else:
        engine = create_engine("sqlite:///pessoas.db")

    Base.metadata.create_all(engine)
    return engine #retorna o banco escolhido 


def main(): #Código principal
    engine = escolher_conexao()
    session = Session(engine)

    while True:
        print("\n================ MENU PRINCIPAL ================")
        print("1 - Cadastrar Professor")
        print("2 - Cadastrar Turma")
        print("3 - Listar Professores e Turmas")
        print("4 - Excluir professor")
        print("5 - Excluir turma")
        print("6 - Trocar de Banco de Dados")
        print("7 - Sair")

        escolha = int(input("Digite o número de sua escolha: "))

        if escolha == 1:

            #criar professores aqui
            nome_professor = input("Digite o nome do professor: ")
            telefone_professor = input("Digite o telefone do professor: ")
            email_professor = input("Digite o email do professor: ")
            materia_professor = input("Digite a materia do professor: ")

            novo_professor = Professor(nome = nome_professor, telefone = telefone_professor, email = email_professor, materia = materia_professor)

            try: #Tenta salvar no banco de dados
                session.add(novo_professor)
                session.commit()
                print("Professor cadastrado com sucesso!")
            except Exception as e: #Se não salvar no banco de dados uma mensagem de erro será exibida
                session.rollback()
                print(f"Erro ao cadastrar professor (verifique se o e-mail já existe): {e}")

        elif escolha == 2:

            email_escolhido = input("\nDigite exatamente o E-MAIL do professor que deseja vincular a esta turma: ")
                    
            # Verifica se o e-mail informado realmente existe no banco
            professor_valido = session.query(Professor).filter_by(email=email_escolhido).first()
                #O query utilizado acima é um comando do sqlalchemy para busca e listagem

            if professor_valido:
                #criar turmas aqui
                nivel = input("Digite o nivel da turma: ")
                sala = input("Digite a sala da turma: ")
                quant_alunos = input("Digite a quantidade de alunos da turma: ")
                
                nova_turma = Turma(nivel = nivel, sala = sala, quant_alunos = quant_alunos, professor_email = email_escolhido)

                #Adiciona nova turma ao banco
                try: 
                    session.add(nova_turma)
                    session.commit()
                    print("Turma cadastrada com sucesso")
                except Exception as e: #Se não salvar no banco de dados uma mensagem de erro será exibida
                    session.rollback()
                    print(f"Erro ao cadastrar turma: {e}")
            else:
                print("E-mail inválido ou não encontrado na lista.")

        elif escolha == 3:
            # Busca o(s) professores pelo nome ou parte dele
            termo = input("Digite o nome do professor para filtrar (ou enter para listar todos): ")
            query = session.query(Professor) #prepara para uma busca na tabea professores
            if termo: #Verifica se algo foi digitado
                query = query.filter(Professor.nome.ilike(f"%{termo}%")) #Busca os nomes que em alguma parte tenham o termo digitado
            
            professores = query.all() #Coloca os resultados em professores
            
            if not professores:
                print("Nenhum registro encontrado.")
            else: #Se houver professor com o termo então a busca retorna as informações do professor e das turmas
                print("\n--- LISTA DE PROFESSORES E TURMAS ---")
                for p in professores:
                    print(f"Professor: {p.nome} | E-mail: {p.email} | Matéria: {p.materia}")
                    if p.turmas:
                        print("Turmas:")
                        for t in p.turmas:
                            print(f"Turma ID: {t.id} | Nível: {t.nivel} | Sala: {t.sala} | Alunos: {t.quant_alunos}")
                    else:
                        print("  (Sem turmas cadastradas)")

        elif escolha == 4:
            #Excluir professor            
            email_excluir = input("\nDigite exatamente o E-MAIL do professor que deseja excluir: ")
            professor_alvo = session.query(Professor).filter_by(email=email_excluir).first()

            if professor_alvo:
                try:
                    session.delete(professor_alvo)
                    session.commit()
                    print("Professor (e as respetivas turmas associadas) excluído com sucesso!")
                except Exception as e:
                    session.rollback()
                    print(f"Erro ao excluir professor: {e}")
            else:
                print("E-mail não encontrado.")

        elif escolha == 5:
            # Excluir Turma
            turmas = session.query(Turma).all()
            if not turmas:
                print("Nenhuma turma cadastrada para excluir.")
            else:
                print("\nTurmas disponíveis:")
                for t in turmas:
                    print(f"-> ID: {t.id} | Nível: {t.nivel} | Sala: {t.sala} | Professor Email: {t.professor_email}")
                
                id_turma_str = input("\nDigite o ID numérico da turma que deseja excluir: ")
                if id_turma_str.isdigit():
                    id_turma = int(id_turma_str)
                    turma_alvo = session.query(Turma).filter_by(id=id_turma).first()
                    if turma_alvo:
                        try:
                            session.delete(turma_alvo)
                            session.commit()
                            print("Turma excluída com sucesso!")
                        except Exception as e:
                            session.rollback()
                            print(f"Erro ao excluir turma: {e}")
                    else:
                        print("ID de turma não encontrado.")
                else:
                    print("ID inválido. Deve ser um número.")

        elif escolha == 6:
            # Troca segura de banco de dados
            session.close() # Fecha a sessão antiga
            engine = escolher_conexao() # Pega um novo engine
            session = Session(engine) # Abre nova sessão para o novo banco
            print("Banco de dados alterado com sucesso!")

        elif escolha == 7:
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")        

    session.close()

#Roda a função main
if __name__ == "__main__": 
    main()