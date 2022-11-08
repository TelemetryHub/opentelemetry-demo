#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
from pythonjsonlogger import jsonlogger
from opentelemetry import trace

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
    set_logger_provider,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("otelTraceID"):
            log_record["otelTraceID"] = trace.format_trace_id(
                trace.get_current_span().get_span_context().trace_id
            )
        if not log_record.get("otelSpanID"):
            log_record["otelSpanID"] = trace.format_span_id(
                trace.get_current_span().get_span_context().span_id
            )


def getOtelLogHandler():
    log_exporter = OTLPLogExporter()
    # print(f"Exporter endpoint: {log_exporter.endpoint}")
    # print(repr(log_exporter))
    # log_emitter_provider = LogEmitterProvider()
    # raise SystemExit()
    # set_log_emitter_provider(log_emitter_provider)
    logger_provider = LoggerProvider()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    return LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)


def getJSONLogger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(getOtelLogHandler())
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
