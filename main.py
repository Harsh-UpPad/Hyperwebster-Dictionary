from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Full printable ASCII sequence spectrum
BASE94_CHARS = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

def base94_index_to_text(index):
    """Converts a numerical remainder sequence value back into structural string symbols."""
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
    return render_template('index.html')

@app.route('/view')
def view_page():
    return render_template('page.html')

@app.route('/api/simple-search', methods=['GET'])
def search_hyperwebster():
    user_query = request.args.get('search', '') # Keep exact text layout unmodified
    user_index = request.args.get('searchIndex', '').strip()
    
    # Track the active string context block
    current_prefix = request.args.get('prefix', '').strip()

    # 1. CASE A: Initial phrase text lookup initiation
    if user_query:
        base_prefix = user_query
        start_offset = 0 # Begin with the clean keyword base match itself
        
    # 2. CASE B: Index offset adjustments via pagination controls
    elif user_index:
        base_prefix = current_prefix if current_prefix else ""
        try:
            start_offset = max(0, int(user_index))
        except ValueError:
            return jsonify({"message": "Invalid page numeric arguments provided."}), 400
    else:
        return jsonify({"message": "Please input contextual metrics."}), 400

    # 3. COMBINATORIAL PREFIX ITERATION GENERATION (50 rows)
    words_list = []
    
    # Row 0 matches the raw entry string perfectly if we are on the first page
    if start_offset == 0:
        words_list.append({
            "offset": 0,
            "word": base_prefix
        })
        limit = 49
    else:
        limit = 50

    for i in range(limit):
        current_offset = start_offset + (i + 1 if start_offset == 0 else i)
        
        # Calculate the sequential suffix modifications following the base term
        suffix_string = base94_index_to_text(current_offset)
        
        words_list.append({
            "offset": current_offset,
            "word": f"{base_prefix}{suffix_string}"
        })

    return jsonify({
        "prefix": base_prefix,
        "current_offset": start_offset,
        "words": words_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True)