from datetime import datetime
import os
import sys

from veracitysdk import Client, MetadataType, SimpleCache

def catch_err(err):
	if err:
		print(err.data)
		sys.exit()


# Create client
client = Client(
	key = os.environ["VERACITY_KEY"],
	secret = os.environ["VERACITY_SECRET"],
)

# Perform a search
results, err = client.articles.fulltext_search("disinformation -france")
catch_err(err)
print(results)


# Perform a search with domains and date-range
results, err = client.articles.fulltext_search(
	"disinformation",
	domains = [45, 99, 102],
	start_date = datetime(2020, 1, 1),
	end_date = datetime(2020, 2, 1),
)
