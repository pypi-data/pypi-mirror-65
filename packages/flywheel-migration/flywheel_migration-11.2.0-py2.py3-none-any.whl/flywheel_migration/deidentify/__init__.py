"""Provides de-identification and subject mapping functionality"""
import json
import logging
import os

from ruamel.yaml import YAML

from . import file_profile
from . import dicom_file_profile
from . import jpg_file_profile

from .factory import load_subject_map, create_subject_map
from .deid_profile import DeIdProfile
from .validation_error import ValidationError

log = logging.getLogger('deidentify')


def load_deid_profile(name, enhanced=False):
    """Helper function to load profile either at path or one of the defaults"""
    if os.path.isfile(name):
        return load_profile(name, enhanced=enhanced)

    # Load default profiles
    profiles = load_default_profiles()
    for profile in profiles:
        if profile.name == name:
            return profile

    raise ValueError('Unknown de-identification profile: {}'.format(name))


def load_profile(path, enhanced=False):
    """Load the de-identification profile at path"""
    _, ext = os.path.splitext(path.lower())

    config = None
    try:
        if ext == '.json':
            with open(path, 'r') as f:
                config = json.load(f)
        elif ext in ['.yml', '.yaml']:
            with open(path, 'r') as f:
                yaml = YAML()
                config = yaml.load(f)
    except ValueError:
        log.exception('Unable to load config at: %s', path)

    if not config:
        raise ValueError('Could not load config at: {}'.format(path))

    profile = DeIdProfile()
    profile.load_config(config)

    errors = profile.validate(enhanced=enhanced)
    if errors:
        raise ValidationError(path, errors)

    return profile


def load_default_profiles():
    """Load default de-identification profiles"""
    src_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(src_dir, 'deid-profiles.yml')

    results = []

    with open(path, 'r') as f:
        yaml = YAML()
        profiles = yaml.load(f)

    for config in profiles:
        profile = DeIdProfile()
        profile.load_config(config)
        results.append(profile)

    return results
