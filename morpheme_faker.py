from orderer import load_frequency
import sys
open(sys.argv[2], "w", encoding="UTF8").write("".join(f"{k} " * v for k, v in load_frequency(sys.argv[1]).items()))