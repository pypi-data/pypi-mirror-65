from dblue_mlwatch import config
from dblue_mlwatch.logger import logger
from dblue_mlwatch.trackers.feedback import FeedbackTracker
from dblue_mlwatch.trackers.metrics import MetricsTracker
from dblue_mlwatch.trackers.prediction import PredictionTracker


class MLWatch:
    def __init__(self, model_id, model_version, account=None, project=None, api_key=None):
        """
        Monitor prediction, feedback, request logs etc
        :param model_id: Dblue MLWatch model id
        :param model_version: Dblue MLWatch model version
        :param account: Dblue MLWatch account id
        :param project: Dblue MLWatch project id
        :param api_key: Dblue MLWatch API Key
        """

        self.model_id = model_id
        self.model_version = model_version

        self.account = account or config.ACCOUNT
        self.project = project or config.PROJECT
        self.api_key = api_key or config.API_KEY

        self.p_tracker = PredictionTracker(
            model_id=model_id, model_version=model_version, account=account, project=project, api_key=api_key
        )
        self.f_tracker = FeedbackTracker(
            model_id=model_id, model_version=model_version, account=account, project=project, api_key=api_key
        )
        self.m_tracker = MetricsTracker(
            model_id=model_id, model_version=model_version, account=account, project=project, api_key=api_key
        )

    def capture_prediction(self, data):
        """
        Capture prediction data from dict
        :param data: Prediction dat in dictionary format
        :return: Capture status
        """

        try:
            return self.p_tracker.capture_prediction(event=data)
        except Exception:
            self.p_tracker.capture_exception("Failed to capture prediction")

        return None

    def capture_prediction_batch(self, data):
        """
        Capture prediction data in batch
        :param data: List of data
        :return: List of capture status
        """

        try:
            return self.p_tracker.capture_prediction_batch(events=data)
        except Exception:
            self.p_tracker.capture_exception("Failed to capture prediction in batch")

        return None

    def capture_exception(self, message=None):
        """
        Capture exceptions
        :param message: Error message
        :return: Emit status
        """

        try:
            return self.p_tracker.capture_exception(message=message)
        except Exception:
            logger.exception("Failed to capture exception")

        return None

    def capture_request_log(self, request, response, response_time):
        """
        Capture request logs with response and time taken to serve the request

        :param request: Request parameters
        :param response:  Response
        :param response_time: Time taken to serve the request
        :return: Capture status
        """

        try:
            return self.p_tracker.capture_request_log(request=request, response=response, response_time=response_time)
        except Exception:
            self.p_tracker.capture_exception("Failed to capture request log")

        return None

    def capture_feedback(self, data):
        """
        Capture feedback data from dictionary
        :param data: Feedback data in dict format
        :return: Capture status
        """

        try:
            return self.f_tracker.capture_feedback(event=data)
        except Exception:
            self.p_tracker.capture_exception("Failed to capture feedback")

        return None

    def capture_feedback_batch(self, data):
        """
        Capture feedback data in batch from dictionary
        :param data: List of feedback data
        :return: Capture statuses
        """

        try:
            return self.f_tracker.capture_feedback_batch(events=data)
        except Exception:
            self.p_tracker.capture_exception("Failed to capture feedback in batch")

        return None

    def track_system_metrics(self, interval: int = config.METRICS_TRACKING_INTERVAL):
        try:
            import psutil  # noqa

            self.m_tracker.track_system_metrics(interval=interval)
        except ImportError:
            logger.exception(
                "System metrics module is not installed."
                "Please install Dblue MLWatch with pip install dblue_mlwatch[system-metrics]"
            )
        except Exception:
            self.p_tracker.capture_exception("Failed to track system metrics")

    def stop_tracking_system_metrics(self):
        self.m_tracker.stop()
