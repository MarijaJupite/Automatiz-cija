import requests
from bs4 import BeautifulSoup

class Recipe:
    def __init__(self, title, url):
        self.title = title
        self.url = url

class Recipe: 
    def __init__(self, title, url): #done
        self.title = title 
        self.url = url 
        self.ingredients = [] 
        
    def __str__(self): #done
        return f"{self.title} - {self.url}"
        
    def fetch_ingredients(self): #okk
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
            
    def _extract_ingredients(self, soup): #good
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

class Category:
    def __init__(self, name, url): #done
        self.name = name
        self.url = url

    def get_recipes(self): #good, done
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

    print("Izvēlieties kategoriju no saraksta:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.name}")

    choice = int(input("Ievadiet numuru no 1 līdz 12: "))
    if choice < 1 or choice > len(categories):
        print("Nepareiza izvēle!")
        return

    selected_category = categories[choice - 1]
    print(f"\nNotiek recepšu ielāde no kategorijas: {selected_category.name}...\n")

    recipes = selected_category.get_recipes()

    if recipes:
        print(f"\nKategorijā '{selected_category.name}' atrastas {len(recipes)} receptes:\n")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
    else:
        print("Neizdevās atrast receptes.")

if __name__ == "__main__":
    main()
