from getpass import getpass
from secrets import compare_digest

from app.database import SessionLocal
from app.models.user import User
from app.security import get_password_hash


def main():
    email = input("E-mail da conta: ").strip()
    if not email:
        print("O e-mail e obrigatorio.")
        return

    password = getpass("Nova senha (minimo de 6 caracteres): ")
    confirmation = getpass("Confirme a nova senha: ")
    if len(password) < 6:
        print("A senha precisa ter pelo menos 6 caracteres.")
        return
    if not compare_digest(password, confirmation):
        print("As senhas nao conferem.")
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            print("Nenhuma conta encontrada com esse e-mail.")
            return

        user.hashed_password = get_password_hash(password)
        db.commit()
        print("Senha redefinida. Voce ja pode entrar na aplicacao.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()