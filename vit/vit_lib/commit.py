import time
from vit import path_helpers
from vit import py_helpers
from vit.vit_lib.misc import (
    tree_fetch,
    file_name_generation,
    tracked_file_func
)
from vit.connection.vit_connection import ssh_connect_auto
from vit.custom_exceptions import *
from vit.file_handlers import repo_config

def commit_file(local_path, checkout_file, commit_mess,
                keep_file=False, keep_editable=False):

    file_track_data = tracked_file_func.get_file_track_data(local_path, checkout_file)
    _, _, user = repo_config.get_origin_ssh_info(local_path)

    with ssh_connect_auto(local_path) as ssh_connection:

        tree_asset, tree_asset_path = tree_fetch.fetch_up_to_date_tree_asset(
                ssh_connection,
                local_path,
                file_track_data["package_path"],
                file_track_data["asset_name"]
        )

        with tree_asset:

            raise_if_file_is_not_to_commit(
                file_track_data, tree_asset,
                user, checkout_file
            )

            new_file_path = file_name_generation.generate_unique_asset_file_path(
                file_track_data["package_path"],
                file_track_data["asset_name"],
                py_helpers.get_file_extension(checkout_file)
            )

            tree_asset.update_on_commit(
                path_helpers.localize_path(local_path, checkout_file),
                new_file_path,
                file_track_data["origin_file_name"],
                time.time(),
                user,
                commit_mess,
                keep_editable
            )

        ssh_connection.put_auto(checkout_file, new_file_path)
        ssh_connection.put_auto(tree_asset_path, tree_asset_path)

    if not keep_file:
        tracked_file_func.remove_tracked_file(local_path, checkout_file)
    else:
        tracked_file_func.update_tracked_file(local_path, checkout_file, new_file_path)
    return new_file_path

def list_commits(local_path, package_path, asset_name):
    with ssh_connect_auto(local_path) as ssh_connection:
        tree_asset, _ = tree_fetch.fetch_up_to_date_tree_asset(
            ssh_connection, local_path,
            package_path,asset_name
        )
        with tree_asset:
            commits = tree_asset.list_commits()
    return commits

def release_editable(local_path, checkout_file):

    file_track_data = tracked_file_func.get_file_track_data(local_path, checkout_file)
    _, _, user = repo_config.get_origin_ssh_info(local_path)

    with ssh_connect_auto(local_path) as ssh_connection:

        tree_asset, tree_asset_path = tree_fetch.fetch_up_to_date_tree_asset(
                ssh_connection,
                local_path,
                file_track_data["package_path"],
                file_track_data["asset_name"]
        )

        with tree_asset:
            if tree_asset.get_editor(file_track_data["origin_file_name"]) != user:
                raise Asset_NotEditable_E(checkout_file)
            tree_asset.remove_editor(file_track_data["origin_file_name"])

        ssh_connection.put_auto(tree_asset_path, tree_asset_path)

# -----------------------------------------------------------------------------

def raise_if_file_is_not_to_commit(file_track_data, tree_asset_open,
                                   user, checkout_file):
    if not file_track_data["changes"]:
        raise Asset_NoChangeToCommit_E(checkout_file)
    if tree_asset_open.get_editor(file_track_data["origin_file_name"]) != user:
        raise Asset_NotEditable_E(checkout_file)
    if not tree_asset_open.get_branch_from_file(file_track_data["origin_file_name"]):
        raise Asset_NotAtTipOfBranch(checkout_file, "FIXME blabla")

