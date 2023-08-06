###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""

Wrappers for some DIRAC commands

@author Joel Closier <joel.closier@cern.ch>
@author Ben Couturier <ben.couturier@cern.ch>

"""
from __future__ import print_function

import argparse
import pipes
import os
from os.path import basename, isdir, join
import re
import sys

# TODO: Remove pro when /cvmfs/lhcb.cern.ch/lib/lhcb/LHCBDIRAC/ is removed
DIRAC_VERISON_PATTERN = re.compile(r"(prod|pro|v\d+r\d+(p\d+)?(-pre\d+)?)")
INSTALL_ROOTS = [
    "/cvmfs/lhcb.cern.ch/lhcbdirac/",
    "/cvmfs/lhcb.cern.ch/lib/lhcb/LHCBDIRAC/",
    "/cvmfs/lhcbdev.cern.ch/lhcbdirac/",
]
LHCB_ETC = "/cvmfs/lhcb.cern.ch/etc/grid-security"
ENV_VAR_WHITELIST = [
    # General unix
    r"DISPLAY",
    r"EDITOR",
    r"HOME",
    r"HOSTNAME",
    r"LANG",
    r"LC_.*",
    r"TMPDIR",
    r"TZ",
    r"USER",
    r"VISUAL",
    # HEP specific
    r"VOMS_.*",
    r"X509_.*",
    r"XRD_.*",
    # LHCb specific
    r"MYSITEROOT",
]
ENV_VAR_WHITELIST = re.compile(r"^(" + r"|".join(ENV_VAR_WHITELIST) + r")$")


def sort_versions(versions):
    parsedVersions = {}
    for version in versions:
        match = re.match(
            r"^v(?P<major>\d+)r(?P<minor>\d+)(?:p(?P<patch>\d+))?(?:-pre(?P<pre>\d+))?$",
            version,
        )
        if not match:
            continue
        v = match.groupdict()
        if v["pre"] is None:
            v["pre"] = sys.maxsize
        v = {k: 0 if v is None else int(v) for k, v in v.items()}
        parsedVersions[version] = (v["major"], v["minor"], v["patch"], v["pre"])

    return sorted(parsedVersions, key=parsedVersions.get, reverse=True)


def list_lhcbdirac_versions():
    versions = {}
    for install_root in INSTALL_ROOTS:
        if not isdir(install_root):
            continue
        for version in filter(DIRAC_VERISON_PATTERN.match, os.listdir(install_root)):
            # Skip versions that have already been found from a preferred location
            if version in versions:
                continue
            dirac_path = os.path.join(install_root, version)
            bashrc = os.path.join(install_root, "bashrc")
            # TODO: Remove when /cvmfs/lhcb.cern.ch/lib/lhcb/LHCBDIRAC/ is removed
            if version == "pro" and "prod" not in versions:
                versions["prod"] = dirac_path, bashrc
            else:
                versions[version] = dirac_path, bashrc
    return versions


LHCBDIRAC_VERSIONS = list_lhcbdirac_versions()


def call_dirac(command, version="prod"):
    """Replace the current process with a command in the LHCbDirac environment

    If the command is sucessfully executed this function will never return.
    """
    dirac_path, bashrc = LHCBDIRAC_VERSIONS[version]

    env = {k: v for k, v in os.environ.items() if ENV_VAR_WHITELIST.match(k)}
    env["DIRAC"] = dirac_path
    env["BASH_ENV"] = bashrc
    env["PS1"] = "(LHCbDIRAC " + version + ")$ "
    if isdir(LHCB_ETC):
        env["VOMS_USERCONF"] = env.get("VOMS_USERCONF", join(LHCB_ETC, "vomses"))
        env["X509_CERT_DIR"] = env.get("X509_CERT_DIR", join(LHCB_ETC, "certificates"))
        env["X509_VOMS_DIR"] = env.get("X509_VOMS_DIR", join(LHCB_ETC, "vomsdir"))
        env["X509_VOMSES"] = env.get("X509_VOMSES", join(LHCB_ETC, "vomses"))

    if basename(command[0]) == "bash":
        exec_command = "source $BASH_ENV; exec bash --norc --noprofile"
        for c in command[1:]:
            exec_command += " " + pipes.quote(c)
    elif basename(command[0]) in ["sh", "ksh", "csh", "tcsh", "zsh", "fish"]:
        raise NotImplementedError(
            "Unable to launch %s as only bash is supported by LHCbDIRAC"
            % basename(command[0]),
        )
    else:
        exec_command = " ".join(pipes.quote(x) for x in command)

    sys.stdout.flush()
    sys.stderr.flush()
    os.execvpe("bash", ["--norc", "--noprofile", "-c", exec_command], env)


def lb_dirac():
    """Invoke a commands in the correct environment"""
    parser = argparse.ArgumentParser(
        usage="lb-dirac [-h] [--list] [version] [command] ...",
        description="Run a command in the LHCbDIRAC environment",
    )
    parser.add_argument("--list", action="store_true", help="List available versions")
    # argparse doesn't support optional positional arguments so use metavar to
    # set the help text
    positional_help_text = (
        "version  optional, the version of LHCbDIRAC to use (default: prod)\n  "
        "command  optional, the command to run (default: bash)\n  "
        "...      optional, any additional arguments"
    )
    parser.add_argument(
        "command",
        metavar=positional_help_text,
        default=["bash"],
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    # Handle --list
    if args.list:
        print(*sort_versions(LHCBDIRAC_VERSIONS), sep="\n")
        sys.exit(0)

    # Parse the version/command positional arguments
    if args.command and args.command[0] in LHCBDIRAC_VERSIONS:
        command = args.command[1:]
        version = args.command[0]
    else:
        command = args.command
        version = "prod"
    command = command or ["bash"]

    # Try to replace the current process with the desired command
    try:
        call_dirac(command, version)
    except Exception as e:
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(1)


def lhcb_proxy_init():
    """Invoke lhcb-proxy-init in the correct environment"""
    # We just ignore the first argument...
    return call_dirac(["lhcb-proxy-init"] + sys.argv[1:])


def lhcb_proxy_info():
    """Invoke lhcb-proxy-init in the correct environment"""
    # We just ignore the first argument...
    return call_dirac(["dirac-proxy-info"] + sys.argv[1:])
