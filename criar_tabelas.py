from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    import models._all_models

    try:
        print("Conectando ao banco de dados...")
        async with engine.begin() as conn:
            # print("Deletando tabelas...")
            await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
            print("Criando tabelas...")
            await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        await engine.dispose()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
