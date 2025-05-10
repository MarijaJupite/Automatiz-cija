import requests
from bs4 import BeautifulSoup

class Recipe: 
    def __init__(self, title, url): #done
        self.title = title 
        self.url = url 
        self.ingredients = [] 
        
    def __str__(self): #done
        return f"{self.title} - {self.url}"

class Category:
    def __init__(self, name, url): #done
        self.name = name
        self.url = url

    def get_recipes(self): #done
        self.recipes = []
        current_url = self.url
        while current_url:
            try:
                response=response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                recipe_cards = soup.find_all("h2", class_="entry-title")
                for card in recipe_cards:
                    title_link = card.find("a")
                    if title_link:
                        self.recipes.append(Recipe(title_link.text.strip(), title_link["href"]))

                next_page_link = soup.find("a", string="« Older Entries")
                if next_page_link and "href" in next_page_link.attrs:
                    current_url = next_page_link["href"]
                else:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Neizdevās ielādēt lapu {current_url}. Kļūda: {e}")
                break
        return self.recipes

def display_recipes(recipes): #done
    if recipes:
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
        return True
    else:
        print("Šajā kategorijā nav recepšu.")
        return False
        
def handle_recipe_selection(recipes):
    selected_recipe = None  # inicializējam mainīgo, lai sekotu līdzi izvēlētajai receptei
    while recipes:
        try:
            choice = input("\nIzvēlieties receptes numuru, lai redzētu sastāvdaļas (vai 0 lai atgriezties atpakaļ uz kategorijām): ")
            if choice == "0":
                break
            elif choice.isdigit():
                recipe_choice = int(choice)
                if selected_recipe := get_selected_item(recipes, recipe_choice):
                    print(f"\nSastāvdaļas receptei '{selected_recipe.title}':\n")
                    ingredients = selected_recipe.fetch_ingredients()
                    if ingredients:
                        for ingredient in ingredients:
                            print(f"- {ingredient}")
                else:
                    print("Nepareiza izvēle.")
            else:
                print("Nepareiza ievade.")
        except ValueError:
            print("Lūdzu, ievadiet skaitli vai 0.")

def get_selected_item(items, choice): #done
    if isinstance(choice, int) and 1 <= choice <= len(items): 
        return items[choice - 1] 
    return None 
        
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
        Category("Ziemai", "https://www.garsigalatvija.lv/receptes/ziemai/"),
    ]

    while True:
        print("\nIzvēlieties kategoriju no saraksta: ")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
        print("-1. Iziet")

        try:
            choice = input("Ievadiet numuru: ")
            if choice == "-1":
                break
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(categories):
                    selected_category = categories[choice - 1]
                    print(f"\nNotiek recepšu ielāde: {selected_category.name}...\n")
                    recipes = selected_category.get_recipes()
                    display_recipes(recipes)
                    handle_recipe_selection(recipes)
                else:
                    print("Nepareiza izvēle.")
            else:
                print("Nepareiza ievade.")
        except ValueError:
            print("Lūdzu, ievadiet skaitli.")

if __name__ == "__main__":
    main()
