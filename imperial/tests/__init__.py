import os

if "IMPERIAl_TOKEN" in os.environ:
    del os.environ["IMPERIAl_TOKEN"]
#  tests inspired from imperial-node
#  two extra dependencies are needed
#  1. pytests
#  2. requests-mock
