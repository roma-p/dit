from vit import constants
from vit.custom_exceptions import *
from vit.vit_lib import (
    asset_template,
    asset, branch, checkout,
    clean, commit, infos, package,
    repo_init_clone, tag, rebase, update
)
from vit.command_line_lib import graph as graph_module
from vit.command_line_lib import log as log_module

import logging
log = logging.getLogger("vit")
log.setLevel(logging.INFO)


def is_vit_repo():
    current_path = os.getcwd()
    s = os.path.exists(
        os.path.join(
            current_path,
            constants.VIT_DIR
        )
    )
    if not s:
        log.error("{} is not a vit repository".format(current_path))
    return s


def parse_ssh_link(link):
    if ":" not in link:
        return None
    split = link.split(":")
    if len(split) != 2:
        return None
    host, path = link.split(":")
    if "@" in host:
        split = host.split("@")
        if len(split) > 2:
            return None
        user, host = split
    else:
        user = input("username:")
    if not user or not host or not path:
        return None
    return user, host, path


def init(name):
    try:
        repo_init_clone.init_origin(
            os.path.join(
                os.getcwd(),
                name
            )
        )
    except (
            Path_AlreadyExists_E,
            Path_ParentDirNotExist_E,
            Exception) as e:
        log.error("Could not initialize repository {}:".format(name))
        log.error(str(e))
        return False
    else:
        log.info("Repository successfully initialized at {}".format(name))
        return True


def clone(origin_link):

    origin_link = parse_ssh_link(origin_link)
    if not origin_link:
        log.error("{} is not a valid ssh link")
        return False
    user, host, origin_path = origin_link

    repository_name = os.path.basename(origin_path)
    clone_path = os.path.join(
        os.getcwd(),
        repository_name
    )

    try:
        repo_init_clone.clone(origin_path, clone_path, user, host)
    except (
            Path_AlreadyExists_E,
            Path_ParentDirNotExist_E,
            SSH_ConnectionError_E,
            OriginNotFound_E) as e:
        log.error("Could not clone repository {}:".format(origin_link))
        log.error(str(e))
        return False
    else:
        log.info("{} successfully cloned at: {}".format(
            repository_name,
            clone_path
        ))
        return True


def create_template(template_name, file_path, force=False):
    if not is_vit_repo(): return False
    try:
        asset_template.create_template_asset(
            os.getcwd(),
            template_name,
            file_path,
            force
        )
    except (
            Path_FileNotFound_E,
            RepoIsLock_E,
            SSH_ConnectionError_E,
            Template_AlreadyExists_E) as e:
        log.error("Could not create template {} from {}".format(
            template_name,
            file_path
        ))
        log.error(str(e))
        return False
    else:
        log.info("template {} successfully created from file {}".format(
            template_name,
            file_path))
        return True


def create_package(path):
    if not is_vit_repo(): return False
    try:
        package.create_package(
            os.getcwd(),
            path,
            force_subtree=False
            # TODO: add option for this....
        )
    except (
            SSH_ConnectionError_E,
            RepoIsLock_E,
            Path_AlreadyExists_E,
            Path_ParentDirNotExist_E) as e:
        log.error("Could not create package {}".format(path))
        log.error(str(e))
        return False
    else:
        log.info("Package successfully created at {}".format(path))
        return True


def create_asset_from_template(package, asset_name, template):
    if not is_vit_repo(): return False
    try:
        asset.create_asset_from_template(
            os.getcwd(),
            package, asset_name, template
        )
    except (
            SSH_ConnectionError_E,
            RepoIsLock_E,
            Package_NotFound_E,
            Path_AlreadyExists_E,
            Template_NotFound_E) as e:
        log.error("Could not create asset {}".format(asset_name))
        log.error(str(e))
        return False
    else:
        log.info("Asset {} successfully created at {}".format(
            asset_name, package))
        return True


def create_asset_from_file(package, asset_name, file):
    if not is_vit_repo(): return False
    try:
        asset.create_asset_from_file(
            os.getcwd(),
            package, asset_name, file
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Path_AlreadyExists_E,
            Path_FileNotFound_E) as e:
        log.error("Could not create asset {}".format(asset_name))
        log.error(str(e))
        return False
    else:
        log.info("Asset {} successfully created at {}".format(
            asset_name, package))
        return True


def checkout_asset_by_branch(package, asset, branch, editable, reset):
    if not is_vit_repo(): return False
    try:
        checkout_file = checkout.checkout_asset_by_branch(
            os.getcwd(), package, asset,
            branch, editable, reset
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Branch_NotFound_E,
            Asset_AlreadyEdited_E,
            Asset_NotFound_E) as e:
        log.error("Could not checkout asset {}.".format(asset))
        log.error(str(e))
        return False
    else:
        log.info("asset {} successfully checkout at {}".format(
            asset, checkout_file))
        return True

def checkout_asset_by_tag(package_id, asset_id, tag_id, reset):
    if not is_vit_repo(): return False
    try:
        checkout_file = checkout.checkout_asset_by_tag(
            os.getcwd(), package_id,
            asset_id, tag_id, reset
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Tag_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not checkout asset {}.".format(asset_id))
        log.error(str(e))
        return False
    else:
        log.info("asset {} successfully checkout at {}".format(
            asset_id, checkout_file))
        return True

def checkout_asset_by_commit(package_id, asset_id, commit_id, reset):
    if not is_vit_repo(): return False
    try:
        checkout_file = checkout.checkout_asset_by_commit(
            os.getcwd(), package_id,
            asset_id, commit_id, reset
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Commit_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not checkout asset {}.".format(asset))
        log.error(str(e))
        return False
    else:
        log.info("asset {} successfully checkout at {}".format(
            asset_id, checkout_file))
        return True


def commit_func(file, message, keep_file, keep_editable):
    # FIXME: handle multiple commits at once?
    #   (and ask for confirmation).
    err = "Could not commit file {}".format(file)
    if not is_vit_repo(): return False
    try:
        commit.commit_file(
            os.getcwd(), file, message,
            keep_file, keep_editable
        )
    except Asset_NotEditable_E as e:
        log.error(err)
        log.error(str(e))
        log.info("* you can try to fetch it as editable so you can commit it")
        log.info("    following line won't overwrite your local modification")
        log.info("    vit update {} -e".format(file))
        return False
    except (
            Asset_NotFound_E,
            Asset_UntrackedFile_E,
            Asset_NoChangeToCommit_E,
            Asset_NotAtTipOfBranch_E,
            RepoIsLock_E,
            SSH_ConnectionError_E) as e:
        log.error(err)
        log.error(str(e))
        return False
    else:
        log.info("file {} successfully committed".format(file))
        return True


def free(file):
    if not is_vit_repo(): return False
    try:
        commit.release_editable(os.getcwd(), file)
    except (
            Asset_NotFound_E,
            Asset_UntrackedFile_E,
            RepoIsLock_E,
            Asset_NotEditable_E,
            SSH_ConnectionError_E) as e:
        log.error(err)
        log.error(str(e))
        return False
    else:
        log.info("file {} successfully freed, now can be checkout as editable. ".format(file))
        return True


def rebase_from_commit(package, asset, branch, commit):
    if not is_vit_repo(): return False
    _str = "rebased branch {} of asset {} to commit {}".format(branch, asset, commit)
    try:
        rebase.rebase_from_commit(
            os.getcwd(), package,
            asset, branch, commit
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            Asset_NotFound_E,
            RepoIsLock_E,
            Branch_NotFound_E,
            Commit_NotFound_E,
            Asset_AlreadyEdited_E,
            Path_FileNotFoundAtOrigin_E) as e:
        log.error("Could not {}".format(_str))
        log.error(str(e))
        return False
    else:
        log.info("successfully {}".format(_str))
        return True


def update_func(checkout_file, editable=False, reset=False):
    if not is_vit_repo(): return False
    try:
        update.update(os.getcwd(), checkout_file, editable, reset)
    except(
            SSH_ConnectionError_E,
            Package_NotFound_E,
            Asset_NotFound_E,
            RepoIsLock_E,
            Asset_UntrackedFile_E,
            Asset_UpdateOnNonBranchCheckout_E,
            Asset_ChangeNotCommitted_E,
            Asset_AlreadyUpToDate_E) as e:
        log.error("Could not update file {}".format(checkout_file))
        log.error(str(e))
        return False
    else:
        log.info("{} successfully updated".format(checkout_file))
        return True


def create_branch_from_origin_branch(
        package, asset, branch_new,
        branch_parent, create_tag):
    if not is_vit_repo(): return False
    try:
        branch.branch_from_origin_branch(
            os.getcwd(), package, asset,
            branch_parent, branch_new,
            create_tag
        )
    except (
            SSH_ConnectionError_E,
            Asset_NotFound_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Branch_NotFound_E,
            Branch_AlreadyExist_E) as e:
        log.error("Could not create branch {}".format(branch_parent))
        log.error(str(e))
        return False
    else:
        log.info("Successfully created branch {} from branch {}".format(
            branch_new, branch_parent
        ))
        return True


def create_tag_light_from_branch(package, asset, branch, tag_name):
    if not is_vit_repo(): return False
    try:
        tag.create_tag_light_from_branch(
            os.getcwd(), package, asset,
            branch, tag_name
        )
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Asset_NotFound_E,
            Branch_NotFound_E,
            Tag_AlreadyExists_E,
            Tag_NameMatchVersionnedTag_E) as e:
        log.error("Could not tag create {} for asset {}".format(tag_name, asset))
        log.error(str(e))
        return False
    else:
        log.info("Successfully tagged {} {} to {} from {}".format(
            package, asset,
            tag_name, branch
        ))
        return True


def create_tag_annotated_from_branch(package, asset, branch, tag_name, message):
    if not is_vit_repo(): return False
    try:
        tag.create_tag_annotated_from_branch(
            os.getcwd(), package, asset,
            branch, tag_name, message
        )
    except (
            SSH_ConnectionError_E,
            Asset_NotFound_E,
            Package_NotFound_E,
            RepoIsLock_E,
            Branch_NotFound_E,
            Tag_AlreadyExists_E,
            Tag_NameMatchVersionnedTag_E) as e:
        log.error("Could not tag create {} for asset {}".format(tag_name, asset))
        log.error(str(e))
        return False
    else:
        log.info("Successfully tagged {} {} to {} from {}".format(
            package, asset,
            tag_name, branch
        ))
        return True


def create_tag_annotated_from_branch(package, asset, branch, tag_name, message):
    if not is_vit_repo(): return False
    try:
        tag.create_tag_annotated_from_branch(
            os.getcwd(), package, asset,
            branch, tag_name, message
        )
    except (
            SSH_ConnectionError_E,
            Asset_NotFound_E,
            Package_NotFound_E,
            Branch_NotFound_E,
            RepoIsLock_E,
            Tag_AlreadyExists_E,
            Tag_NameMatchVersionnedTag_E) as e:
        log.error("Could not tag create {} for asset {}".format(tag_name, asset))
        log.error(str(e))
        return False
    else:
        log.info("Successfully tagged {} {} to {} from {}".format(
            package, asset,
            tag_name, branch
        ))
        return True


def create_tag_auto_from_branch(package, asset, branch, tag_name, message, increment):
    if not is_vit_repo(): return False
    try:
        tag.create_tag_auto_from_branch(
            os.getcwd(), package, asset,
            branch, message, increment
        )
    except (
            SSH_ConnectionError_E,
            Asset_NotFound_E,
            Package_NotFound_E,
            Branch_NotFound_E,
            RepoIsLock_E,
            Tag_AlreadyExists_E,
            Tag_NameMatchVersionnedTag_E) as e:
        log.error("Could not tag create {} for asset {}".format(tag_name, asset))
        log.error(str(e))
        return False
    else:
        log.info("Successfully tagged {} {} to {} from {}".format(
            package, asset,
            tag_name, branch
        ))
        return True




def list_templates():
    if not is_vit_repo(): return False
    try:
        template_data = asset_template.list_templates(os.getcwd())
    except SSH_ConnectionError_E as e:
        log.error("Could not list templates.")
        log.error(str(e))
        return False
    else:
        log.info("templates found on origin repository are:")
        for template_id, template_file in template_data.items():
            log.info("    - {} : {}".format(template_id, template_file))
        return True


def get_template(template_id):
    if not is_vit_repo(): return False
    try:
        template_path_local = asset_template.get_template(os.getcwd(), template_id)
    except (
            SSH_ConnectionError_E,
            Template_NotFound_E) as e:
        log.error("Could not get template file for {}".format(template_id))
        log.error(str(e))
        return False
    else:
        log.info("template {} successfully copied at: {}".format(
            template_id,
            template_path_local
        ))
        return True


def list_packages():
    if not is_vit_repo(): return False
    try:
        packages = package.list_packages(os.getcwd())
    except (SSH_ConnectionError_E,
            Package_NotFound_E) as e:
        log.error("Could not list templates.")
        log.error(str(e))
        return False
    else:
        log.info("packages found on origin repository are:")
        for p in packages:
            log.info("    - {}".format(p))
        return True


def list_assets(package):
    if not is_vit_repo(): return False
    try:
        assets = asset.list_assets(os.getcwd(), package)
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E) as e:
        log.error("Could not list assets for package {}.".format(package))
        log.error(str(e))
        return False
    else:
        log.info("Assets found on origin for package {} repository are:".format(
            package))
        for a in assets:
            log.info("    - {}".format(a))
        return True


def list_branches(package, asset):
    if not is_vit_repo(): return False
    try:
        branches = branch.list_branches(os.getcwd(), package, asset)
    except (
            SSH_ConnectionError_E,
            RepoIsLock_E,
            Package_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not list branches for assets {} {}.".format(package, asset))
        log.error(str(e))
        return False
    else:
        log.info("branches of {} {}".format(package, asset))
        for b in branches:
            log.info("    - {}".format(b))
        return True


def list_tags(package, asset):
    if not is_vit_repo(): return False
    try:
        tags = tag.list_tags(os.getcwd(), package, asset)
    except (
            SSH_ConnectionError_E,
            RepoIsLock_E,
            Package_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not list tags for assets {} {}.".format(package, asset))
        log.error(str(e))
        return False
    else:
        log.info("tags of {} {}".format(package, asset))
        for t in tags:
            log.info("    - {}".format(t))
        return True

def info(file_ref):
    if not is_vit_repo(): return False
    try:
        data = infos.get_info_from_ref_file(os.getcwd(), file_ref)
    except (
            RepoIsLock_E,
            SSH_ConnectionError_E,
            Path_FileNotFound_E,
            Asset_UntrackedFile_E) as e:
        log.error("Could not get info for file: ".format(file_ref))
        log.error(str(e))
        return False
    else:
        log.info(file_ref)
        log.info("\t{}: {} -> {}".format(
            data["asset_name"],
            data["checkout_type"],
            data["checkout_value"]
        ))
        log.info("\tpackage: {}".format(data["package_path"]))
        log.info ("\teditable: {}".format(data["editable"]))
        log.info("\tchanges: {}".format(data["changes"]))
        return True

def log_func(package, asset):
    if not is_vit_repo(): return False
    try:
        lines = log_module.get_log_lines(os.getcwd(), package, asset)
    except (
            SSH_ConnectionError_E,
            RepoIsLock_E,
            Package_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not {} {}.".format(package, asset))
        log.error(str(e))
        return False
    else:
        for line in lines:
            print(line)
        return True


def graph_func(package, asset):
    if not is_vit_repo(): return False
    try:
        lines = graph_module.main(os.getcwd(), package, asset)
    except (
            SSH_ConnectionError_E,
            Package_NotFound_E,
            Asset_NotFound_E) as e:
        log.error("Could not {} {}.".format(package, asset))
        log.error(str(e))
        return False
    else:
        for line in lines:
            print(line)
        return True


def clean_func():
    if not is_vit_repo(): return False
    local_path = os.getcwd()
    try:
        files_dict = clean.get_files_to_clean(local_path)
    except SSH_ConnectionError_E as e:
        log.error("could not get files to clean")
        log.error(str(e))
        return False
    else:
        def print_file(f, tab_number=1):
            log.info("\t"*tab_number+"- {}".format(f))

        if not files_dict["to_clean"]:
            log.info("no file to clean")
        else:
            log.info("following files will be cleaned:")
            for f in files_dict["to_clean"]:
                print_file(f)
        if files_dict["editable"] or files_dict["changes"]:
            log.info("following files won't be cleaned:")
            if files_dict["editable"]:
                log.info("\tfiles checkout as editable:")
                for f in files_dict["editable"]:
                    print_file(f, 2)
            if files_dict["changes"]:
                log.info("\tuncommit changes on files:")
                for f in files_dict["changes"]:
                    print_file(f, 2)
        clean.clean_files(local_path, *files_dict["to_clean"])
        return True


def clean_files(*files):
    if not is_vit_repo(): return False
    try:
        files_dict = clean.get_files_to_clean(os.getcwd())
    except SSH_ConnectionError_E as e:
        log.error("could not get files to clean")
        log.error(str(e))
        return False
    else:
        return True



