import copy
import json
import logging

class StructuredLog(object):
    # Used to get a dict with the correct structuring from a LogRecord

    REQUIRED_JSON_LOG_KEYS = ['event', 'asctime']
    OPTIONAL_JSON_LOG_KEYS = ['aws_request_id', 'filename', 'funcName', 'levelname', 'exc_info']

    def __init__(self, record: logging.LogRecord):
        self._input_record = record
        self._log = {}
        self._generate_log()

    def get_structured_log(self) -> dict:
        return self._log

    def promote_message_keys(self):
        # Move as many keys as possible from the _log['message'] dict up one level to the _log dict
        if self._log['message'] and type(self._log['message']) is dict:
            self._log['message'] = copy.deepcopy(self._log['message'])
            for key in list(self._log['message'].keys()):
                self._promote_message_key(key)
            if len(self._log['message']) == 1 and 'message' in self._log['message']:
                self._log['message'] = self._log['message'].pop('message')
            elif not self._log['message']:
                del self._log['message']

    def _generate_log(self):
            self._add_message_key()
            self._add_log_keys()

    def _add_message_key(self):
            unformatted_message = getattr(self._input_record, 'msg', None)
            if type(unformatted_message) is str:
                try:
                    json_message = json.loads(unformatted_message)
                    self._log['message'] = json_message
                except json.decoder.JSONDecodeError:
                    self._log['message'] = unformatted_message
            else:
                self._log['message'] = unformatted_message

    def _add_log_keys(self):
            for _key in self.OPTIONAL_JSON_LOG_KEYS:
                if getattr(self._input_record, _key, None):
                    self._log[_key] = getattr(self._input_record, _key)
            for _key in self.REQUIRED_JSON_LOG_KEYS:
                self._log[_key] = getattr(self._input_record, _key, None)

    def _promote_message_key(self, key: str):
        if key and not self._is_reserved_key(key):
            self._log[key] = self._log['message'].pop(key)

    def _is_reserved_key(self, key: str):
        return key in self.REQUIRED_JSON_LOG_KEYS + self.OPTIONAL_JSON_LOG_KEYS + ['message']