# net_genconfig.__main__


import net_genconfig

import argparse
from copy import copy, deepcopy
import datetime
import jinja2
import os
import re
import sys
import yaml

from deepops import deepmerge, deepremoveitems

from net_genconfig import netaddr_filter



# --- functions ---



def raise_exception(e):
    """Simple function to raise the specified exception.  This is used
    for the parameter onerror for os.walk(), which otherwise ignores
    errors and skips over problematic directory entries.
    """

    raise e


def warn_helper(msg):
    """Helper function to print a warning inside a Jinja2 template.  The
    supplied message is printed to stderr but execution is not stopped.

    Keyword arguments:

    msg -- warning message to display
    """

    print("warning: " + msg, file=sys.stderr)


    # helper functions return a string to be included in the template; we don't
    # particularly have anything to include but have to return something, so we
    # return an empty string

    return ""


def raise_helper(msg):
    """Helper function to raise an exception inside a Jinja2 template.  The
    generic 'Exception' class is raised in Python.

    Keyword arguments:

    msg -- exception message to display when aborting
    """

    raise Exception(msg)


def assert_helper(condition, msg):
    """Helper function for assertions inside a Jinja2 template.  If the
    supplied condition is False, an exception is raised with the given
    error message.  The 'AssertionError' class is raised by Python.

    If the condition is True, an empty string is returned to avoid
    printing anything.

    Keyword arguments:

    condition -- the condition which must be satisfied to not raise the
    exception

    msg -- message to display in the event of the condition not being
    true
    """

    if not condition:
        raise AssertionError(msg)

    return ""


def re_match_helper(pattern, string):
    """Helper function for matching strings against regular expressions
    in a Jinja2 template.  The regular expression is compiled and
    matched against the supplied string (the Python regular expression
    library caches compiled strings for efficiency) and a boolean is
    returned, indicating whether the match succeeded or not.

    Keyword arguments:

    pattern -- the regular expression to match against

    string -- the string to match against
    """

    return bool(re.match(pattern, string))


def re_match_groups_helper(pattern, string):
    """Helper function for matching strings against regular expressions
    and extract groups of (separated by parentheses) in a Jinja2
    template.  The regular expression is compiled and matched against
    the supplied string (the Python regular expression library caches
    compiled strings for efficiency) and the groups in the expression
    are returned in the form of a list.

    Keyword arguments:

    pattern -- the regular expression to match against; the required
    groups to return should be specified using parentheses

    string -- the string to match and return the groups of
    """

    r = re.match(pattern, string)

    if r is None:
        raise ValueError("'%s' does not match regular expression '%s'" %
                             (string, pattern))

    return r.groups()



# --- command line arguments ---



# create the parser and add in the available command line options

parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a module
    # directory will use '__main__' by default - this name isn't necessarily
    # correct, but it looks better than that
    prog="net-genconfig",

    # we want the epilog help output to be printed as it and not reformatted or
    # line wrapped
    formatter_class=argparse.RawDescriptionHelpFormatter)


parser.add_argument(
    "-C", "--config",
    dest="config_dirname",
    default=(os.environ.get("NET_CONFIG_DIR")
                 if "NET_CONFIG_DIR" in os.environ else "."),
    help="base directory for roles, include and inventory")

parser.add_argument(
    "-r", "--roles",
    dest="roles_dirname",
    default="roles",
    help="directory containing role configuration templates")

parser.add_argument(
    "-n", "--include",
    dest="include_dirname",
    default="include",
    help="directory containing included templates / macro libraries")

parser.add_argument(
    "-i", "--inventory",
    dest="inventory_dirname",
    default="inventory",
    help="directory containing inventory of devices, networks, etc.")

parser.add_argument(
    "-o", "--output",
    dest="output_filename",
    help="write configuration to named file instead of stdout; '%%' can be "
         "used to substitute in the name of the device into the filename")

parser.add_argument(
    "-O", "--no-output",
    action="store_true",
    help="generate the configuration but do not output it - useful to test "
         "generation succeeds")

parser.add_argument(
    "-I", "--dump-inventory",
    action="store_true",
    help="dump complete read inventory in YAML to stdout and stop, without "
         "generating any configurations")

parser.add_argument(
    "-U", "--dump-device",
    action="store_true",
    help="dump resulting device definition in YAML to stdout, after merging "
         "profiles and stop, without generating any configurations")

parser.add_argument(
    "-d", "--define",
    action="append",
    nargs=2,
    default=[],
    help="define variable for use in the template",
    metavar=("VAR", "VALUE"))

parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="when generating configuration for multiple devices, don't print the "
         "name of each device, as it's generated")

parser.add_argument(
    "-D", "--debug",
    action="store_true",
    help="enable debug mode")

parser.add_argument(
    "devicename",
    nargs="*",
    help="name(s) of the device(s) to generate the configuration for")

parser.add_argument(
    "--version",
    action="version",
    version=("%(prog)s " + net_genconfig.__version__))


# parse the supplied command line against these options, storing the results

args = parser.parse_args()

roles_dirname = os.path.join(args.config_dirname, args.roles_dirname)
include_dirname = os.path.join(args.config_dirname, args.include_dirname)
inventory_dirname = os.path.join(args.config_dirname, args.inventory_dirname)
output_filename = args.output_filename
no_output = args.no_output
dump_inventory = args.dump_inventory
dump_device = args.dump_device
quiet = args.quiet
devicenames = args.devicename
debug = args.debug

vars = {}
for var, value in args.define:
    vars[var] = value


if debug:
    print("""\
debug: roles directory: %s
debug: include directory: %s
debug: inventory directory: %s
debug: output filename: %s
debug: device names: %s"""
              % (roles_dirname, include_dirname, inventory_dirname,
                 output_filename, devicenames),
          file=sys.stderr)


# check a couple of nonsensical configurations aren't being use related to
# multiple devices

if (len(devicenames) > 1) and (not (no_output or dump_device)):
    if not output_filename:
        print("error: multiple device names specified but outputting to "
                  "standard output - all configurations would be concatenated",
              file=sys.stderr)

        exit(1)


    elif output_filename.find("%") == -1:
        print("error: multiple device names specified but output filename "
                  "does not contain a '%' to substitute the device name - "
                  "output file would be overwritten",

              file=sys.stderr)

        exit(1)



# --- inventory ---



if debug:
    print("debug: starting to read inventory directory", file=sys.stderr)



# trawl the inventory directory tree, read and merge all the YAML files into
# one big dictionary

inventory = dict()

item_filepaths = dict()

try:
    # walk the directory tree, raising an exception if there are any
    # problems (oddly, os.walk() doesn't do this by default and skips
    # over any errors)

    for dirpath, dirnames, filenames in \
        os.walk(inventory_dirname, onerror=raise_exception):

        # remove any directories whose name begins with a dot (to skip over
        # things like '.git'; '.' and '..' are already removed) so they're not
        # traversed into on subsequent iterations

        for dirname in dirnames:
            if dirname.startswith("."):
                dirnames.remove(dirname)


        # work through all the files in this directory, in sorted order, and
        # process them

        for filename in sorted(filenames):
            # skip files beginning with a dot (assumed to be temporary,
            # control, or other unwanted files)

            if filename.startswith("."):
                continue


            # read this file as YAML and add it to the inventory

            filepath = os.path.join(dirpath, filename)

            if debug:
                print("debug: reading inventory file: %s" % filepath,
                      file=sys.stderr)

            try:
                inventory_file = yaml.safe_load(open(filepath))

            except ValueError as exception:
                print("error: failed parsing inventory file: %s: %s" %
                          (filepath, exception),
                      file=sys.stderr)

                exit(1)


            if not inventory_file:
                print("warning: skipping empty inventory file: %s" % filepath,
                      file=sys.stderr)

                continue


            for area in inventory_file:
                # create this part of the inventory, if it doesn't exist

                if area not in inventory:
                    inventory[area] = dict()
                    item_filepaths[area] = dict()


                else:
                    # if it did exist, raise an error if we already have a
                    # sub-item with the same name in that part

                    for item in inventory_file[area]:
                        if item in inventory[area]:
                            print("error: duplicate entry: %s.%s in "
                                  "inventory file: %s previously read in "
                                  "file: %s" %
                                      (area, item, filepath,
                                       item_filepaths[area][item]),
                                  file=sys.stderr)

                            exit(1)


                # add the items to the (possibly empty) part of the inventory

                inventory[area].update(inventory_file[area])


                # record where we found those items

                for item in inventory_file[area]:
                    item_filepaths[area][item] = filepath


                if debug:
                    print("debug: read: %s: %d"
                              % (area, len(inventory_file[area])),
                          file=sys.stderr)


except OSError as e:
    # this exception catches subclasses of OSError, including things
    # like 'file not found' or 'permission denied'

    print("error: problem reading inventory: %s" % e, file=sys.stderr)
    exit(1)


if debug:
    print("debug: finished reading inventory", file=sys.stderr)


if dump_inventory:
    print(yaml.dump(inventory, default_flow_style=False))
    exit(0)


if "devices" not in inventory:
    print("error: no devices found in inventory", file=sys.stderr)
    exit(1)



# build the Jinja2 environment

jinja_fsloader_dirs = [roles_dirname, include_dirname]

if debug:
    print("debug: creating environment with filesystem loader directories: "
          "%s" % jinja_fsloader_dirs)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(jinja_fsloader_dirs),
    extensions=[
        "jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
    trim_blocks=True)


# add in the special warn(), raise() and assert() functions, as well as
# some other functions we need, into the Jinja2 environment

env.globals["warn"] = warn_helper
env.globals["raise"] = raise_helper
env.globals["assert"] = assert_helper
env.globals["re_match"] = re_match_helper
env.globals["re_match_groups"] = re_match_groups_helper

env.globals["deepcopy"] = deepcopy

env.globals["deepmerge"] = deepmerge
env.globals["deepremoveitems"] = deepremoveitems


# add in the netaddr library functions as additional filters

for filter_name, filter_func in (
    netaddr_filter.FilterModule().filters().items()):

    env.filters[filter_name] = filter_func



def profiles_merge(source_description, device, included_profiles=set()):
    """This function recursively merges profiles into the supplied
    device (or device profile).
    
    If there is a "profiles" key in the device, it is read as a list of
    profiles to merge in, with items in the profiles later in the list
    taking precedence.  Each of these is merged recursively, allowing
    them to merge profiles themselves, and/or exclude items (see next).

    If there is a "profiles-exclude" key, it is taken as a structure
    giving items in the merged set of profiles (above) to be removed
    before the final merge.

    Once the merge and exclude stages are complete, the supplied device
    is merged into the merged/excluded profile data (with items in the
    supplied device taking precedence).

    Keyword arguments:

    source_description -- a textual description of this item (device or
    device profile), in the form "type: name" (e.g. "device: sw-office"
    or "device profile: cat3850"), that is used in debugging and error
    messages.

    device -- a device or device profile definition dictionary that is
    used as the definition to merge into, as well as read the
    "profiles" and "profiles-exclude" keys from (if present).

    included_profiles=set() -- the set of profiles which have been
    included so far - this is used to identify recursive profile usage
    and abort with a helpful error (rather than Python crashing with a
    recursion error).
    """

    # this function makes use of global variables defined outside it so
    # must appear here in the code


    # this dictionary will be used to build up the composite of all the merged
    # profiles and then exclude items, before merging the device into it at
    # the end

    profiles_merged = {}


    # if there are no profiles to be merged in to this device, return

    if "profiles" not in device:
        if debug:
            print("debug: %s complete - no profiles to merge"
                      % source_description,

                file=sys.stderr)

        return device


    # go through the list of profiles to merge

    for profile in device["profiles"]:
        # check this particular profile is defined and abort with an error
        # if not

        if profile not in inventory["device-profiles"]:
            print("error: %s unknown device profile: %s"
                        % (source_description, profile),

                  file=sys.stderr)

            exit(1)


        # get the profile with a recursive call (merging profiles and
        # excluding items, if the profile does that)
        #
        # this will effectively just return the profile itself, if the
        # profile doesn't do this
        
        if debug:
            print("debug: %s merging device profile: %s"
                      % (source_description, profile),

                  file=sys.stderr)


        # check if we've included this profile already, at some point higher 
        # in the hierarchy - if we have, abort with an error

        if profile in included_profiles:
            print("error: %s recursive inclusion of device profile: %s"
                      % (source_description, profile),

                  file=sys.stderr)

            exit(1)


        # copy the included profiles set and add this profile to it, before
        # doing the recursive profile merge
        #
        # doing this here will allow the same profile to be included twice, in
        # different branches of the hierarchy, which we want to allow, as they
        # will be in a different place in the order and may have different
        # exclusion definitions
        #
        # this will also allow the same profile to be included multiple times
        # by the same device or device profile, which doesn't make sense but
        # is not an error, so we can let it go

        included_profiles_this = copy(included_profiles)
        included_profiles_this.add(profile)

        sub_profile_merged = profiles_merge(
                                 "device profile: %s" % profile,
                                 inventory["device-profiles"][profile],
                                 included_profiles_this)


        # merge a deepcopy() of this profile into the composite profile
        # we're building of all the merged profiles
        #
        # we have to deepcopy() it to avoid changing parts of the merged
        # structure here and also if we exclude items later

        deepmerge(profiles_merged, deepcopy(sub_profile_merged))


    # if we're excluding anything from the imported profiles, we now
    # remove these from the merged profile we just assembled
    #
    # we have to copy the composite merged profile first so we don't
    # remove anything from the underlying profiles
    #
    # we do this inside the "if" statement checking for the "profiles"
    # key as there is no point excluding anything if we haven't included
    # any profiles first

    if "profiles-exclude" in device:
        if debug:
            print("debug: %s excluding items from merge"
                        % source_description,

                file=sys.stderr)

        deepremoveitems(profiles_merged, device["profiles-exclude"])


    # finally, we merge this device's (or device profile's) definition
    # dictionary over the top of the merged/excluded profiles; this will give
    # precedence to the ones in this device's definition

    if debug:
        print("debug: %s merging" % source_description, file=sys.stderr)

    deepmerge(profiles_merged, device)


    # return the device definition with the profiles merged/excluded

    if debug:
        print("debug: %s complete" % source_description, file=sys.stderr)

    return profiles_merged



def generate_config(devicename):
    """Generate the configuration for the specified device and write it
    to either standard output or a file, depending on the command line
    options specified.

    Returns true value if the configuration is generated successfully.  If
    there is a problem of some sort which is not serious enough to abort the
    script (such as one device cannot be found), the function will return a
    false value.  More serious problems will stop the entire script.
    """

    # this function makes use of global variables defined outside it so
    # must appear here in the code


    # get the definition dictionary for this device from the inventory; because
    # we're not going to modify it, we don't need to copy it
    #
    # we use this variable for some checks here, and to pass it to the starting
    # role template, so it avoids repeatedly fetching it
    #
    # if we're using a device profile, we will overwrite this after merging the
    # profiles in

    if devicename not in inventory["devices"]:
        print("warning: device not found in inventory: %s - skipping"
                  % devicename,

              file=sys.stderr)

        return False

    device_unmerged = inventory["devices"][devicename]

    if device_unmerged is None:
        print("warning: device definition empty: %s - skipping" % devicename,
              file=sys.stderr)

        return False


    # if we have profiles for this device, we need to use those as the base for
    # the device definition, so we need to merge them all together and into the
    # explicit device definition itself

    if "profiles" in device_unmerged:
        if "device-profiles" not in inventory:
            print("error: unknown profile: %s used in device: %s - no "
                  "profiles defined"
                      % (device_unmerged["profile"], devicename),

                  file=sys.stderr)

            exit(1)


        # call the merge function to recursively merge profiles and exclude
        # items

        if debug:
            print("debug: device: %s using profiles" % devicename,
                      file=sys.stderr)

        device = profiles_merge("device: %s" % devicename, device_unmerged)


    # we don't have amy profiles for this device, so we just use the device
    # data as is

    else:

        if debug:
            print("debug: device: %s not using profiles" % devicename,
                      file=sys.stderr)

        device = device_unmerged


    # if the dump device option is enabled, print a YAML version of the device
    # definition (now we've done merges, etc.) to stdout and return

    if dump_device:
        print(yaml.dump(device, default_flow_style=False))
        return True


    # we need a role and platform to read in the template

    if "role" not in device:
        print("error: missing role for device: %s" % devicename,
              file=sys.stderr)

        exit(1)

    if "platform" not in device:
        print("error: missing platform for device: %s" % devicename,
              file=sys.stderr)

        exit(1)


    role = device["role"]
    platform = device["platform"]



    # --- generate configuration ---



    if debug:
        print("debug: generating configuration for: %s role: %s platform: %s"
                  % (devicename, role, platform), file=sys.stderr)


    if not os.path.isdir(roles_dirname):
        print("error: role directory does not exist: %s" % roles_dirname,
              file=sys.stderr)

        exit(1)

    if not os.path.isdir(include_dirname):
        print("error: include directory does not exist: %s" % include_dirname,
              file=sys.stderr)

        exit(1)


    if not os.path.isdir(os.path.join(roles_dirname, platform)):
        print("error: platform not found: %s used for device: %s"
                  % (platform, devicename), file=sys.stderr)

        exit(1)


    # read the template file

    role_filename = os.path.join(platform, role) + ".j2"

    if debug:
        print("debug: using role file (relative to filesystem loader "
              "directory): %s" % role_filename, file=sys.stderr)

    try:
        template = env.get_template(role_filename)

    except jinja2.exceptions.TemplateNotFound:
        print("error: role not found: %s for platform: %s" % (role, platform),
              file=sys.stderr)

        exit(1)


    # render the template

    config = template.render(devicename=devicename, device=device,
                             inventory=inventory, **vars)


    # return, if output is disabled

    if no_output:
        if debug:
            print("debug: output disabled", file=sys.stderr)

        return True

    
    # write output to either standard output or a file, depending on the
    # options specified

    if output_filename:
        output_filename_expanded = (
            output_filename.replace("%", devicename))

        if debug:
            print("debug: writing to output file: %s"
                    % output_filename_expanded, file=sys.stderr)

        with open(output_filename_expanded, "w") as output_file:
            print(config, file=output_file)

    else:
        if debug:
            print("debug: writing to standard output", file=sys.stderr)

        print(config)


    return True



# go through all the devices specified, generate and write out their
# configurations

if not devicenames:
    print("warning: no device names specified", file=sys.stderr)


# this flag will change to False if any configuration fails to generate and
# is used to affect the return code from the script

complete_success = True


for devicename in devicenames:
    if (not quiet) and (len(devicenames) > 1):
        print(devicename)

    complete_success &= generate_config(devicename)


exit(0 if complete_success else 1)
