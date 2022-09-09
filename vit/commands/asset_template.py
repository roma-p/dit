from vit import constants
from vit import py_helpers
from vit.connection.vit_connection import ssh_connect_auto
from vit.custom_exceptions import *
from vit.file_handlers.index_template import IndexTemplate


def create_asset_template(path, template_id, template_filepath, force=False):
    if not os.path.exists(template_filepath):
        raise Path_FileNotFound_E(template_filepath)

    with ssh_connect_auto(path) as sshConnection:

        sshConnection.get_vit_file(path, constants.VIT_TEMPLATE_CONFIG)

        with IndexTemplate(path) as index_template:

            if not force and not index_template.is_template_id_free(template_id):
                raise Template_AlreadyExists_E(template_id)

            template_scn_dst = os.path.join(
                constants.VIT_DIR,
                constants.VIT_TEMPLATE_DIR,
                os.path.basename(template_filepath)
            )

            index_template.reference_new_template(
                template_id,
                template_scn_dst,
                py_helpers.calculate_file_sha(template_filepath)
            )

        sshConnection.put_vit_file(path, constants.VIT_TEMPLATE_CONFIG)
        sshConnection.put(template_filepath, template_scn_dst)


def get_template(path, template_id):

    with ssh_connect_auto(path) as sshConnection:

        sshConnection.get_vit_file(path, constants.VIT_TEMPLATE_CONFIG)

        with IndexTemplate(path) as index_template:
            template_data = index_template.get_template_path_from_id(template_id)
            if not template_data:
                raise Template_NotFound_E(template_id)

        template_path_origin, sha256 = template_data
        template_path_local = os.path.join(
            path,
            os.path.basename(template_path_origin)
        )

        sshConnection.get(
            template_path_origin,
            template_path_local
        )
    return template_path_local