import subprocess
from argparse import ArgumentParser
from ConfigParser import ConfigParser


def main():
    """Customize parameters based on the DuT.

    This script reads the devices configuration file given as parameter, and,
    based on the DuT, which is retrieved via the ADB, configures the environment
    variables that change amongst different terminals.
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", required=True, dest="configfile", action="store", help="configuration file")
    parser.add_argument("-o", "--out", required=False, dest="outfile", action="store",
                        help="configure the output file", default=".OWD_DEVICE_CONFIG")

    options = parser.parse_args()

    # Read configuration file
    configfile = options.configfile
    configparser = ConfigParser()
    configparser.readfp(open(configfile))

    outfile = options.outfile

    result = subprocess.check_output(["adb", "shell", "cat", "/system/build.prop"])
    device_idx = result.index("ro.product.name")
    device = result[device_idx:].split("\r")[0].split("=")[1]

    if not configparser.has_section(device):
        print "No specific section for device [{}] was found. Falling down to [generic] device options.".format(device)
        device = "generic"

    device_config = {}
    for item in configparser.items(device):
        device_config["OWD_DEVICE_" + item[0].upper()] = item[1]

    with open(outfile, "w") as f:
        f.write("# Device under Test: {}\n".format(device))
        for key in device_config.keys():
            f.write("export {}={}\n".format(key, device_config[key]))

if __name__ == '__main__':
    main()
