from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from audacious_webui.models.base import Base


class Cookies(Base):
    __tablename__ = "cookies"
    id = Column(Integer, primary_key=True)
    ip = Column(String(16), nullable=True)
    cookies = Column(String(2048), nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, id: int,  ip: str, cookies: str):
        self.id = id
        self.ip = str(ip)
        self.cookies = str(cookies)

    def __init__(self,  ip: str, cookies: str):
        self.ip = str(ip)
        self.cookies = str(cookies)

    def __repr__(self):
        return str(self.id)


    def db_add_cookies(self, session: Session):
        try:
            session.add(self)
            session.commit()
            return self
        except IntegrityError:
            # flash("Duplicate entry!")
            return None

    @classmethod
    def db_delete_cookies(cls, session, id):
        cookies_to_delete = session.query(Cookies).get(id)
        session.delete(cookies_to_delete)
        session.commit()

    # def db_list_cookies(self, session: Session):
    #     try:
    #         cookies = Cookies.query.all()
        