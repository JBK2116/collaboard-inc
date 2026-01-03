"""
This module stores the business logic to be used in `views.py`
"""

import logging
import uuid
from random import randint

from django.core.exceptions import ValidationError

from ..authentication.models import CustomUser
from .models import Meeting, Question

logger = logging.getLogger(__name__)


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
        logger.log(
            level=logging.DEBUG,
            msg="Creating Meeting",
            extra={"title": title, "description": description, "duration": duration},
        )
        meeting = Meeting(
            user=user,
            title=title,
            description=description,
            duration=int(duration),
            access_code=generate_access_code(8),
        )
        logger.log(
            level=logging.DEBUG, msg="Meeting created", extra={"meeting": meeting}
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


def get_meeting(meeting_id: uuid.UUID) -> Meeting | None:
    """
    Gets a meeting object with the given `meeting_id`
    :param meeting_id: ID of the meeting to retrieve
    :return: Meeting object if found else None
    """
    try:
        meeting: Meeting = Meeting.objects.get(pk=meeting_id)
        return meeting
    except (ValueError, Meeting.DoesNotExist):
        return None
