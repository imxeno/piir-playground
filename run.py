#!/usr/bin/env python3

import argparse
from fujitsu import Fujitsu_AR_REA2E
import sys

parser = argparse.ArgumentParser(description = "Emulator of a Fujtisu Air Conditioner Remote AR-REA2E",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--off", action="store_true", help="turn off")
parser.add_argument("-s", "--swing", action="store_true", help="enable swing")
parser.add_argument("-f", "--fan", default=0, type=int, help="fan speed - 0 = auto, 1-4")
parser.add_argument("-m", "--mode", default='auto', choices=['auto', 'cool', 'dry', 'fan', 'heat'], help="operation mode")
parser.add_argument("-t", "--temperature", default=18, type=int, help="temperature")

args = parser.parse_args(sys.argv[1:])

fujitsu = Fujitsu_AR_REA2E(2)
fujitsu.power = not args.off
fujitsu.swing = args.swing
fujitsu.fan_speed = args.fan
fujitsu.mode = args.mode
fujitsu.temperature = args.temperature
fujitsu.send()