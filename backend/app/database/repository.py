from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import User,Conversation,Message

def create_user(db:Session,email:str,):

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is not None:
        return user

    user=User(email=email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_conversation(db:Session,user_id:int,title:str):
    conversation=Conversation(user_id=user_id,title=title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def save_message(db:Session,conversation_id:int,role:str,content:str):
    message=Message(conversation_id=conversation_id,role=role,content=content)
    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_messages(db:Session,conversation_id:int):
    return (
        db.query(Message).filter(
            Message.conversation_id==conversation_id
        ).order_by(Message.created_at)
        .all()
    )

def get_conversation(db:Session,conversation_id:int):
    return(
        db.query(Conversation).filter(
            Conversation.id==conversation_id
        )
        .first()
    )