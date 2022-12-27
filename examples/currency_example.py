from bloxflip import Currency, Authorization
import random
import time

auth = ""
if not Authorization.validate(auth):
	print("Invalid authorization")
	exit()

old = None

while True:
	affiliate = Currency.affiliate(auth)
	balance = Currency.balance(auth)
	if not affiliate == old:
		print(f"R$ {affiliate} available to claim.")
		print(f"R$ {balance} Robux in your balance")
		if affiliate >= 100:
			print("Claiming affiliate")
			Currency.claimAffiliate(auth, round(affiliate, 2))
			print("Withdrawing robux")
			Currency.withdraw(auth, round(affiliate, 2))
		else:
			print("Not enough affiliate to claim")
		old = Currency.affiliate(auth)