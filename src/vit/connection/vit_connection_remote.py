import os
from vit.connection.vit_connection import VitConnection


class VitConnectionRemote(VitConnection):

    def get_data_from_origin(
            self, src, dst,
            recursive=False,
            is_editable=False):
        return self._ssh_get_wrapper(src, dst, recursive=recursive)

    def put_data_to_origin(self, src, dst, is_src_abritrary_path=False):
        if is_src_abritrary_path:
            src = os.path.abspath(src)
        return self._ssh_put_wrapper(src, dst)

    def put_commit_to_origin(
            self, src, dst,
            keep_file,
            keep_editable,
            recursive=True):
        return self.put_data_to_origin(src, dst)
