from pyprobar import bar, probar
import time

def test_bar():
	N = 1234
	for i in range(N):
		time.sleep(0.01)
		bar(i, N, "update_random", symbol_2="o")


def test_probar():
	for idx, i in probar(range(1234), symbol_2="o"):
		time.sleep(0.01)


# test_bar()
test_probar()