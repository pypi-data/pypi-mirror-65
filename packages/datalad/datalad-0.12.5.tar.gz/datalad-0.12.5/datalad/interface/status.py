# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Plumbing command for reporting the status of a dataset"""


import logging
import re
from os.path import join as opj
from os.path import normpath

from git import GitConfigParser

from datalad.interface.base import Interface
from datalad.interface.utils import eval_results
from datalad.interface.utils import build_doc
from datalad.interface.results import get_status_dict
from datalad.support.constraints import EnsureBool
from datalad.support.constraints import EnsureNone
from datalad.support.param import Parameter
from datalad.interface.common_opts import recursion_flag
from datalad.interface.common_opts import recursion_limit
from datalad.distribution.dataset import require_dataset
from datalad.cmd import GitRunner
from datalad.support.gitrepo import GitRepo

from .dataset import Dataset
from .dataset import EnsureDataset
from .dataset import datasetmethod

__docformat__ = 'restructuredtext'

lgr = logging.getLogger('datalad.interface.status')


@build_doc
class Status(Interface):
    """Report the status of a dataset.
    """

    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc="""specify the dataset to report on.  If
            no dataset is given, an attempt is made to identify the dataset
            based on the input and/or the current working directory""",
            constraints=EnsureDataset() | EnsureNone()),
        recursive=recursion_flag,
        recursion_limit=recursion_limit,
    )

    # TODO: paths (optional)

            path=Parameter(
            args=("path",),
            metavar="PATH",
            doc="""path/name of the requested dataset component. The component
            must already be known to a dataset. To add new components to a
            dataset use the `add` command""",
            nargs="*",
            constraints=EnsureStr() | EnsureNone()),




    @staticmethod
    @datasetmethod(name='status')
    @eval_results
    def __call__(
            dataset=None,
            recursive=False,
            recursion_limit=None):

        dataset = require_dataset(
            dataset, check_installed=False, purpose='status reporting')




        ########### if actually recursive, ...:

        # return as quickly as possible
        if isinstance(recursion_limit, int) and (recursion_limit <= 0):
            return
        ###########


        #### from AnnexRepo
        if True == False:
            def _submodules_dirty_direct_mode(self,
                    untracked=True, deleted=True, modified=True, added=True,
                    type_changed=True, path=None):
                """Get modified submodules

                Workaround for http://git-annex.branchable.com/bugs/git_annex_status_fails_with_submodule_in_direct_mode/

                This is using git-annex-status with --ignore-submodules to not let
                git-status try to recurse into annex submodules without a working tree.
                Therefore we need to do the recursion on our own.

                Note, that added submodules will just be reported dirty. It's at very
                least difficult to distinguish whether a submodule in direct mode was
                just added or modified. ATM not worth the effort, I think.
                This is leads to a bit inconsistent reportings by AnnexRepo.status()
                whenever it needs to call this subroutine and there are added submodules.

                Intended to be used by AnnexRepo.status() internally.
                """

                # Note: We do a lazy recursion. The only thing we need to know is
                # whether or not a submodule is to be reported dirty. Once we already
                # know it is, there's no need to go any deeper in the hierarchy.
                # Apart from better performance, this also allows us to inspect each
                # submodule separately, and therefore be able to deal with mixed
                # hierarchies of git and annex submodules!

                modified_subs = []
                for sm in self.get_submodules():
                    sm_dirty = False

                    # First check for changes committed in the submodule, using
                    # git submodule summary -- path,
                    # since this can't be detected from within the submodule.
                    if self.submodules_is_modified(sm.name):
                        sm_dirty = True

                    # check state of annex submodules, that might be in direct mode
                    elif AnnexRepo.is_valid_repo(opj(self.path, sm.path),
                                                 allow_noninitialized=False):

                        sm_repo = AnnexRepo(opj(self.path, sm.path),
                                            create=False, init=False)

                        sm_status = sm_repo.status(untracked=untracked, deleted=deleted,
                                                   modified=modified, added=added,
                                                   type_changed=type_changed,
                                                   submodules=False, path=path)
                        if any([bool(sm_status[i]) for i in sm_status]):
                            sm_dirty = True

                    # check state of submodule, that is a plain git or not an
                    # initialized annex, which we can safely treat as a plain git, too.
                    elif GitRepo.is_valid_repo(opj(self.path, sm.path)):
                        sm_repo = GitRepo(opj(self.path, sm.path))

                        # TODO: Clarify issue: GitRepo.dirty() doesn't fit our parameters
                        if sm_repo.dirty(index=deleted or modified or added or type_changed,
                                         working_tree=deleted or modified or added or type_changed,
                                         untracked_files=untracked,
                                         submodules=False, path=path):
                            sm_dirty = True
                    else:
                        raise InvalidGitRepositoryError

                    if sm_dirty:
                        # the submodule itself is dirty
                        modified_subs.append(sm.path)
                    else:
                        # the submodule itself is clean, recurse:
                        modified_subs.extend(
                            sm_repo._submodules_dirty_direct_mode(
                                untracked=untracked, deleted=deleted,
                                modified=modified, added=added,
                                type_changed=type_changed, path=path
                            ))

                return modified_subs

        ####


        # TODO:
        # - Repo.status to return dict?
        # - check how to use get_status_dict and other helpers
        #