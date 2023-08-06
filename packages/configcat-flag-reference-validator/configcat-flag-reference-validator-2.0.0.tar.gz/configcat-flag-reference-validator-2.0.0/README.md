# feature-flag-reference-validator 
[![PyPI](https://img.shields.io/pypi/v/configcat-flag-reference-validator.svg)](https://pypi.python.org/pypi/configcat-flag-reference-validator) [![Docker version](https://img.shields.io/badge/docker-latest-blue)](https://hub.docker.com/r/configcat/feature-flag-reference-validator)

This CLI utility discovers ConfigCat feature flag usages in your source code and validates them against your feature flags on the ConfigCat Dashboard.

## About ConfigCat

Manage features and change your software configuration using [ConfigCat feature flags](https://configcat.com), without the need to re-deploy code. A [10 minute trainable Dashboard](https://app.configcat.com) allows even non-technical team members to manage features directly. Deploy anytime, release when confident. Target a specific group of users first with new ideas. Supports A/B/n testing and soft launching. Provides [open-source SDKs](https://github.com/configcat) for easy integration with any web, mobile or backend application.

## Installation

This CLI tool is written in python so you have to have python installed on your system.

1. Install the [The silver searcher](https://github.com/ggreer/the_silver_searcher) used for source code scanning.
    - Linux
        ```bash
        apt-get install silversearcher-ag
        ```
    - Windows
        ```powershell
        choco install ag
        ```
2. Install the reference validator using pip.
    ```bash
    pip install configcat-flag-reference-validator
    ```
3. Execute the validator.
    ```bash
    configcat-validator.py [YOUR-CONFIGCAT-SDKKEY] [DIRECTORY-TO-SCAN] 
    ```

### Docker

Pull the configcat/feature-flag-reference-validator docker image to your environment. The image provides an entry point `configcat-validator.py` to execute the validator.
```powershell
docker pull configcat/feature-flag-reference-validator

docker run configcat-validator.py [YOUR-CONFIGCAT-SDKKEY] [DIRECTORY-TO-SCAN]
```

## Arguments

| Name                       | Required | Default value     | Description                                                                            |
| -------------------------- | -------- | ----------------- | -------------------------------------------------------------------------------------- |
| configcat_sdk_key          | yes      | N/A               | The SDK Key of your ConfigCat project.                                                 |
| search_dir                 | yes      | N/A               | The directory to scan for flag references.                                             |
| -s, --configcat_cdn_server | no       | cdn.configcat.com | The domain name of the ConfigCat CDN where you ConfigCat configuration file is stored. |
| -f, --fail_on_warnings     | no       | false             | Signals an error when the validation fails. By default only warnings are showed.       |
| -v, --verbose              | no       | false             | Turns on detailed logging.                                                             |

## Example
The following command will execute a flag reference validation on the ./repo folder and signals a failure when it finds flag key mismatches.
```bash
configcat-validator.py \
    [YOUR-CONFIGCAT-SDKKEY] \
    ./repo \
    --fail_on_warnings \
    --verbose
```
Output:
```bash
INFO:configcat.reference_validator.config_fetcher:Fetching the current ConfigCat configuration from cdn.configcat.com.
INFO:configcat.reference_validator.config_fetcher:Successful fetch, 2 settings found: ['key1', 'key2'].
INFO:configcat.reference_validator.reference_finder:Scanning the ./repo directory for ConfigCat setting references.
INFO:configcat.reference_validator.reference_finder:6 references found: {'key1', 'key2', 'key3'}.
WARNING:configcat.reference_validator.reference_validator:Feature flag/Setting keys not found in ConfigCat (but present in source code): {'key3'}.
Exited with code 1
```

## CI Integrations
- [CircleCI Orb](https://circleci.com/orbs/registry/orb/configcat/feature-flag-reference-validator)

## About ConfigCat
- [Documentation](https://configcat.com/docs)
- [Blog](https://blog.configcat.com)
