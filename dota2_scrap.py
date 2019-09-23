import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictWriter, DictReader

base_url = 'https://dota2.ru/'
def scrap_heroes():
	url_heroes = 'heroes/'
	request = requests.get(f"{base_url}{url_heroes}")
	soup = BeautifulSoup(request.text, "html.parser")
	heroes = soup.select("[data-title]")
	all_heroes = []
	for hero in heroes:
		name = hero['data-tooltipe']
		href = hero['href']
		all_heroes.append({
			"Name": name,
			"hero_url": href
			})
	return all_heroes
	# print(hero['data-tooltipe'])
def start_game(all_heroes):
	hero = choice(all_heroes)
	hero_url = hero['hero_url']
	request = requests.get(f"{base_url}{hero_url}")
	soup = BeautifulSoup(request.text, "html.parser")
	bio = soup.find(class_="bio").find("p").get_text()
	hidden_bio_name = bio.replace(hero['Name'], "...")
	print(hidden_bio_name)
	guess=''
	guess_number = 3
	while guess.lower() != hero['Name'].lower() and guess_number > 0:
		guess = input("Это описание какого героя?\n Введи здесь: ")
		guess_number -= 1
		if guess.lower() == hero['Name'].lower():
			print("Поздравляю, ты прав!")
			break
		if guess_number == 2:
			skills = []
			for skill in soup.select(".single"):
				skill_name = skill.find("h3").get_text()
				skill_desc = skill.find(class_="description").get_text()
				skills.append({skill_name:skill_desc})
			skill_hint = choice(skills)
			skill_name = list(skill_hint.keys())[0]
			skill_desc = list(skill_hint.values())[0]
			print(f"Герой имеет умение: {skill_name}")
		elif guess_number == 1:
			print(f"Описание этого умения:\n{skill_desc}")
		else:
			print(f"Попытки закончились, это был {hero['Name']}")

	again = ''
	while again.lower() not in ('yes', 'y', 'no',' n'):
		again = input("Would ypu like play again? (y/n): ").lower()
		if again in ('yes', 'y'):
			print("ok, play again.")
			return start_game(all_heroes)
		else:
			print("ok, bye.")
			break

# heroes = scrap_heroes()
def write_heroes(heroes):
	with open("d2heroes.csv","w") as file:
		headers = ["Name","hero_url"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for hero in heroes:
			csv_writer.writerow(hero)

def read_heroes(filename):
	with open(filename) as file:
		csv_reader = DictReader(file)
		return list(csv_reader)
		

#Scrapping hearoes:		

# heroes = scrap_heroes()
# heroes_file = write_heroes(heroes)

heroes = read_heroes("d2heroes.csv")
start_game(heroes)