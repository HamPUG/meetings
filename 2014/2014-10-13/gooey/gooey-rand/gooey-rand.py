import argparse
import random
from gooey import Gooey

@Gooey
def main():

	parser = argparse.ArgumentParser(description="Generate a sequence of random numbers")
	parser.add_argument("num", type=int, help="How many random numbers to return")
	parser.add_argument("min", type=int, help="Random numbers have to be at least this number")
	parser.add_argument("max", type=int, help="Random numbers have to be at most this number")

	parser.add_argument("-s", "--sum", action="store_true", help="Take the sum of these random numbers?")

	args = parser.parse_args()

	nums = [ random.randint(args.min,args.max) for x in range(0, args.num) ]

	if not args.sum:
		for num in nums:
			print num
	else:
		print sum(nums)

if __name__ == "__main__":
	main()