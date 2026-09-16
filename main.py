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

def parse_base36(s):
    """Converts a base-36 string (0-9, a-z) of any size to a standard Python integer."""
    return int(s, 36)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view_page():
    return render_template('page.html')

@app.route('/api/simple-search', methods=['GET'])
def search_hyperwebster():
    user_input = request.args.get('search', '').strip()
    mode = request.args.get('mode', 'str').lower()
    
    if not user_input:
        return jsonify({"message": "Please enter a value to search the void."}), 400

    try:
        # Determine the base index according to the selected mode
        if mode == 'str':
            # Text Mode: Convert custom string directly to Base-94 index
            target_idx = text_to_base94_index(user_input)
            start_idx = max(1, target_idx - 25) # Center the word
        elif mode == 'hex':
            # Hexadecimal Mode: Convert base-16 string directly to big-int
            start_idx = max(1, int(user_input, 16))
        elif mode == 'b36':
            # Base-36 Mode: Convert alphanumeric base-36 string directly to big-int
            start_idx = max(1, parse_base36(user_input))
        elif mode == 'idx':
            # Standard Base-10 Index Mode
            start_idx = max(1, int(user_input))
        else:
            return jsonify({"message": "Invalid search mode selected."}), 400
            
    except ValueError:
        return jsonify({"message": f"Invalid character found for selected mode '{mode}'."}), 400

    # Generate 50 sequential items from the calculated starting index
    words_list = []
    for i in range(50):
        current_idx = start_idx + i
        words_list.append({
            "index": str(current_idx), # Keep as string to prevent JS precision issues
            "word": base94_index_to_text(current_idx)
        })

    return jsonify({
        "start_index": str(start_idx),
        "mode": mode,
        "query": user_input,
        "words": words_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True)