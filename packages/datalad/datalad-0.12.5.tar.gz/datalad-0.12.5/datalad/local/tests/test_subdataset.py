# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Test subdataset command"""


import os
from os.path import (
    join as opj,
    relpath,
    pardir,
)

from datalad.distribution.dataset import Dataset
from datalad.api import (
    subdatasets,
    create,
)
from datalad.utils import (
    chpwd,
    Path,
)
from datalad.tests.utils import (
    eq_,
    with_testrepos,
    with_tempfile,
    assert_result_count,
    assert_false,
    assert_in,
    assert_not_in,
    assert_status,
    known_failure_windows,
)


# https://github.com/datalad/datalad/pull/3975/checks?check_run_id=369789014#step:8:275
@known_failure_windows
@with_testrepos('.*nested_submodule.*', flavors=['clone'])
def test_get_subdatasets(path):
    ds = Dataset(path)
    # one more subdataset with a name that could ruin config option parsing
    dots = str(Path('subdir') / '.lots.of.dots.')
    ds.create(dots)
    eq_(ds.subdatasets(recursive=True, fulfilled=False, result_xfm='relpaths'), [
        'sub dataset1'
    ])
    ds.get('sub dataset1')
    eq_(ds.subdatasets(recursive=True, fulfilled=False, result_xfm='relpaths'), [
        'sub dataset1/2',
        'sub dataset1/sub sub dataset1',
        'sub dataset1/subm 1',
    ])
    # obtain key subdataset, so all leaf subdatasets are discoverable
    ds.get(opj('sub dataset1', 'sub sub dataset1'))
    eq_(ds.subdatasets(result_xfm='relpaths'), ['sub dataset1', dots])
    eq_([(r['parentds'], r['path']) for r in ds.subdatasets()],
        [(path, opj(path, 'sub dataset1')),
         (path, opj(path, dots))])
    all_subs = [
        'sub dataset1',
        'sub dataset1/2',
        'sub dataset1/sub sub dataset1',
        'sub dataset1/sub sub dataset1/2',
        'sub dataset1/sub sub dataset1/subm 1',
        'sub dataset1/subm 1',
        dots,
    ]
    eq_(ds.subdatasets(recursive=True, result_xfm='relpaths'), all_subs)
    with chpwd(str(ds.pathobj)):
        # imitate cmdline invocation w/ no dataset argument
        eq_(subdatasets(dataset=None,
                        path=[],
                        recursive=True,
                        result_xfm='relpaths'),
            all_subs)

    # redo, but limit to specific paths
    eq_(
        ds.subdatasets(
            path=['sub dataset1/2', 'sub dataset1/sub sub dataset1'],
            recursive=True, result_xfm='relpaths'),
        [
            'sub dataset1/2',
            'sub dataset1/sub sub dataset1',
            'sub dataset1/sub sub dataset1/2',
            'sub dataset1/sub sub dataset1/subm 1',
        ]
    )
    eq_(
        ds.subdatasets(
            path=['sub dataset1'],
            recursive=True, result_xfm='relpaths'),
        [
            'sub dataset1',
            'sub dataset1/2',
            'sub dataset1/sub sub dataset1',
            'sub dataset1/sub sub dataset1/2',
            'sub dataset1/sub sub dataset1/subm 1',
            'sub dataset1/subm 1',
        ]
    )
    with chpwd(str(ds.pathobj / 'subdir')):
        # imitate cmdline invocation w/ no dataset argument
        # -> curdir limits the query, when no info is given
        eq_(subdatasets(dataset=None,
                        path=[],
                        recursive=True,
                        result_xfm='paths'),
            [str(ds.pathobj / dots)]
        )
        # but with a dataset explicitly given, even if just as a path,
        # curdir does no limit the query
        eq_(subdatasets(dataset=os.pardir,
                        path=None,
                        recursive=True,
                        result_xfm='relpaths'),
            ['sub dataset1',
             'sub dataset1/2',
             'sub dataset1/sub sub dataset1',
             'sub dataset1/sub sub dataset1/2',
             'sub dataset1/sub sub dataset1/subm 1',
             'sub dataset1/subm 1',
             dots]
        )
    # uses slow, flexible query
    eq_(ds.subdatasets(recursive=True, bottomup=True, result_xfm='relpaths'), [
        'sub dataset1/2',
        'sub dataset1/sub sub dataset1/2',
        'sub dataset1/sub sub dataset1/subm 1',
        'sub dataset1/sub sub dataset1',
        'sub dataset1/subm 1',
        'sub dataset1',
        dots,
    ])
    eq_(ds.subdatasets(recursive=True, fulfilled=True, result_xfm='relpaths'), [
        'sub dataset1',
        'sub dataset1/sub sub dataset1',
        dots,
    ])
    eq_([(relpath(r['parentds'], start=ds.path), relpath(r['path'], start=ds.path))
         for r in ds.subdatasets(recursive=True)], [
        (os.curdir, 'sub dataset1'),
        ('sub dataset1', 'sub dataset1/2'),
        ('sub dataset1', 'sub dataset1/sub sub dataset1'),
        ('sub dataset1/sub sub dataset1', 'sub dataset1/sub sub dataset1/2'),
        ('sub dataset1/sub sub dataset1', 'sub dataset1/sub sub dataset1/subm 1'),
        ('sub dataset1', 'sub dataset1/subm 1'),
        (os.curdir, dots),
    ])
    # uses slow, flexible query
    eq_(ds.subdatasets(recursive=True, recursion_limit=0),
        [])
    # uses slow, flexible query
    eq_(ds.subdatasets(recursive=True, recursion_limit=1, result_xfm='relpaths'),
        ['sub dataset1', dots])
    # uses slow, flexible query
    eq_(ds.subdatasets(recursive=True, recursion_limit=2, result_xfm='relpaths'),
        [
        'sub dataset1',
        'sub dataset1/2',
        'sub dataset1/sub sub dataset1',
        'sub dataset1/subm 1',
        dots,
    ])
    res = ds.subdatasets(recursive=True)
    assert_status('ok', res)
    for r in res:
        #for prop in ('gitmodule_url', 'state', 'revision', 'gitmodule_name'):
        for prop in ('gitmodule_url', 'revision', 'gitmodule_name'):
            assert_in(prop, r)
        # random property is unknown
        assert_not_in('mike', r)

    # now add info to all datasets
    res = ds.subdatasets(
        recursive=True,
        set_property=[('mike', 'slow'),
                      ('expansion', '<{refds_relname}>')])
    assert_status('ok', res)
    for r in res:
        eq_(r['gitmodule_mike'], 'slow')
        eq_(r['gitmodule_expansion'], relpath(r['path'], r['refds']).replace(os.sep, '-'))
    # plain query again to see if it got into the files
    res = ds.subdatasets(recursive=True)
    assert_status('ok', res)
    for r in res:
        eq_(r['gitmodule_mike'], 'slow')
        eq_(r['gitmodule_expansion'], relpath(r['path'], r['refds']).replace(os.sep, '-'))

    # and remove again
    res = ds.subdatasets(recursive=True, delete_property='mike')
    assert_status('ok', res)
    for r in res:
        for prop in ('gitmodule_mike'):
            assert_not_in(prop, r)
    # and again, because above yields on the fly edit
    res = ds.subdatasets(recursive=True)
    assert_status('ok', res)
    for r in res:
        for prop in ('gitmodule_mike'):
            assert_not_in(prop, r)

    #
    # test --contains
    #
    target_sub = 'sub dataset1/sub sub dataset1/subm 1'
    # give the closest direct subdataset
    eq_(ds.subdatasets(contains=opj(target_sub, 'something_inside'),
                       result_xfm='relpaths'),
        ['sub dataset1'])
    # should find the actual subdataset trail
    eq_(ds.subdatasets(recursive=True,
                       contains=opj(target_sub, 'something_inside'),
                       result_xfm='relpaths'),
        ['sub dataset1',
         'sub dataset1/sub sub dataset1',
         'sub dataset1/sub sub dataset1/subm 1'])
    # doesn't affect recursion limit
    eq_(ds.subdatasets(recursive=True, recursion_limit=2,
                       contains=opj(target_sub, 'something_inside'),
                       result_xfm='relpaths'),
        ['sub dataset1',
         'sub dataset1/sub sub dataset1'])
    # for a direct dataset path match, return the matching dataset
    eq_(ds.subdatasets(recursive=True,
                       contains=target_sub,
                       result_xfm='relpaths'),
        ['sub dataset1',
         'sub dataset1/sub sub dataset1',
         'sub dataset1/sub sub dataset1/subm 1'])
    # but it has to be a subdataset, otherwise no match
    # which is what get_containing_subdataset() used to do
    assert_status('impossible',
                  ds.subdatasets(contains=ds.path, on_failure='ignore'))

    # 'impossible' if contains is bullshit
    assert_status('impossible',
                  ds.subdatasets(recursive=True,
                                 contains='impossible_yes',
                                 on_failure='ignore'))

    assert_status('impossible',
                  ds.subdatasets(recursive=True,
                                 contains=opj(pardir, 'impossible_yes'),
                                 on_failure='ignore'))

    eq_(ds.subdatasets(
        recursive=True,
        contains=[target_sub, 'sub dataset1/2'],
        result_xfm='relpaths'), [
        'sub dataset1',
        'sub dataset1/2',
        'sub dataset1/sub sub dataset1',
        'sub dataset1/sub sub dataset1/subm 1',
    ])


@with_tempfile
def test_state(path):
    ds = Dataset.create(path)
    sub = ds.create('sub')
    res = ds.subdatasets()
    assert_result_count(res, 1, path=sub.path)
    # by default we are not reporting any state info
    assert_not_in('state', res[0])
    # uninstall the subdataset
    ds.uninstall('sub')
    # normale 'gone' is "absent"
    assert_false(sub.is_installed())
    assert_result_count(
        ds.subdatasets(), 1, path=sub.path, state='absent')
    # with directory totally gone also
    os.rmdir(sub.path)
    assert_result_count(
        ds.subdatasets(), 1, path=sub.path, state='absent')
    # putting dir back, no change
    os.makedirs(sub.path)
    assert_result_count(
        ds.subdatasets(), 1, path=sub.path, state='absent')


@with_tempfile
def test_get_subdatasets_types(path):
    ds = create(path)
    ds.create('1')
    ds.create('true')
    # no types casting should happen
    eq_(ds.subdatasets(result_xfm='relpaths'), ['1', 'true'])


@with_tempfile
def test_parent_on_unborn_branch(path):
    from datalad.support.gitrepo import GitRepo
    ds = Dataset(GitRepo(path, create=True).path)
    assert_false(ds.repo.get_hexsha())

    subrepo = GitRepo(opj(path, "sub"), create=True)
    subrepo.commit(msg="c", options=["--allow-empty"])

    ds.repo.add_submodule(path="sub")
    eq_(ds.subdatasets(result_xfm='relpaths'),
        ["sub"])
