from flask import Flask, render_template, request

app = Flask(__name__)

def parse_preferences(raw_preferences):
    """
    Parse les préférences entrées via le formulaire (au format texte).
    """
    preferences = {}
    for line in raw_preferences.split("\n"):
        if line.strip():
            name, prefs = line.split(":")
            parsed_prefs = []
            for item in prefs.split(","):
                if item.startswith("{") and item.endswith("}"):
                    parsed_prefs.append(set(item[1:-1].split(";")))
                else:
                    parsed_prefs.append({item})
            preferences[name.strip()] = parsed_prefs
    return preferences


def rank_in_preferences(preferences, person, candidate):
    for rank, group in enumerate(preferences[person]):
        if candidate in group:
            return rank
    return float("inf")


def paluch_algorithm(men_preferences, women_preferences):
    matches = {}
    free_men = list(men_preferences.keys())

    while free_men:
        man = free_men.pop(0)
        for group in men_preferences[man]:
            for woman in group:
                if woman not in matches:
                    matches[woman] = man
                    break
                else:
                    current_man = matches[woman]
                    if rank_in_preferences(women_preferences, woman, man) < rank_in_preferences(women_preferences, woman, current_man):
                        matches[woman] = man
                        free_men.append(current_man)
                        break
            else:
                continue
            break
    return matches


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Récupérer les données du formulaire
        num_men = int(request.form["num_men"])
        num_women = int(request.form["num_women"])
        men_preferences_raw = request.form["men_preferences"]
        women_preferences_raw = request.form["women_preferences"]

        # Parser les préférences
        men_preferences = parse_preferences(men_preferences_raw)
        women_preferences = parse_preferences(women_preferences_raw)

        # Exécuter l'algorithme
        results = paluch_algorithm(men_preferences, women_preferences)

        return render_template("results.html", results=results)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
