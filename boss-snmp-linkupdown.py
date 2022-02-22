################################################################
# User Script
#
# Script        : Configure SNMP linkUp and LinkDown
# Revision      : 1.0
# Last updated  : Feb/18/2022
# Purpose       : Enables SNMP linkUp and LinkDown for uplink ports (MLT member ports) and disables it for edge ports.
#
################################################################
from device import api
import re

cli_results1 = emc_cli.send("enable")
cli_results1 = emc_cli.send("conf t")
cli_results1 = emc_cli.send("int fa all")
cli_results1 = emc_cli.send("no snmp-server notification-control linkDown ALL")
cli_results1 = emc_cli.send("no snmp-server notification-control linkUp ALL")
cli_results = emc_cli.send("show mlt | match Enabled")
cli_output = str(cli_results.getOutput())
cli_output_split = cli_output.splitlines()

for row in cli_output_split:
    match = re.search('(Uplink Core\s+)(\d[\d/]*[,-]\d[\d,/]*)', row)
    if match:
        mlt_ports = match.group(2)
        cli_results = emc_cli.send("snmp-server notification-control linkDown {0}".format(mlt_ports))
        cli_results = emc_cli.send("snmp-server notification-control linkUp {0}".format(mlt_ports))
        cli_results = emc_cli.send("exit")
        cli_results = emc_cli.send("save config")
