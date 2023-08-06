# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Download and load model explanation configuration."""
from typing import Any, Dict, Optional, Union
from logging import Logger, LoggerAdapter
import json
import os
import time

from azureml.automl.core._downloader import Downloader
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import ConfigException


class AutoMLModelExplanationConfig:
    """Holder for model explanation configurations."""

    CONFIG_DOWNLOAD_PREFIX = "https://aka.ms/automl-resources/configs/"
    CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.0.json"
    REMOTE_CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.1.json"

    DEFAULT_CONFIG_PATH = "../model_explanation_config_v1.0.json"

    def __init__(self, logger: Optional[Union[Logger, LoggerAdapter]] = None) -> None:
        self._logger = logger or logging_utilities.get_logger()

    def get_config(self, is_remote: bool = False) -> Dict[str, Any]:
        """Provide configuration."""
        try:
            if is_remote:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX,
                                                self.REMOTE_CONFIG_DOWNLOAD_FILE, os.getcwd(),
                                                prefix=str(time.time()))
            else:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX, self.CONFIG_DOWNLOAD_FILE,
                                                os.getcwd(), prefix=str(time.time()))
            if file_path is None:
                raise ConfigException("Model explanation configuration url is not accessible!")

            with open(file_path, 'r') as f:
                cfg = json.load(f)  # type: Dict[str, Any]
                self._logger.debug("Successfully downloaded the model explanations configuration from the remote.")

            os.remove(file_path)
            return cfg
        except Exception:
            self._logger.debug("Error encountered reading model explanation configuration." +
                               "Falling back to default configuration")
            return self.default()

    def default(self) -> Dict[str, Any]:
        """Return the default back up configuration."""
        default_config_path = os.path.abspath(os.path.join(__file__, self.DEFAULT_CONFIG_PATH))
        with open(default_config_path, "r") as f:
            result = json.loads(f.read())  # type: Dict[str, Any]
            self._logger.debug("Read model explanations config from SDK.")
            return result
