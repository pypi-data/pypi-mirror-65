# Sermos Utils

Utilities for interacting with Sermos.

## Deployments

### Prerequisites

To deploy your application to Sermos, there are a few prerequisites:

1. Deployment environment created and configured
1. A `deploy key` has been issued for that deployment
1. Your app is a valid Python package with a standard structure (see below)
1. You have a `sermos.yaml` file written with your defined API endpoints, workers, etc.
1. Your application has `sermos-utils` as a dependency and it's installed.

### Deployment

You can initiate a Sermos deployment in two ways: programmatically or using the
CLI tool.

It is recommended to keep your deployment key in the environment and to set the
client package directory in the environment as well, for convenience.

    SERMOS_DEPLOY_KEY=abc123
    SERMOS_CLIENT_PKG_NAME=your_package

#### Programmatic Deployment

Invoking a pipeline programmatically (e.g. as part of a build pipeline) can
be done similar to below (assumes deployment key/client package direcotry
are available in the environment per note above).

    from sermos_utils.deploy import SermosDeploy

    sd = SermosDeploy()
    status = sd.invoke_deployment()
    print(status)

#### CLI Deployment

For a cli-based deployment, there is a `sermos_deploy` command installed
as part of the sermos-utils package.

    honcho run -e .env sermos_deploy

### Deployment Status

Assuming your environment is set up per notes in the `Deployment` section above:

#### Programmatic Status Checks

    from sermos_utils.deploy import SermosDeploy

    sd = SermosDeploy()
    status = sd.get_deployment_status()
    print(status)

#### CLI Status Checks

    honcho run -e .env sermos_status

### Proper Python Package Structure

Assuming your package is called "my_sermos_client":

    /path/to/codebase/
        my-sermos-client/
            setup.py
            my_sermos_client/
                __init__.py
                sermos.yaml

`my_sermos_client/__init__.py` has only one requirement, to contain your
application's version assigned as a variable `__version__`, e.g.:

    __version__ = '0.1.0'

Common practice is to use that value in your `setup.py` file, e.g.

    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open('my_sermos_client/__init__.py', 'rb') as f:
        __version__ = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))

## Local Development

Sermos provides a local development environment in two ways:

1. Local 'sandbox' environment
1. Cloud-connected environment that proxies into your deployment's databases

See `sermos-utils/dev/README.md` for more information.

## Testing

To run the tests you need to have `pyenv` running on your system and `tox` in
your environment.

Refer to RhoAI documentation for instructions on installing `pyenv` correctly.

After `pyenv` is intalled, then install `tox`

    $ pip install tox

Then install the different python versions in `pyenv`

    $ pyenv install 3.7.4

Now, run the tests:

    $ tox
