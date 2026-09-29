from database.repository import create_note as create_note_db
from tools.context import current_db,current_user_id


def create_note(title:str,content:str)->dict:
    """
    Creates a note for the current user.

    Args:
        title: The title of the note.
        content: The content of the note.

    Returns:
        Information about the created note.
    """

    db=current_db.get()
    user_id=current_user_id.get()


    note = create_note_db(
        db=db,
        user_id=user_id,
        title=title,
        content=content
    )

    return{
        "id": note.id,
        "title": note.title,
        "content": note.content
    }