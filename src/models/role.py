from enum import Enum


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


"""
Step 2: Create an Enum
class Role(Enum):

Normally, we write:
    class Student:

Here we write:
    class Role(Enum):

This means:

Role is not a normal class. It is an Enum class.
An Enum is a class where the values are fixed and predefined.


Step 3: Define the values
USER = "user"
ASSISTANT = "assistant"
SYSTEM = "system"

This creates three valid roles.
Visual representation:

Role
│
├── USER
├── ASSISTANT
└── SYSTEM

Each one has an associated value:
Role.USER
        │
        ▼
      "user"

Role.ASSISTANT
        │
        ▼
   "assistant"

Role.SYSTEM
        │
        ▼
     "system"
"""
