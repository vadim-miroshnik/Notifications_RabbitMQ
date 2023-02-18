from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DBService:
    def __init__(self, session):
        self.session = session

    async def get_user(self, id: str):
        from models.user import User
        res = await self.session.execute(select(User).filter_by(id=id))
        return res.first()[0]

    async def get_user_by_login(self, login: str):
        from models.user import User

        res = await self.session.execute(select(User).filter_by(login=login))
        return res.first()[0]

    async def get_user_by_email(self, email: str):
        from models.user import User
        res = await self.session.execute(select(User).filter_by(email=email))
        return res.first()[0]

    async def add_user(self, login: str, password: str, email: str, fullname: str, phone: str, subscribed: bool):
        from models.user import User
        user = User(
            login=login,
            password=password,
            email=email,
            fullname=fullname,
            phone=phone,
            subscribed=False,
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user_prop(self, id: str, prop: str, value):
        from models.user import User
        res = await self.session.execute(select(User).filter_by(id=id))
        user = res.first()[0]
        setattr(user, prop, value)
        self.session.commit()
        return user

    async def get_template(self, id: str):
        from models.template import Template
        res = await self.session.execute(select(Template).filter_by(id=id))
        return res.first()[0]

    async def get_template_by_name(self, name: str):
        from models.template import Template
        res = await self.session.execute(select(Template).filter_by(name=name))
        return res.first()[0]

    async def get_users_by_group(self, id: str):
        from models.user import user_notification
        res = await self.session.execute(select(user_notification).filter_by(notification_user_group_id=id))
        return res.all()
