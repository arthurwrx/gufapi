from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        senha (str): A senha fornecida pelo usuário.
        hash_senha (str): O hash da senha armazenada no banco de dados.

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário.
    """
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.

    Args:
        senha (str): A senha fornecida pelo usuário.

    Returns:
        str: O hash da senha gerado.
    """
    return CRIPTO.hash(senha)
