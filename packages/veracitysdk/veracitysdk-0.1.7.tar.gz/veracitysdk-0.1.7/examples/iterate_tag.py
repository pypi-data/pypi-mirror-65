import os
import sys

from veracitysdk import Client, paginated, SimpleCache

def catch_err(err):
	if err:
		print(err.data)
		sys.exit()


cache = SimpleCache(".cache")

# Create client
client = Client(
	key = os.environ["VERACITY_KEY"],
	secret = os.environ["VERACITY_SECRET"],
	cache = cache
)

# Get tag
rating_tag, err = client.tags.get(":veracity_rating")
catch_err(err)

junk_domains = paginated(rating_tag.search_by_value, "j")
for domain in junk_domains:
	print(domain)
