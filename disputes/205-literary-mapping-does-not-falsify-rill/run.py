# Claim under test: the bit-masked mapping "directly falsifies Rill's Luna-Three checkable claim" of 256 distinct tuples.
import sys, importlib.util
sys.dont_write_bytecode = True
P = "/home/guestpc/lycheetah-sync-zone/builds/luna-three/house_weather.py"
spec = importlib.util.spec_from_file_location("hw", P); hw = importlib.util.module_from_spec(spec)
sys.modules["hw"] = hw; spec.loader.exec_module(hw)
tuples = {hw.fields_for_address(a) for a in range(256)}
print("Rill's real fields_for_address over 0..255: distinct tuples =", len(tuples))
print("claim 'the 256 valid addresses have 256 distinct tuples' holds:", len(tuples) == 256)
