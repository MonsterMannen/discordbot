#imports
import urllib2

# functions
def getHTML(url):
	response = urllib2.urlopen(url)
	return response.read()

def getTweets(html):
	tag = '<div class="js-tweet-text-container">'
	tweetPoses = findAll(html, tag)
	tweets = []
	start = 0;
	end = 0;
	for pos in tweetPoses:
		# offset to skip first ta
		start = html.find(">", (pos + len(tag)))
		end = html.find("<", start)
		tweets.append(html[start+1:end-2])
	return tweets

def findAll(str_text, str_find):
	foundPos = []
	pos = 0
	while(True):
		# searching starting at pos
		pos = str_text.find(str_find, pos)
		if pos == -1: break
		foundPos.append(pos)
		pos += len(str_find)
	return foundPos

def url2tweets(url):
	return getTweets(getHTML(url))


# main
if __name__ == '__main__':
	print "Scanning twitter \n"
	twitterURL = "https://twitter.com/PokemonGBG"
	tweets = url2tweets(twitterURL)
	for tweet in tweets:
		print tweet

	