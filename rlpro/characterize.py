import argparse
import math
import serial
import time
from .rlpro import ReloadPro

parser = argparse.ArgumentParser(description="Evaluate Re:load Pro current setting accuracy")

parser.add_argument(
	'--current-step',
	action='store',
	dest='current_step',
	metavar='AMPS',
	default=0.1,
	type=float,
	help="Interval to step up current in")
parser.add_argument(
	'-current-max',
	action='store',
	dest='current_max',
	metavar='AMPS',
	default=3.0,
	type=float,
	help="Maximum current to test with")
parser.add_argument(
	'--delay',
	action='store',
	dest='delay',
	metavar='SECONDS',
	default=1.0,
	type=float,
	help="Interval between current steps")
parser.add_argument(
	'--baudrate',
	action='store',
	dest='baudrate',
	metavar='BAUD',
	default=115200,
	type=int,
	help="Baud rate to use when flashing using serial (default 115200)")
parser.add_argument(
	'--timeout',
	action='store',
	dest='timeout',
	metavar='SECS',
	default=5.0,
	type=float,
	help="Time to wait for a Bootloader response (default 5)")
parser.add_argument(
	'port',
	action='store',
	metavar='PORT',
	default=None,
	help="Serial port to use")


def main():
	args = parser.parse_args()
	s = serial.Serial(args.port, args.baudrate, timeout=args.timeout)
	rl = ReloadPro(s)

	i = 0.0
	err = 0.0
	count = 0
	while i < args.current_max:
		rl.set(i)
		time.sleep(args.delay)
		current, voltage = rl.read()
		err += math.sqrt(abs(i - current))
		count += 1
		print "%.2f, %.2f, %.2f, %.2f" % (i, current, i - current, i / current if current else float('nan'))
		i += args.current_step
	print "# RMS error: %.3f" % (math.pow(err / count, 2),)
	rl.set(0.0)

if __name__ == '__main__':
	main()
