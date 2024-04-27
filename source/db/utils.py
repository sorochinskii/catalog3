from collections.abc import Coroutine

# async def get_user_by_email(email: str) -> Coroutine:
#     query = users_table.select().where(users_table.c.email == email)
#     return await database.fetch_one(query)


# async def get_user_by_token(token: str) -> Coroutine:
#     query = tokens_table.join(users_table).select().where(
#         and_(
#             tokens_table.c.token == token,
#             tokens_table.c.expires > datetime.now()
#         )
#     )
#     return await database.fetch_one(query)


# async def create_user_token(user_id: int):
#     """ Создает токен для пользователя с указанным user_id """
#     query = (
#         tokens_table.insert()
#         .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
#         .returning(tokens_table.c.token, tokens_table.c.expires)
#     )
#     return await database.fetch_one(query)
