from bs4 import BeautifulSoup
import requests
import argparse
import cv2
import os.path

def getHTMLText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		print(len(r.text))
		return r.text
	except requests.RequestException as e:
		print(e)
		return ""

def downloadPokeDex(text):
	gen1 = []
	soup = BeautifulSoup(text, "html.parser")
	file = open("pokemon_list.html", "w")

	if soup.h2.text == 'Generation 1':
		for sibling in soup.h2.next_siblings:
			if sibling.name == "div":
				gen1 = str(sibling)
				break

	gen1Soup = BeautifulSoup(gen1, "html.parser")
	for span in gen1Soup.find_all('span', "infocard-data"):
		href = span.a.get('href')
		name = href[href.rfind('/')+1:]
		print(name)
		link = "https://img.pokemondb.net/sprites/red-blue/normal/%s.png" % (name)
		downloadPic(link, name)
		file.write(link+"\n")

	file.close()

def downloadPic(url, name):
	try:
		r = requests.get(url)
		r.raise_for_status()
		if os.path.isdir('E:\github\Pokedex\sprites'):
			pass
		else:
			os.mkdir('E:\github\Pokedex\sprites')
		f = open("sprites/%s.png" % (name.lower()), "wb")
		f.write(r.content)
		f.close()
	except requests.RequestException as e:
		print(e)


def main():
	url="https://pokemondb.net/sprites/"
	text = getHTMLText(url)
	downloadPokeDex(text)
	
if __name__ == '__main__':
	main()