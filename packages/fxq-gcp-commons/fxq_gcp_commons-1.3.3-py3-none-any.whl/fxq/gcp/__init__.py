import logging
from http import HTTPStatus

from fxq.env import Environment

from fxq.gcp.cloud_func import CloudFunctionResponse, Error, Success

LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
DEFAULT_LOGGING_LEVEL = logging.WARN
LOGGING_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def get_app_status(env: Environment, exposed_fields=("name", "description", "version"), health_check=None):
    """
    Gets the Cloud Function Status from the environment object and augments with Health information.

    By Default exposes the app name, description, version and active_profiles and sets the health status to OK

    Example Usage:

        def fail_health_check(response):
            response["health"] = "DOWN"
            return response

        def health():
            return get_app_status(health_check=fail_health_check)


    :param env: Application Environment object with the properties already loaded
    :param exposed_fields: List of Fields to Expose from the package.json
    :param health_check: Health Check Function to call, function receives the response and should return the response
    :return: Returns a dictionary with the version and health of the app
    """
    resp = {
        "status": "OK"
    }

    for k, v in env.get_property("app").items():
        if k in exposed_fields:
            resp[k] = v

    resp["active_profiles"] = env.active_profiles

    if health_check:
        health_check(resp)

    return resp


def propagate_logging_level_from_request(request):
    """
    Propagates the logging level through the application to enable log level override
    in a Cloud Function.

    Using the following request parameter on the URL will allow the request to have
    a different than standard logging level:

    http://127.0.0.1:5000/logtest?loglev=debug

    :param request: Takes the request object to extract the parameters
    :return: No Return Value
    """
    if 'loglev' not in request.values:
        return

    requested_level = request.values['loglev']
    try:
        _ll = LOGGING_LEVELS[requested_level]
        logging.getLogger().setLevel(_ll)
        logging.getLogger('werkzeug').setLevel(_ll)
        logging.info(f'Set Log Level to {requested_level} {_ll}')
    except KeyError:
        logging.warning(
            f'Requested log level {requested_level} is not available, try {",".join(LOGGING_LEVELS.keys())}')
    except Exception as e:
        logging.error("Failed to get logging level", e)
    return


def handle_cloud_function(req, request_map: dict):
    """
    Handle the Cloud Function/Flask Request.

    Takes the request object from Flask and Routes to the associated method defined in the request map

    Request Map Dictionary should key, value pairs where key is the route i.e. /publishers/fxcm and the value is the
    function that should be called.

    :param req: Flas request Object
    :param request_map: Dictionary of paths to functions
    :return: Returns the return value of the function defined in the request map
    """
    response: CloudFunctionResponse
    try:
        message = request_map[req.path]()
        response = Success.Builder().with_body(message).build()
    except KeyError:
        return Error.Builder() \
            .with_message(f'No Action at route {req.path}') \
            .with_code(HTTPStatus.NOT_FOUND) \
            .build()
    except Exception as e:
        logging.error("Error running report", e)
        response = Error.Builder().build()
    finally:
        logging.info("== DONE ==")

    return response
