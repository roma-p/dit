import os
import json

from vit import constants
from vit import py_helpers
from vit import path_helpers

cfg_filepath = constants.VIT_TEMPLATE_CONFIG

def create(path):
    return py_helpers.create_empty_json(
        path_helpers.get_vit_file_config_path(path, cfg_filepath),
    )

def reference_new_template(path, template_id, template_filepath, sha256):
    return py_helpers.update_json(
        path_helpers.get_vit_file_config_path(path, cfg_filepath),
        {template_id:[template_filepath, sha256]} # and a hash in case file is changed?
    )

def get_template_path_from_id(path, template_id):
    return py_helpers.get_json_main_key(
        path_helpers.get_vit_file_config_path(path, cfg_filepath),
        template_id
    )

def is_template_id_free(path, template_id):
    return not bool(get_template_path_from_id(path, template_id))

def get_template_data(path):
    return {
        template_id: os.path.basename(template_data[0])
        for template_id, template_data in py_helpers.parse_json(
            path_helpers.get_vit_file_config_path(path, cfg_filepath)
        ).items()
    }
