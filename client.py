import sys

from sstpyg.client import main


server_address = sys.argv[1]
role = sys.argv[2]

main.run(server_address, role)
