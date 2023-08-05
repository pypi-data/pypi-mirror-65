net-genconfig
=============

This package generates configurations for network devices based on three
sources of information:

* roles -- these Jinja2 templates form the basis of an output
  configuration file and exist for each platform and device role (e.g.
  IOS as distribution router; IOS as core router, NX-OS as core router,
  NX-OS as row switch)

* include -- Jinja2 includes (some to be included 'as is' [.j2] and
  some with macros that can be called [.j2m]); these are included by
  the role templates and by each other

* inventory -- this is a big database of device details (including the role for
  a particular device) and associated information, such as VLANs, subnets,
  interfaces, etc.
