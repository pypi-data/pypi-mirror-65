# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains utility methods used in automated ML in Azure Machine Learning."""
from typing import Any, Union, Optional, Tuple
from types import ModuleType
from datetime import datetime
import importlib
import importlib.util
import importlib.abc
import logging
import os
import numpy as np
import pytz

from azureml.core import Run
from azureml.automl.core.shared import constants
from azureml.automl.runtime.shared.types import DataSingleColumnInputType
from azureml.train.automl.exceptions import ConfigException, FileNotFoundException
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings


def _load_user_script(script_path: str, logger: logging.Logger, calling_in_client_runtime: bool = True) -> ModuleType:
    #  Load user script to get access to GetData function
    logger.info('Loading data using user script.')

    module_name, module_ext = os.path.splitext(os.path.basename(script_path))
    if module_ext != '.py':
        raise ConfigException.create_without_pii('The provided user script was not a Python file.')
    spec = importlib.util.spec_from_file_location('get_data', script_path)
    if spec is None:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                           target="LoadUserScript")

    module_obj = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ConfigException.create_without_pii('The provided user script is a namespace package, '
                                                 'which is not supported.')

    # exec_module exists on 3.4+, but it's marked optional so we have to assert
    assert isinstance(spec.loader, importlib.abc.Loader)
    assert spec.loader.exec_module is not None
    _execute_user_script_object(spec, calling_in_client_runtime, script_path, module_obj)
    return module_obj


def _execute_user_script_object(spec: Any, calling_in_client_runtime: bool, script_path: str, module_obj: Any) -> Any:
    """Execute the loaded user script to obtain the data."""
    try:
        spec.loader.exec_module(module_obj)
    except FileNotFoundError:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            if not os.path.exists(script_path):
                raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                               target="LoadUserScript")
            else:
                raise ConfigException.create_without_pii(
                    'The provided user script references files that are not in the project folder.')
    except Exception as e:
        raise ConfigException.from_exception(
            e,
            target="module_obj",
            reference_code="_execute_user_script_object.module_obj.exception").with_generic_msg(
            'Exception while executing user script.'
        )

    if not hasattr(module_obj, 'get_data'):
        raise ConfigException.with_generic_msg('The provided user script does not implement get_data().')

    return module_obj


def _get_run_createdtime_starttime_and_endtime(run: Optional[Run]) -> Tuple[Optional[datetime],
                                                                            Optional[datetime],
                                                                            Optional[datetime]]:
    def _get_utc_time(datetime_str: Optional[str]) -> Optional[datetime]:
        if datetime_str is not None and isinstance(datetime_str, str):
            try:
                return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
            except Exception:
                pass

        return None

    if run is None or run._run_dto is None:
        return None, None, None

    created_time_utc = _get_utc_time(run._run_dto.get('created_utc'))
    start_time_utc = _get_utc_time(run._run_dto.get('start_time_utc'))
    end_time_utc = _get_utc_time(run._run_dto.get('end_time_utc'))

    return created_time_utc, start_time_utc, end_time_utc


def _calculate_start_end_times(start_time: datetime, end_time: datetime, run: Optional[Run]) -> Tuple[datetime,
                                                                                                      datetime]:
    _, run_start_time, run_end_time = _get_run_createdtime_starttime_and_endtime(run)
    start_time = run_start_time or start_time
    end_time = run_end_time or end_time
    return start_time, end_time
