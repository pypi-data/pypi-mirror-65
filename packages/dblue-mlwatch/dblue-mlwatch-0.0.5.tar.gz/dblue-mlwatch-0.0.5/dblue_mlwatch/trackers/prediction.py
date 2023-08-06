import json
import sys
import traceback
import uuid

from typing import Dict, List

from dblue_mlwatch.constants import EventType, Types
from dblue_mlwatch.exceptions import DblueMLWatchException
from dblue_mlwatch.logger import logger
from dblue_mlwatch.trackers.base import BaseTracker
from dblue_mlwatch.validation import validate_schema
from dblue_mlwatch.validation.schemas import PREDICTION_SCHEMA


class PredictionTracker(BaseTracker):

    def __init__(self, *args, **kwargs):
        super(PredictionTracker, self).__init__(*args, **kwargs)

    def _create_prediction_event(
            self,
            features: Types.Features,
            prediction: Types.Prediction,
            prediction_probs: Types.PredictionProbs = None,
            unique_id: Types.UniqueId = None
    ) -> Types.PredictionEvent:
        """
        Create prediction event dict
        :param features: Model features
        :param prediction: Prediction from model
        :param prediction_probs: Prediction probability for classification models
        :param unique_id: Unique id for the model request, used for combining feedback at later stage
        :return: Dict of the prediction event
        """

        unique_id = unique_id or uuid.uuid4().hex
        _features = None
        _prediction_probs = None

        try:
            _features = json.dumps(features) if features else None
            _prediction_probs = json.dumps(prediction_probs) if prediction_probs else None
        except Exception as e:
            raise DblueMLWatchException("Failed to serialize prediction data: %s" % e)

        event = {
            'event_type': EventType.PREDICTION,
            'features': _features,
            'prediction': prediction,
            'prediction_probs': _prediction_probs,
            'unique_id': unique_id,
        }

        return unique_id, event

    def capture_prediction(self, event: Dict) -> Types.CaptureStatus:
        """
        Capture prediction event from dict
        :param event: Prediction event in dictionary format
        :return: Capture status
        """

        is_valid, errors = validate_schema(data=event, schema=PREDICTION_SCHEMA)

        if not is_valid:
            raise DblueMLWatchException("Prediction data is not as per the schema: %s" % errors)

        unique_id, event = self._create_prediction_event(
            features=event.get('features'),
            prediction=event.get('prediction'),
            prediction_probs=event.get('prediction_probs'),
            unique_id=event.get("unique_id")
        )

        statuses = self.emit(events=[event])

        return unique_id, statuses[0]

    def capture_prediction_batch(self, events: List[Dict]) -> List[Types.CaptureStatus]:
        """
        Capture prediction events in batch
        :param events: List of events
        :return: List of capture status
        """

        _events = []
        _unique_ids = []

        for event in events:

            is_valid, errors = validate_schema(data=event, schema=PREDICTION_SCHEMA)

            if not is_valid:
                raise DblueMLWatchException("Prediction data is not as per the schema: %s" % errors)

            unique_id, event = self._create_prediction_event(
                features=event.get('features'),
                prediction=event.get('prediction'),
                prediction_probs=event.get('prediction_probs'),
                unique_id=event.get("unique_id")
            )

            _unique_ids.append(unique_id)
            _events.append(event)

        statuses = self.emit(events=_events)
        return list(zip(_unique_ids, statuses))

    def capture_exception(self, message: str = None) -> bool:
        """
        Capture exceptions
        :param message: Error message
        :return: Emit status
        """
        exc_info = sys.exc_info()

        event = {
            'event_type': EventType.EXCEPTION,
            'message': message,
            'exec_info': traceback.format_exception(*exc_info),
        }

        logger.exception(msg=message)

        statuses = self.emit(events=[event])
        return statuses[0]

    def capture_request_log(self, request: Dict, response: Dict, response_time: float) -> bool:
        """
        Capture request logs with response and time taken to serve the request

        :param request: Request parameters
        :param response:  Response
        :param response_time: Time taken to serve the request
        :return: Capture status
        """

        _request = None
        _response = None

        try:
            _request = json.dumps(request) if request else None
            _response = json.dumps(response) if response else None

        except Exception as e:
            raise DblueMLWatchException("Failed to serialize prediction data: %s" % e)

        event = {
            'event_type': EventType.REQUEST_LOG,
            'request': _request,
            'response': _response,
            'response_time': response_time,
        }

        statuses = self.emit(events=[event])
        return statuses[0]
