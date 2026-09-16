from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE94_CHARS = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

def text_to_base94_index(text):
    index = 0
    for char in text:
        if char in BASE94_CHARS:
            char_value = BASE94_CHARS.index(char) + 1
            index = index * 94 + char_value
    return index

def base94_index_to_text(index):
    if index <= 0:
        return ""
    text = ""
    while index > 0:
        index -= 1
        text = BASE94_CHARS[index % 94] + text
        index //= 94
    return text

@app.route('/')
def home():
    # Renders the splash main entry form page
    return render_template('index.html')

@app.route('/view')
def view_page():
    # Renders the target pagination presentation layout template
    return render_template('page.html')

@app.route('/api/simple-search', methods=['GET'])
def search_hyperwebster():
    user_query = request.args.get('search', '').strip()
    user_index = request.args.get('searchIndex', '').strip()
    
    if user_query:
        target_idx = text_to_base94_index(user_query)
        # Center the user's searched item by displaying 25 rows before it
        start_idx = max(1, target_idx - 25) 
    elif user_index:
        try:
            start_idx = max(1, int(user_index))
        except ValueError:
            return jsonify({"message": "Please enter a valid round page count number."}), 400
    else:
        return jsonify({"message": "No valid search parameters were passed."}), 400

    # Build sequence listing blocks of exactly 50 entries
    words_list = []
    for i in range(50):
        current_idx = start_idx + i
        words_list.append({
            "index": f"{current_idx:,}",
            "word": base94_index_to_text(current_idx)
        })

    return jsonify({
        "start_index": start_idx,
        "words": words_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True)