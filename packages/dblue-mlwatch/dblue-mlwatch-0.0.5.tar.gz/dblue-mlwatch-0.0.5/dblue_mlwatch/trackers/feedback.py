from typing import Dict, List

from dblue_mlwatch.constants import EventType, Types
from dblue_mlwatch.exceptions import DblueMLWatchException
from dblue_mlwatch.trackers.base import BaseTracker
from dblue_mlwatch.validation import validate_schema
from dblue_mlwatch.validation.schemas import FEEDBACK_SCHEMA


class FeedbackTracker(BaseTracker):

    def __init__(self, *args, **kwargs):
        super(FeedbackTracker, self).__init__(*args, **kwargs)

    def _create_feedback_event(self, unique_id: str, target: Types.Target) -> Dict:
        """
        Create feedback event dict
        :param unique_id: Unique id for combining the feedback with prediction event
        :param target: Target label for the event
        :return: Event dict
        """

        return {
            'event_type': EventType.FEEDBACK,
            'target': target,
            'unique_id': unique_id,
        }

    def capture_feedback(self, event: Dict) -> Types.CaptureStatus:
        """
        Capture feedback event from dictionary
        :param event: Feedback event in dict format
        :return: Capture status
        """

        is_valid, errors = validate_schema(data=event, schema=FEEDBACK_SCHEMA)

        if not is_valid:
            raise DblueMLWatchException("Feedback data is not as per the schema: %s" % errors)

        unique_id = event.get('unique_id')

        event = self._create_feedback_event(
            unique_id=unique_id,
            target=event.get('target')
        )

        statuses = self.emit(events=[event])

        return unique_id, statuses[0]

    def capture_feedback_batch(self, events: List[Dict]) -> List[Types.CaptureStatus]:
        """
        Capture feedback event in batch from dictionary
        :param events: List of feedback events
        :return: Capture statuses
        """

        _events = []
        _unique_ids = []

        for event in events:
            is_valid, errors = validate_schema(data=event, schema=FEEDBACK_SCHEMA)

            if not is_valid:
                raise DblueMLWatchException("Feedback data is not as per the schema: %s" % errors)

            unique_id = event.get('unique_id')

            _unique_ids.append(unique_id)

            event = self._create_feedback_event(
                unique_id=unique_id,
                target=event.get('target')
            )

            _events.append(event)

        statuses = self.emit(events=events)
        return list(zip(_unique_ids, statuses))
