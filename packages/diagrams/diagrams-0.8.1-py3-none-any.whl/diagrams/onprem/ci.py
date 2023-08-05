# This module is automatically generated by autogen.sh. DO NOT EDIT.

from . import _OnPrem


class _Ci(_OnPrem):
    _type = "ci"
    _icon_dir = "resources/onprem/ci"


class Circleci(_Ci):
    _icon = "circleci.png"


class Jenkins(_Ci):
    _icon = "jenkins.png"


class Travisci(_Ci):
    _icon = "travisci.png"


# Aliases

CircleCI = Circleci
TravisCI = Travisci
