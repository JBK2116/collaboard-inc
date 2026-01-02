"""
This module stores the business logic to be used in `views.py`
"""

from random import randint

from django.core.exceptions import ValidationError

from ..authentication.models import CustomUser
from .models import Meeting, Question


def generate_access_code(num_of_digits: int) -> str:
    """
    Generates a random numerical access code of `num_of_digits` length
    :param num_of_digits: The number of digits to be in the access code
    :return: The access code
    """
    return "".join(["{}".format(randint(0, 9)) for _ in range(0, num_of_digits)])


def create_meeting(
    user: CustomUser, title: str | None, description: str | None, duration: str | None
) -> Meeting | None:
    """
    Creates a meeting object and runs validation on it
    :param user: User of the meeting
    :param title: Title of the meeting
    :param description: Description of the meeting
    :param duration: Minute Duration of the meeting (converted to an int later)
    :return: Meeting object if created else None if an exception occurred
    """
    try:
        if not title or not description or not duration:
            return None
        meeting = Meeting(
            user=user,
            title=title,
            description=description,
            duration=int(duration) * 60,
            access_code=generate_access_code(8),
        )
        meeting.clean()
        return meeting
    except (TypeError, ValueError, ValidationError):
        return None


def create_questions(
    meeting: Meeting, questions: list[Question] | None
) -> list[Question] | None:
    """
    Iterates over the `questions` array and creates a new question object for each value.
    Each created object is validated with `clean`
    :param meeting: Meeting object related to the question
    :param questions: Array of questions
    :return: list of Question objects if all questions were valid, else None
    """
    try:
        new_questions: list[Question] = []
        if not meeting or not questions:
            return None
        for index, question in enumerate(questions, start=1):
            if not question:
                return None
            new_question = Question(meeting=meeting, text=question, index=index)
            new_question.clean()
            new_questions.append(new_question)
        return new_questions
    except ValidationError:
        return None
