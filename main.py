import requests
from bs4 import BeautifulSoup

class Recipe:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title} - {self.url}"

class Category:
    def __init__(self, name, url):
        self.name = name
        self.url = url
    def get_recipes(self):
        recipes = []
        current_url = self.url

def main():
    categories = [
        Category("Brokastis", "https://www.garsigalatvija.lv/receptes/brokastis/"),
        Category("Zupas", "https://www.garsigalatvija.lv/receptes/zupas/"),
        Category("Pamatēdieni", "https://www.garsigalatvija.lv/receptes/pamatedieni/"),
        Category("Piedevas", "https://www.garsigalatvija.lv/receptes/piedevas/"),
        Category("Salāti", "https://www.garsigalatvija.lv/receptes/salati/"),
        Category("Uzkodas", "https://www.garsigalatvija.lv/receptes/uzkodas/"),
        Category("Saldēdieni", "https://www.garsigalatvija.lv/receptes/saldedieni/"),
        Category("Kūkas-maizītes", "https://www.garsigalatvija.lv/receptes/kukas-maizites/"),
        Category("Maize", "https://www.garsigalatvija.lv/receptes/maize/"),
        Category("Cepumi", "https://www.garsigalatvija.lv/receptes/cepumi/"),
        Category("Dzērieni", "https://www.garsigalatvija.lv/receptes/dzerieni/"),
        Category("Ziemai", "https://www.garsigalatvija.lv/receptes/ziemai/")
    ]
    print("Izvēlies kategoriju no saraksta: ")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.name}")
    choice = int(input("Ievadiet numuru no 1 līdz 12: "))
    if choice < 1 or choice > len(categories):
        print("Nepareiza izvēle")
        return
    selected_category = categories[choice - 1]
    print(f"\nNotiek recepšu ielāde: {selected_category.name}...\n")
    recipes = selected_category.get_recipes()
  
if __name__ == "__main__":
    main()
