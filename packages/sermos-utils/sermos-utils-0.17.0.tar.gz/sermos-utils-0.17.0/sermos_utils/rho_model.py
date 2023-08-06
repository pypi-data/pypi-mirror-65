import logging
import os
import pprint
from json.decoder import JSONDecodeError
from typing import Dict, Type, Optional

import boto3
import io
import re
import requests
from boto3.s3.transfer import TransferConfig

from rho_ml.rho_model import RhoModel, StoredModel
from rho_ml.serialization import LocalModelStorage
from rho_ml.utils import Version
from sermos_utils.constants import DEFAULT_STORE_MODEL_URL, S3_MODEL_BUCKET, \
    DEFAULT_GET_MODEL_URL

logger = logging.getLogger(__name__)


def get_storage_key(model: Type[RhoModel], prefix: str) -> str:
    return "{0}/{1}_{2}".format(prefix, model.name, model.version)


def get_headers(api_key: str) -> Dict[str, str]:
    return {
        'Content-Type': 'application/json',
        'apikey': api_key
    }


def get_s3_client_from_api_response(response_data: Dict[str, str]):
    """ Get a valid s3 client based on credentials response from Sermos
    """
    try:
        access_key = response_data['aws_access_key']
        secret_key = response_data['aws_secret_key']
        session_token = response_data['aws_session_token']
        region = response_data['aws_region']
    except KeyError as e:
        logger.warning("Missing IAM keys in response:\n{0}"
                       .format(pprint.pformat(response_data)))
        raise e
    else:
        client = boto3.client('s3',
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key,
                              aws_session_token=session_token,
                              region_name=region)
        return client


def _get_transfer_config(max_concurrency: Optional[int] = None,
                         max_io_queue: Optional[int] = None,
                         multipart_chunksize: Optional[int] = None) -> \
        TransferConfig:
    kwargs = {}
    if max_concurrency:
        kwargs['max_concurrency'] = max_concurrency
    if max_io_queue:
        kwargs['max_io_queue'] = max_io_queue
    if multipart_chunksize:
        kwargs['multipart_chunksize'] = multipart_chunksize
    config = TransferConfig(**kwargs)
    return config


def store_rho_model(model: Type[RhoModel],
                    deploy_key: Optional[str] = None,
                    store_model_endpoint: Optional[str] = None,
                    max_concurrency: Optional[int] = None,
                    max_io_queue: Optional[int] = None,
                    multipart_chunksize: Optional[int] = None):
    """ Get S3 credentials from the sermos-admin API, then use the credentials
        to store the model and metadata in the appropriate bucket / subfolder

        TODO: come up w/ way to compare hashes of stored models and loaded
        models
    """
    logger.info(f"Attempting to serialize {model.name}")

    # Given a RhoModel, create a StoredModel instance and pickle it to bytes
    stored_model = model.build_stored_model()
    store_bytes = stored_model.to_pickle()
    f = io.BytesIO()
    f.write(store_bytes)
    f.seek(0)
    logger.info("Serialization finished, requesting credentials from API...")

    # Get deployment key from environment if not explicitly provided. Fail here
    # if it's also not defined in environment.
    if not deploy_key:
        deploy_key = os.environ['SERMOS_DEPLOY_KEY']

    if not store_model_endpoint:
        store_model_endpoint = DEFAULT_STORE_MODEL_URL

    headers = get_headers(api_key=deploy_key)
    post_data = {'model_key': model.name + '_' + str(model.version)}

    # Ask Sermos for credentials
    r = requests.post(url=store_model_endpoint, headers=headers, json=post_data)
    response_data = r.json()
    client = get_s3_client_from_api_response(response_data=response_data)
    storage_key = response_data['model_key']

    logger.info("Uploading serialized {0}"
                .format('_'.join([model.name, str(model.version)])))

    transfer_config = _get_transfer_config(
        max_concurrency=max_concurrency,
        max_io_queue=max_io_queue,
        multipart_chunksize=multipart_chunksize)

    client.upload_fileobj(
        f, Bucket=S3_MODEL_BUCKET, Key=storage_key, Config=transfer_config)


class ModelNotFoundError(Exception):
    pass


def get_model_search_api_response(model_name: str,
                                  version_pattern: str,
                                  deploy_key: str,
                                  get_model_endpoint: Optional[str] = None) \
        -> Dict[str, str]:
    headers = get_headers(api_key=deploy_key)
    if not get_model_endpoint:
        get_model_endpoint = DEFAULT_GET_MODEL_URL
    query_params = {
        'model_name': model_name,
        'version_pattern': version_pattern
    }
    logger.debug("Requesting storage info from Admin API...")
    r = requests.post(
        url=get_model_endpoint, headers=headers, json=query_params)
    try:
        response_data = r.json()
    except JSONDecodeError:
        logger.warning(f"Could not decode search API response!  "
                       f"Server response: {r.content}")
        raise ModelNotFoundError(f"Invalid response received from admin API!\n"
                                 f" {r.content}")
    except Exception as e:
        logger.exception(e)
        raise e

    return response_data


def get_stored_model_json_from_api_response(response_data: Dict[str, str]) \
        -> bytes:
    """ Given a model search response from Sermos, retrieve the StoredModel
    """
    client = get_s3_client_from_api_response(response_data=response_data)
    model_key = response_data['model_key']
    if not model_key:
        raise ModelNotFoundError("No model key found!")

    logger.debug("Retrieving {0} from storage...".format(model_key))
    s3_response = client.get_object(Bucket=S3_MODEL_BUCKET, Key=model_key)
    model_json = s3_response['Body'].read()

    return model_json


def get_local_storage(base_path: Optional[str]) -> LocalModelStorage:
    if base_path:
        result = LocalModelStorage(base_path=base_path)
    else:
        result = LocalModelStorage()
    return result


def get_local_model(model_name: str,
                    version_pattern: str,
                    local_base_path: str) -> Optional[RhoModel]:
    """ Search for a local model by name and version and instantiate it
    if found. """
    local_storage = get_local_storage(base_path=local_base_path)
    local_key = local_storage.get_key_from_pattern(
        model_name=model_name, version_pattern=version_pattern)
    if local_key:
        logger.info("Local model found with filename: {0}".format(local_key))
        result = local_storage.retrieve(local_key)
        return result


def get_version_from_key(key: str) -> Version:
    m = re.search(r'[0-9]+\.[0-9]+\.[0-9]+', key)
    if m:
        version_string = m.group()
        result = Version.from_string(version_string)
        return result
    else:
        raise ValueError(f"Couldn't create Version from {key}!")


def rho_model_loader(model_name: str,
                     version_pattern: str,
                     deploy_key: Optional[str] = None,
                     local_base_path: Optional[str] = None,
                     save_to_local_disk: bool = True,
                     get_model_endpoint: Optional[str] = None,
                     force_search: bool = False) -> Type[RhoModel]:
    """ Retrieve models stored using the Sermos Admin API by name and
    version.

    Optionally cache the result locally for later use (caching on by
    default). If force_search == True, always check cloud storage,
    regardless of whether or not """
    if not deploy_key:
        deploy_key = os.environ['SERMOS_DEPLOY_KEY']
    if force_search:
        api_response = get_model_search_api_response(
            model_name=model_name, version_pattern=version_pattern,
            deploy_key=deploy_key, get_model_endpoint=get_model_endpoint)
        model_key = api_response['model_key']
        remote_version = get_version_from_key(key=model_key)

    force_get_remote = False
    model = get_local_model(model_name=model_name,
                            version_pattern=version_pattern,
                            local_base_path=local_base_path)

    if model and force_search:
        if model.version < remote_version:
            force_get_remote = True
    if (not model) or force_get_remote:
        if not force_search:
            api_response = get_model_search_api_response(
                model_name=model_name, version_pattern=version_pattern,
                deploy_key=deploy_key, get_model_endpoint=get_model_endpoint)
        stored_bytes = get_stored_model_json_from_api_response(
            response_data=api_response)
        stored_model = StoredModel.from_pickle(s=stored_bytes)
        model = stored_model.load_model()
        if save_to_local_disk:
            logger.info("Caching retrieved model {0} locally..."
                        .format(model.name))
            local_storage = get_local_storage(base_path=local_base_path)
            local_storage.store(model=model)
    return model
