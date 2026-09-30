from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import User,Conversation,Message,Note

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
def create_note(db:Session,user_id:int,title:str,content:str):

    note=Note(user_id=user_id,title=title,content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db:Session,user_id:int):
    return(
        db.query(Note).filter(
            Note.user_id==user_id
        ).order_by(Note.created_at)
        .all()
    )

def get_conversations(db:Session,user_id:int):
    return(
        db.query(Conversation).filter(
            Conversation.user_id==user_id
        ).order_by(Conversation.created_at)
        .all()
    )

def update_conversation(db:Session,conversation_id,title:str):
    conversation=get_conversation(db,conversation_id)

    if conversation is None:
        return None
    conversation.title=title
    db.commit()
    db.refresh(conversation)
    return conversation

def delete_conversation(db:Session,conversation_id):

    conversation=get_conversation(db,conversation_id)

    if conversation is None:
        return False
    db.delete(conversation)
    db.commit()
    return True