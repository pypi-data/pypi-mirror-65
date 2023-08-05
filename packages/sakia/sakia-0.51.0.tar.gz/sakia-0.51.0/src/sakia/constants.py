import os
import yaml

MAX_CONFIRMATIONS = 6

with open(
    os.path.join(os.path.dirname(__file__), "root_servers.yml"), "r", encoding="utf-8"
) as stream:
    ROOT_SERVERS = yaml.load(stream, Loader=yaml.FullLoader)

with open(
    os.path.join(os.path.dirname(__file__), "g1_license.html"), "r", encoding="utf-8"
) as stream:
    G1_LICENSE = stream.read()
