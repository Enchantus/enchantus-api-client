import uuid
from enum import Enum, auto


class DialogueType(str, Enum):
    NPC = "NPC"
    NARRATION = "NARRATION"
    PLAYER = "PLAYER"
    QUEST = "QUEST"


class Dialogue:
    id: uuid.UUID
    project_id: uuid.UUID
    parent_id: uuid.UUID
    type: DialogueType
    actor_id: uuid.UUID
    content: str

    def __init__(self,
                 dialogue_id: uuid.UUID,
                 project_id: uuid.UUID,
                 dialogue_type: DialogueType,
                 actor_id: uuid.UUID,
                 content: str,
                 parent_id: uuid.UUID = None):
        """
        A dialogue component of a dialogue tree.

        :param dialogue_id: Unique ID for the dialogue for storage and reference.
        :param project_id: The ID of the project this dialogue belongs to.
        :param dialogue_type: Type of the dialogue (from DialogueType enum).
        :param actor_id: The ID of the actor who is speaking the dialogue.
        :param content: The content or text of the dialogue.
        :param parent_id: The ID of the previous dialogue in the conversation. Default is None for starting dialogues.
        """
        if not isinstance(dialogue_type, DialogueType):
            raise ValueError(f"Invalid dialogue type: {dialogue_type}. Must be an instance of DialogueType enum.")
        self.id = dialogue_id
        self.project_id = project_id
        self.parent_id = parent_id
        self.type = dialogue_type
        self.actor_id = actor_id
        self.content = content

    def __str__(self):
        return f"({self.id}) [{self.project_id}] {self.type.name} - {self.actor_id}: {self.content}"

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "type": self.type.name,
            "actor_id": self.actor_id,
            "content": self.content,
            "parent_id": self.parent_id
        }

    @staticmethod
    def from_dict(dialogue_dict):
        return Dialogue(
            dialogue_id=dialogue_dict['id'],
            project_id=dialogue_dict['project_id'],
            parent_id=dialogue_dict['parent_id'],
            dialogue_type=DialogueType[dialogue_dict['type']],
            actor_id=dialogue_dict['actor_id'],
            content=dialogue_dict['content']
        )
