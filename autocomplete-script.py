import requests
import json
import sys
import pandas as pd

def main():
	suggestionUrl = 'http://autocomplete.belvilla.net/v2/search?language=en&query=ams'

	df = pd.read_csv(sys.argv[1])
	for keyword in df[list(df)[0]]:
		pass



if __name__ == "__main__":
	main()