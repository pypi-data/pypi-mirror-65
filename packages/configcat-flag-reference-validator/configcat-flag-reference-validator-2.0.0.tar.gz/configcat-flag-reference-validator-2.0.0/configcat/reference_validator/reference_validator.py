import logging
import sys

log = logging.getLogger(sys.modules[__name__].__name__)


class ReferenceValidator:
    def __init__(self):
        pass

    @staticmethod
    def validate(remote_keys,
                 reference_keys):
        missing_references = remote_keys.difference(reference_keys)
        missing_remote_keys = reference_keys.difference(remote_keys)

        is_failed = len(missing_references) > 0 or len(missing_remote_keys) > 0
        if is_failed:
            log.warning("Found unused feature flags!")

        if len(missing_references) > 0:
            log.debug(
                "Feature flag/Setting keys not found in source code (but present in ConfigCat): %s.",
                missing_references)
            for item in missing_references:
                log.warning("Clean up '%s' from ConfigCat Dashboard.", item)

        if len(missing_remote_keys) > 0:
            log.debug(
                "Feature flag/Setting keys not found in ConfigCat (but present in source code): %s.",
                missing_remote_keys)
            for item in missing_remote_keys:
                log.warning("Clean up '%s' from code.", item)

        return not is_failed
