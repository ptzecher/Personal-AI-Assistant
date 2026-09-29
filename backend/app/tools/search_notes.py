from database.repository import get_notes
from tools.context import current_db,current_user_id


def search_notes(query:str)->list[dict]:
    """
        Searches the notes of the current user.
    
        Args:
            query:Retrieve relevant notes base on this query
    
        Returns:
            A list of relevant notes and their context
    """
    db = current_db.get()
    user_id = current_user_id.get()

    notes=get_notes(db=db,user_id=user_id)
    query = query.lower()

    result=[]
    for note in notes:
        if (
            query in note.title.lower()
            or query in note.content.lower()):
            result.append({"title":note.title,
                           "content":note.content})

    return result



