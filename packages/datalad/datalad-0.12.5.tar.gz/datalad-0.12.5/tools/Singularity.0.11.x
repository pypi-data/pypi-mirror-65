#
# This container provides a full Python3-based installation of DataLad
# (http://datalad.org) using DataLad's latest development state at the
# time the container is built.
#
# Changelog
# ---------
# 0.11.5
#  - copied .fullmaster one to provide a version for 0.11.x branch build as well
# 0.12.0rc4-239-gba66d1c9f
#  - Update to get a fresh build of master
# 0.11.1
#  - Update to get a fresh build, also with fixed up git-annex
# 0.10.2
#  - Update after initial "burn-in" time for 0.10 series
# 0.10.rc5
#  - Pre-release
#
#######################################################################


Bootstrap:docker
From:neurodebian:latest

%post
    echo "Configuring the environment"
    apt-get -y update

    # setup the container sources themselves
    apt-get -y install eatmydata
    eatmydata apt-get -y install gnupg wget locales

    # we need a UTF locale for DataLad to work properly
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
    locale-gen

    # bare essentials to pull everything else in
    eatmydata apt-get -y install --no-install-recommends git git-annex-standalone python3-pip

    eatmydata apt-get -y install --no-install-recommends python3-setuptools python3-wheel less rsync git-remote-gcrypt aria2 libexempi3

    # just for scrapy
    eatmydata apt-get -y install --no-install-recommends python3-twisted

    # little dance because pip cannot handle this url plus [full] in one go
    wget https://github.com/datalad/datalad/archive/0.11.x.zip
    pip3 install --system 0.11.x.zip[full]
    rm -f 0.11.x.zip

    # clean up
    apt-get clean


%environments
    unset PYTHONPATH

%runscript
    datalad "$@"
