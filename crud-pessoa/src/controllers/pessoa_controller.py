from models.pessoa import Pessoa
from database import db
from sqlalchemy.exc import SQLAlchemyError

class PessoaController:
    """
    Controller for managing Pessoa entities.
    """

    @staticmethod
    def salvar_pessoa(nome, sobrenome, cpf, data_nascimento):
        """
        Save a new Pessoa to the database.

        Args:
            nome (str): First name of the person.
            sobrenome (str): Last name of the person.
            cpf (str): CPF (must be 11 digits).
            data_nascimento (str): Date of birth in string format.

        Raises:
            ValueError: If any of the input validations fail.
            SQLAlchemyError: If a database error occurs.
        """
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome é obrigatório e deve ser uma string não vazia.")
        if not isinstance(sobrenome, str) or not sobrenome.strip():
            raise ValueError("Sobrenome é obrigatório e deve ser uma string não vazia.")
        if not isinstance(cpf, str) or len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("O CPF deve ser uma string de 11 dígitos numéricos.")
        if not isinstance(data_nascimento, str) or not data_nascimento.strip():
            raise ValueError("Data de nascimento é obrigatória e deve ser uma string não vazia.")

        try:
            pessoa = Pessoa(
                nome=nome.strip(),
                sobrenome=sobrenome.strip(),
                cpf=cpf.strip(),
                data_de_nascimento=data_nascimento.strip()
            )
            db.session.add(pessoa)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Erro ao salvar pessoa no banco de dados: {e}")

    @staticmethod
    def listar_pessoas():
        """
        List all Pessoa entities from the database.

        Returns:
            list: A list of Pessoa objects.
        """
        try:
            return Pessoa.query.all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro ao listar pessoas: {e}")

    @staticmethod
    def remover_pessoa(pessoa_id):
        """
        Remove a Pessoa from the database by ID.

        Args:
            pessoa_id (int): The ID of the Pessoa to be removed.

        Raises:
            ValueError: If the pessoa_id is invalid.
            SQLAlchemyError: If a database error occurs.
        """
        if not isinstance(pessoa_id, int) or pessoa_id <= 0:
            raise ValueError("O ID da pessoa deve ser um número inteiro positivo.")

        try:
            pessoa = Pessoa.query.get(pessoa_id)
            if not pessoa:
                raise ValueError(f"Pessoa com ID {pessoa_id} não encontrada.")
            db.session.delete(pessoa)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Erro ao remover pessoa do banco de dados: {e}")