
def create_store(self):
    # Note, that the following does create the base-path dir as well:
    self.io.mkdir(self.store_base_path / 'error_logs')

    self.io.write_file(self.store_base_path / 'ria-layout-version',
                       self.dataset_tree_version + '\n')

def verify_store(self):
    """Check whether the store exists and reports a layout version we
    know

    The layout of the store is recorded in base_path/ria-layout-version.
    If the version found on the remote end isn't supported and `force-write`
    isn't configured, sets the remote to read-only operation.
    """

    dataset_tree_version_file = \
        self.store_base_path / 'ria-layout-version'

    # check dataset tree version
    try:
        self.remote_dataset_tree_version = \
            self._get_version_config(dataset_tree_version_file)
        if self.remote_dataset_tree_version not in self.known_versions_dst:
            # Note: In later versions, condition might change in order to
            # deal with older versions.
            raise UnknownLayoutVersion

    except (RemoteError, FileNotFoundError):
        # Exception class depends on whether self.io is local or SSH.
        # assume file doesn't exist
        # TODO: Is there a possibility RemoteError has a different reason
        #       and should be handled differently?
        #       Don't think so ATM. -> Reconsider with new execution layer.

        if not self.io.exists(dataset_tree_version_file.parent):
            # unify exception
            raise FileNotFoundError

        else:
            # Directory is there, but no version file. We don't know what
            # that is. Treat the same way as if there was an unknown version
            # on record.
            raise NoLayoutVersion

# def store_layout(version, base_path, dsid):
#     """Return dataset-related path in a RIA store
#
#     Parameters
#     ----------
#     version : int
#       Layout version of the store.
#     base_path : Path
#       Base path of the store.
#     dsid : str
#       Dataset ID
#
#     Returns
#     -------
#     Path, Path, Path
#       The location of the bare dataset repository in the store,
#       the directory with archive files for the dataset, and the
#       annex object directory are return in that order.
#     """
#     if version == 1:
#         dsgit_dir = base_path / dsid[:3] / dsid[3:]
#         archive_dir = dsgit_dir / 'archives'
#         dsobj_dir = dsgit_dir / 'annex' / 'objects'
#         return dsgit_dir, archive_dir, dsobj_dir
#     else:
#         raise ValueError("Unknown layout version: {}".format(version))
#
#
#
# def create_store(io):
#     pass
#
#
# # store base
# # error_logs
# # version file + parse flags
# # dataset location
#
# # version file + parse flags
# # objects dir
# # archives dir
# # key location
#
#
#
# class RIAStore(object):
#
#     def __init__(self, version, io, base_path):
#
#         self.version = version
#         self.io = io
#         self.base_path = base_path
#
#     def verify(self):
#         pass
#
#     def create(self):
#         pass
#
#     def get_locations(self, dsid):
#         pass
