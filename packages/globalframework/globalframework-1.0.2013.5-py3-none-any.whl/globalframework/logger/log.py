import logging
import time
import os
import datetime
import platform
from pathlib import Path

from globalframework.enumeration import LoggerSeverityType, OperatingSystemTypes


today = str(datetime.datetime.utcnow().date())
logging.Formatter.converter = time.gmtime
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
log.setLevel(logging.INFO)

FREQ = {
    'Mins': {'range': 61, 'ext': 'm', 'func': time.gmtime().tm_min},
    'Hours': {'range': 25, 'ext': 'h', 'func': time.gmtime().tm_hour},
    'Days': {'range': 32, 'ext': 'd', 'func': time.gmtime().tm_mday},
    'Months': {'range': 13, 'ext': 'M', 'func': time.gmtime().tm_mon}
}


class Logger:

    def __init__(self, logger_name='FCSGLOBALFRAMEWORK', debug=False):
        self.logger_name = logger_name
        self.debug = debug

    def _get_config(self):

        get_instance = _LoggerProvider(self.logger_name)
        logger_attributes_dict = get_instance.get_attributes

        self.name = logger_attributes_dict['FileName']
        self.directory = logger_attributes_dict['FileLocation']
        self.format = logger_attributes_dict['FileNameFormat']
        self.ext = logger_attributes_dict['FileExtension']
        self.freqname = logger_attributes_dict['FrequencyTypeName']
        self.freq = logger_attributes_dict['FrequencyValue']

    def _create_prefix(self):
        self._get_config()
        interval = self.freq
        start_range = FREQ[self.freqname]['range']
        get_func = FREQ[self.freqname]['func']
        ext = FREQ[self.freqname]['ext']

        if interval != 1:
            freq = [i for i in range(0, start_range, interval)]
            file_ext = [
                str(i) + '-' + str((range(i, j))[-1])
                for i, j in zip(freq, freq[1:])
            ]
            self.prefix = file_ext[get_func // interval] + ext
            return self.prefix

        self.prefix = str(get_func) + ext
        return self.prefix

    def _create_filename(self):
        self._create_prefix()
        if not Path(self.directory).is_dir():
            os.makedirs(self.directory)

        format_dict = {'{DATE}': str(
            today), '{NAME}': self.name, '{FQ}': self.prefix}
        self.format = self.format.split('-')

        self.filename = self.directory + \
            '_'.join(str(format_dict[i]) for i in self.format) + '.' + self.ext

    def write(self, message: str, message_type: LoggerSeverityType, indentifier_id=None):
        self._create_filename()
        level = message_type.lower()
        message = f"{indentifier_id}: {message}"
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d-[%(levelname)s]:%(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
        fh = logging.FileHandler(self.filename)
        if self.debug:
            log.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.handlers.clear()
        log.addHandler(fh)
        getattr(log, level)(message)


class _LoggerProvider(Logger):

    @property
    def get_attributes(self):
        attributes_dict = {
            'FileName': 'globalframework',
            'FileLocation': '/home/fcs/logs/',
            'FileNameFormat': '{DATE}-{NAME}-{FQ}',
            'FileExtension': 'txt',
            'FrequencyTypeName': 'Hours',
            'FrequencyValue': 4
        }

        os = platform.system()
        os_id = getattr(OperatingSystemTypes, os.upper()).value

        if self.logger_name != 'FCSGLOBALFRAMEWORK':
            try:
                from globalframework.logger.provider import LoggingProvider
                with LoggingProvider() as lp:
                    logger_name_dict = lp.get_loggername()
                    self.logger_name = logger_name_dict.get(
                        self.logger_name.upper(), 'FCSGLOBALFRAMEWORK')
                    if self.logger_name != 'FCSGLOBALFRAMEWORK':
                        logger_attributes_dict = lp.get_loggerattributes(
                            self.logger_name, os_id)
                        logger_freq_dict = lp.get_frequency(self.logger_name)

                        attributes_dict = {
                            **logger_attributes_dict, **logger_freq_dict}
                        return attributes_dict
            except Exception:
                pass

        if os == 'Windows':
            attributes_dict['FileLocation'] = 'D:\\logs\\Root\\'
        return attributes_dict
