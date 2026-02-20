from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# In-memory user behavior storage (for demo purposes)
user_data = {
    "dark_clicks": 0,
    "font_increase": 0,
    "section_clicks": {
        "Home": 0,
        "Profile": 0,
        "Settings": 0
    }
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Adaptive UI Demo</title>
    <style>
        body {
            font-family: Arial;
            transition: all 0.3s ease;
            padding: 20px;
        }

        .dark {
            background-color: #121212;
            color: white;
        }

        .large-font {
            font-size: 22px;
        }

        .section {
            padding: 10px;
            margin: 10px 0;
            border: 1px solid gray;
            cursor: pointer;
        }

        button {
            padding: 10px;
            margin: 5px;
        }
    </style>
</head>
<body id="body">

    <h2>AI-Based Adaptive User Interface</h2>

    <button onclick="toggleDark()">Toggle Dark Mode</button>
    <button onclick="increaseFont()">Increase Font Size</button>

    <div id="sections"></div>

<script>
    let darkMode = false;

    function toggleDark() {
        fetch('/dark', {method:'POST'});
        document.getElementById("body").classList.toggle("dark");
    }

    function increaseFont() {
        fetch('/font', {method:'POST'});
        document.getElementById("body").classList.add("large-font");
    }

    function clickSection(name) {
        fetch('/section', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({section:name})
        }).then(() => loadSections());
    }

    function loadSections() {
        fetch('/get_sections')
        .then(res => res.json())
        .then(data => {
            let container = document.getElementById("sections");
            container.innerHTML = "";
            data.forEach(sec => {
                container.innerHTML += 
                    `<div class="section" onclick="clickSection('${sec}')">${sec}</div>`;
            });
        });
    }

    loadSections();
</script>

</body>
</html>
"""

# Home Route
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


# Track Dark Mode Usage
@app.route("/dark", methods=["POST"])
def dark_mode():
    user_data["dark_clicks"] += 1
    return "", 204


# Track Font Increase
@app.route("/font", methods=["POST"])
def font_size():
    user_data["font_increase"] += 1
    return "", 204


# Track Section Clicks
@app.route("/section", methods=["POST"])
def section_click():
    data = request.get_json()
    section = data["section"]
    user_data["section_clicks"][section] += 1
    return "", 204


# AI Logic: Adaptive Section Ordering
@app.route("/get_sections")
def get_sections():
    sorted_sections = sorted(
        user_data["section_clicks"],
        key=user_data["section_clicks"].get,
        reverse=True
    )
    return jsonify(sorted_sections)


if __name__ == "__main__":
    app.run(debug=True)