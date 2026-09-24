from datetime import datetime

from sqlalchemy import String,Text,ForeignKey,DateTime
from sqlalchemy.orm import relationship,Mapped,mapped_column

from database.database import Base


class User(Base):

    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        nullable=False)
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow

    )
    conversations: Mapped[list["Conversation"]] = relationship(
    back_populates="user"
)

class Conversation(Base):

    __tablename__= "conversations"
    id:Mapped[int]=mapped_column(
        primary_key=True
    )
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=False

    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    user: Mapped["User"] = relationship(
    back_populates="conversations"
)

    messages: Mapped[list["Message"]] = relationship(
    back_populates="conversation"
)

class Message(Base):
    
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    conversation: Mapped["Conversation"] = relationship(
    back_populates="messages"
)