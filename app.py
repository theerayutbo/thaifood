from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests # สำหรับเรียก Ollama API
import json # สำหรับจัดการ JSON response จาก Ollama

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_for_sessions'  # ตั้งค่า secret key สำหรับ session

# --- Ollama Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # หรือ 'llama3', 'mistral' หรือ model อื่นๆ ที่คุณมี

# --- Mock Data (ปรับปรุงให้รองรับ 2 ภาษา) ---
mock_menu_items_data = [
    {
        "id": 1,
        "name_en": "Chicken Stir-fry with Holy Basil", "name_th": "ผัดกะเพราไก่",
        "description_en": "Spicy and aromatic, a Thai classic.", "description_th": "รสชาติจัดจ้าน หอมใบกะเพรา",
        "price": 60, "image": "kaprao_kai.jpg", "category": "Stir-fry"
    },
    {
        "id": 2,
        "name_en": "Green Curry with Pork", "name_th": "แกงเขียวหวานหมู",
        "description_en": "Rich coconut milk, sweet and savory.", "description_th": "เข้มข้นกะทิ หวานมันกลมกล่อม",
        "price": 70, "image": "green_curry_pork.png", "category": "Curry"
    },
    {
        "id": 3,
        "name_en": "Tom Yum Goong (Spicy Shrimp Soup)", "name_th": "ต้มยำกุ้ง",
        "description_en": "Hot and sour soup with fresh shrimp.", "description_th": "ซุปเปอร์แซ่บ ซดคล่องคอ",
        "price": 80, "image": "tom_yum_goong.png", "category": "Soup"
    },
    {
        "id": 4,
        "name_en": "Pineapple Fried Rice", "name_th": "ข้าวผัดสับปะรด",
        "description_en": "Sweet and savory fried rice served in a pineapple.", "description_th": "ข้าวผัดหอมหวาน เสิร์ฟในลูกสับปะรด",
        "price": 90, "image": "pineapple_fried_rice.png", "category": "Rice"
    },
]

mock_grocery_items_data = [
    {"id": 101, "name_en": "Green Curry Paste (100g)", "name_th": "พริกแกงเขียวหวาน (100g)", "price": 35, "image": "green_curry_paste.jpg"},
    {"id": 102, "name_en": "Premium Fish Sauce (300ml)", "name_th": "น้ำปลาอย่างดี (300ml)", "price": 40, "image": "fish_sauce.png"},
]

# --- Language/Localization Strings ---
# (เก็บข้อความ UI สำหรับแต่ละภาษา)
ui_texts = {
    "en": {
        "shop_title": "Saneh Jaan AI - Modern Thai Cuisine",
        "nav_home": "Home",
        "nav_menu": "Menu",
        "nav_grocery": "Ingredients",
        "nav_about": "About Us",
        "nav_contact": "Contact",
        "nav_cart": "Cart",
        "ai_assistant_title": "AI Smart Assistant",
        "ai_greeting": "Hello! How can I help you today? Ask about our menu, opening hours, or get recipe ideas!",
        "ai_input_placeholder": "Type your question...",
        "ai_send_button": "Send",
        "ai_btn_ask_general": "Ask General Question",
        "ai_btn_get_recipe": "Get Recipe Idea",
        "section_recommended_menu": "Recommended Dishes",
        "section_all_menu": "Full Menu",
        "section_ingredients": "Quality Ingredients",
        "add_to_cart_button": "Add to Cart",
        "price_label": "Price",
        "currency_symbol": "THB", # หรือ £ ถ้าต้องการ
        "footer_text": "&copy; 2025 Saneh Jaan AI Manchester. All rights reserved.",
        "lang_switcher_th": "ภาษาไทย",
        "lang_switcher_en": "English",
        "ollama_error": "Sorry, there was an issue connecting to our AI assistant. Please try again later.",
        "ollama_thinking": "AI is thinking...",
        "recipe_input_placeholder": "e.g., 'chicken, basil' or 'a spicy soup'",
        "item_not_found_on_page": "AI: The item you're looking for isn't on this page. Try the 'Menu' page for all dishes.",
        "item_not_found_current_list": "AI: The item you searched for is not in the current list.",
        "cart_item_added_response": "AI: '{item_name}' is a great choice! Would you like me to suggest other complementary dishes?"
    },
    "th": {
        "shop_title": "เสน่ห์จันทน์ AI - อาหารไทยโมเดิร์น",
        "nav_home": "หน้าแรก",
        "nav_menu": "เมนูอาหาร",
        "nav_grocery": "วัตถุดิบ",
        "nav_about": "เกี่ยวกับเรา",
        "nav_contact": "ติดต่อ",
        "nav_cart": "ตะกร้า",
        "ai_assistant_title": "AI ผู้ช่วยอัจฉริยะ",
        "ai_greeting": "สวัสดีค่ะ! มีอะไรให้ AI ช่วยไหมคะ? ลองถามเกี่ยวกับเมนู เวลาเปิดร้าน หรือขอไอเดียสูตรอาหารได้เลยค่ะ",
        "ai_input_placeholder": "พิมพ์คำถามของคุณ...",
        "ai_send_button": "ส่ง",
        "ai_btn_ask_general": "สอบถามทั่วไป",
        "ai_btn_get_recipe": "ขอไอเดียสูตรอาหาร",
        "section_recommended_menu": "เมนูแนะนำจากร้าน",
        "section_all_menu": "เมนูอาหารทั้งหมด",
        "section_ingredients": "วัตถุดิบคุณภาพ",
        "add_to_cart_button": "เพิ่มลงตะกร้า",
        "price_label": "ราคา",
        "currency_symbol": "บาท",
        "footer_text": "&copy; 2025 เสน่ห์จันทน์ AI Manchester. สงวนลิขสิทธิ์",
        "lang_switcher_th": "ภาษาไทย",
        "lang_switcher_en": "English",
        "ollama_error": "ขออภัยค่ะ มีปัญหาในการเชื่อมต่อกับ AI ของเรา กรุณาลองใหม่อีกครั้ง",
        "ollama_thinking": "AI กำลังประมวลผล...",
        "recipe_input_placeholder": "เช่น 'ไก่, กะเพรา' หรือ 'ซุปเผ็ดๆ'",
        "item_not_found_on_page": "AI: ไม่พบเมนูที่คุณต้องการในหน้านี้ค่ะ ลองไปที่หน้า 'เมนูอาหาร' นะคะ",
        "item_not_found_current_list": "AI: ไม่พบเมนูที่คุณค้นหาในรายการปัจจุบันค่ะ",
        "cart_item_added_response": "AI: '{item_name}' เป็นตัวเลือกที่ดีค่ะ! สนใจให้ AI แนะนำเมนูอื่นที่เข้ากันไหมคะ?"
    }
}

def get_current_lang():
    return session.get('language', 'en') # Default to English

def get_ui_text(key):
    lang = get_current_lang()
    return ui_texts.get(lang, ui_texts['en']).get(key, f"[{key}]") # Fallback to English then key

def get_localized_items(items_data):
    lang = get_current_lang()
    localized = []
    for item in items_data:
        loc_item = item.copy()
        loc_item['name'] = item.get(f'name_{lang}', item.get('name_en', 'N/A'))
        loc_item['description'] = item.get(f'description_{lang}', item.get('description_en', ''))
        localized.append(loc_item)
    return localized


@app.before_request
def before_request():
    if 'language' not in session:
        session['language'] = 'en' # Default language

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ui_texts:
        session['language'] = lang
    return redirect(request.referrer or url_for('home'))

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html',
                           ui=lambda k: get_ui_text(k),
                           current_lang=get_current_lang(),
                           items=get_localized_items(mock_menu_items_data),
                           section_title_key="section_recommended_menu")

@app.route('/menu')
def menu_page():
    return render_template('index.html',
                           ui=lambda k: get_ui_text(k),
                           current_lang=get_current_lang(),
                           items=get_localized_items(mock_menu_items_data),
                           section_title_key="section_all_menu")

@app.route('/grocery')
def grocery_page():
    return render_template('index.html',
                           ui=lambda k: get_ui_text(k),
                           current_lang=get_current_lang(),
                           items=get_localized_items(mock_grocery_items_data),
                           section_title_key="section_ingredients")


# --- Ollama AI API Endpoint ---
@app.route('/api/ollama/ask', methods=['POST'])
def ollama_ask():
    user_query = request.json.get('query', '').strip()
    mode = request.json.get('mode', 'general_query') # 'general_query' or 'recipe_suggestion'
    current_language = get_current_lang()
    language_instruction = "Please respond in English." if current_language == 'en' else "กรุณาตอบเป็นภาษาไทย"

    if not user_query:
        return jsonify({"answer": get_ui_text('ai_input_placeholder') if current_language == 'en' else ui_texts['th']['ai_input_placeholder']})

    # Prepare context about menu items for the LLM
    menu_context_list = [f"- {item['name_en']} ({item['name_th']})" for item in mock_menu_items_data]
    menu_context = "\nOur current menu includes:\n" + "\n".join(menu_context_list)


    # Construct prompt based on mode
    if mode == "recipe_suggestion":
        prompt = f"""You are a helpful AI assistant for a Thai restaurant called "Saneh Jaan Manchester".
A customer is looking for a Thai recipe idea based on: "{user_query}".
Please provide a concise and appealing Thai recipe suggestion. If they mention specific ingredients, try to incorporate them.
If they mention a general dish type (e.g., "spicy soup", "something with chicken"), suggest a suitable Thai dish.
Keep the response focused on the recipe idea.
{menu_context}
{language_instruction}
User query: "{user_query}"
Recipe idea: """
    else: # general_query
        prompt = f"""You are a very friendly and helpful AI assistant for a Thai restaurant named "Saneh Jaan Manchester" located in Manchester, UK.
Our restaurant offers authentic Thai cuisine.
{menu_context}
We are open from 10:00 AM to 10:00 PM.
A customer has the following query: "{user_query}".
Please answer the customer's query informatively and politely.
If the query is about a specific menu item that is on our menu, acknowledge it.
{language_instruction}
User query: "{user_query}"
Answer: """

    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False # Set to True for streaming, but requires different handling
        }
        ollama_response = requests.post(OLLAMA_API_URL, json=payload, timeout=60) # Increased timeout
        ollama_response.raise_for_status() # Raise an exception for HTTP errors

        response_data = ollama_response.json()
        ai_answer = response_data.get("response", "No response from AI.").strip()

        # Basic item identification (can be improved with LLM function calling or regex)
        # This is a simplified version, an LLM could be asked to return a structured JSON for this
        found_item_id = None
        item_name_for_highlight = ""
        for item in mock_menu_items_data:
            if item['name_en'].lower() in ai_answer.lower() or item['name_th'] in ai_answer:
                found_item_id = item['id']
                item_name_for_highlight = item[f'name_{current_language}']
                break
        
        if found_item_id:
            return jsonify({
                "answer": ai_answer,
                "action": "highlight_item",
                "item_id": found_item_id,
                "item_name": item_name_for_highlight
            })
        else:
            return jsonify({"answer": ai_answer})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return jsonify({"answer": get_ui_text('ollama_error')}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"answer": f"An unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)