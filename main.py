# Darja Kučerenko 241RDB126 1.grupa
# Marija Jupite 241RDB067 5.grupa
import requests
from bs4 import BeautifulSoup
import json

FAVORITES_FILE = "favorites.json"

class Recipe: 
    def __init__(self, title, url):
        self.title = title 
        self.url = url 
        self.ingredients = [] 
        
    def __str__(self):
        return f"{self.title} - {self.url}"
    
    def fetch_ingredients(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            self.ingredients = self._extract_ingredients(soup)
            if not self.ingredients:
                print(f"Neizdevās atrast sastāvdaļu sarakstu lapā {self.url}.")
            return self.ingredients
        except requests.exceptions.RequestException as e:
            print(f"Neizdevās ielādēt recepti no {self.url}. Kļūda: {e}")
            return None
        
    def _extract_ingredients(self, soup):
        selectors = [
            (".et_pb_row_inner.et_pb_row_inner_2", ['ul', 'ol'], None), 
            (".et_pb_row_inner.et_pb_row_inner_1", ['ul', 'ol'], "span"), 
            (".et_pb_column_inner_2 .et_pb_text_inner ul", ['li'], None),
        ]
        for selector, list_tags, span_tag in selectors:
            container = soup.select_one(selector)
            if container:
                ingredients = []
                for list_container in container.find_all(list_tags):
                    for item in list_container.find_all("li"):
                        if span_tag:
                            span = item.find(span_tag)
                            ingredients.append(span.text.strip() if span else item.text.strip())
                        else:
                            ingredients.append(item.text.strip())
                if ingredients:
                    return ingredients

        keywords = ["Sastāvdaļas", "Ingredienti", "Kas nepieciešams"]
        for keyword in keywords:
            keyword_element = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div'] and keyword in tag.text) 
            if keyword_element:
                ingredients_list_container = keyword_element.find_next(['ul', 'ol'])
                if ingredients_list_container:
                    return [item.text.strip() for item in ingredients_list_container.find_all("li")]
        return []

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Kļūda, atverot izlases failu. Tas var būt bojāts.")
        return []


def save_favorites(favorites):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, indent=4, ensure_ascii=False)


class Category:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.recipes = []

    def get_recipes(self):
        self.recipes = []
        current_url = self.url
        while current_url:
            try:
                response = requests.get(current_url)
                response.raise_for_status()
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

def display_recipes(recipes):
    if recipes:
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
        return True
    else:
        print("Šajā kategorijā nav recepšu.")
        return False

def handle_recipe_selection(recipes, favorites):
  selected_recipe = None  
  while recipes:
        try:
            choice = input("\nIzvēlieties receptes numuru, lai redzētu sastāvdaļas (vai 'f' - pievienot izlasei, 0 - atpakaļ uz kategorijām): ")
            if choice == "0":
                break
            elif choice == "f":
                if selected_recipe:
                    if any(fav['url'] == selected_recipe.url for fav in favorites):
                        print(f"Recepte '{selected_recipe.title}' jau ir izlasē.")
                    else:
                        favorites.append({"title": selected_recipe.title, "url": selected_recipe.url})
                        save_favorites(favorites)
                        print(f"Recepte '{selected_recipe.title}' pievienota izlasei.")
                else:
                    print("Vispirms izvēlieties receptes numuru.")
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
            print("Lūdzu, ievadiet skaitli, 'f' vai 0.")



def display_favorites(favorites):
    if favorites:
        for i, favorite in enumerate(favorites, 1):
            print(f"{i}. {favorite['title']} - {favorite['url']}")
        return True
    else:
        print("Jūsu izlases saraksts ir tukšs.")
        return False


def handle_favorite_selection(favorites):
    while favorites:
        display_favorites(favorites)  

        try:
            choice = input("\nIzvēlieties receptes numuru, lai redzētu sastāvdaļas (vai 'd' - dzēst no izlases, 0 - atpakaļ uz kategorijām): ")
            
            if choice == "0":
                break
                
            elif choice == "d":
                remove_choice = input("Ievadiet receptes numuru, ko dzēst no izlases: ")
                if remove_choice.isdigit():
                    remove_index = int(remove_choice) - 1
                    if 0 <= remove_index < len(favorites):
                        removed_favorite = favorites.pop(remove_index)
                        save_favorites(favorites)
                        print(f"Recepte '{removed_favorite['title']}' dzēsta no izlases.")
                    else:
                        print("Nepareiza izvēle.")
                else:
                    print("Nepareiza ievade.")
                    
            elif choice.isdigit():
                fav_choice = int(choice)
                if 1 <= fav_choice <= len(favorites):
                    selected_favorite = favorites[fav_choice - 1]
                    recipe = Recipe(selected_favorite['title'], selected_favorite['url'])
                    print(f"\nSastāvdaļas receptei '{recipe.title}':\n")
                    ingredients = recipe.fetch_ingredients()
                    if ingredients:
                        for ingredient in ingredients:
                            print(f"- {ingredient}")
                else:
                    print("Nepareiza izvēle.")
            else:
                print("Nepareiza ievade.")
        except ValueError:
            print("Lūdzu, ievadiet skaitli, 'd' vai 0.")

    if not favorites:
        print("Jūsu izlases saraksts ir tukšs.")


def get_selected_item(items, choice):
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
    
    favorites = load_favorites()

    while True:
        print("\nIzvēlieties kategoriju no saraksta: ")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
        print(f"0. Skatīt izlasi ({len(favorites)})")
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
                    handle_recipe_selection(recipes, favorites)
                elif choice == 0:
                    print("\nJūsu izlases receptes:\n")
                    handle_favorite_selection(favorites)
                else:
                    print("Nepareiza izvēle.")
            else:
                print("Nepareiza ievade.")
        except ValueError:
            print("Lūdzu, ievadiet skaitli.")

if __name__ == "__main__":
    main()
