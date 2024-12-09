import streamlit as st

# Predefined list of foods
foods = [
    {"name": "Süt", "grams": 200, "carbs": 10},
    {"name": "Yoğurt", "grams": 200, "carbs": 10},
    {"name": "Ayran", "grams": 300, "carbs": 10},
    {"name": "Kefir", "grams": 200, "carbs": 10},
    {"name": "Ekmek", "grams": 25, "carbs": 15},
    {"name": "Bisküvi (Tuzlu)", "grams": 25, "carbs": 15},
    {"name": "Çorbalar", "grams": 25, "carbs": 15},
    {"name": "Elma", "grams": 100, "carbs": 15},
    {"name": "Kayısı", "grams": 100, "carbs": 15},
    {"name": "Kuru Kayısı", "grams": 20, "carbs": 15},
    {"name": "Kuru Erik", "grams": 20, "carbs": 15},
    {"name": "Kiraz", "grams": 75, "carbs": 15},
    {"name": "Vişne", "grams": 80, "carbs": 15},
    {"name": "Greyfurt", "grams": 125, "carbs": 15},
    {"name": "Portakal", "grams": 100, "carbs": 15},
    {"name": "Mandalina", "grams": 100, "carbs": 15},
    {"name": "Limon", "grams": 100, "carbs": 15},
    {"name": "Yeni Dünya", "grams": 125, "carbs": 15},
    {"name": "Kırmızı Erik", "grams": 100, "carbs": 15},
    {"name": "Yeşil Erik", "grams": 100, "carbs": 15},
    {"name": "Armut", "grams": 100, "carbs": 15},
    {"name": "Şeftali", "grams": 100, "carbs": 15},
    {"name": "Çilek", "grams": 175, "carbs": 15},
    {"name": "Ayva", "grams": 80, "carbs": 15},
    {"name": "Nar", "grams": 80, "carbs": 15},
    {"name": "Kivi", "grams": 100, "carbs": 15},
    {"name": "Kavun", "grams": 200, "carbs": 15},
    {"name": "Karpuz", "grams": 200, "carbs": 15},
    {"name": "Hurma", "grams": 20, "carbs": 15},
    {"name": "Dut", "grams": 100, "carbs": 15},
    {"name": "Kuru İncir", "grams": 20, "carbs": 15},
    {"name": "Kuru Üzüm", "grams": 20, "carbs": 15},
    {"name": "Muz", "grams": 50, "carbs": 15},
    {"name": "Taze İncir", "grams": 80, "carbs": 15},
    {"name": "Üzüm", "grams": 80, "carbs": 15},
]

# Store added foods in session state
if "food_cards" not in st.session_state:
    st.session_state.food_cards = []

if "total_carbs" not in st.session_state:
    st.session_state.total_carbs = 0

# Function to update total carbs
def update_total():
    st.session_state.total_carbs = sum(
        card["carbs_per_amount"]
        for card in st.session_state.food_cards
    )

# Add food card
def add_food_card(food_name):
    food = next((f for f in foods if f["name"] == food_name), None)
    if food:
        st.session_state.food_cards.append(
            {
                "id": len(st.session_state.food_cards),
                "name": food["name"],
                "base_grams": food["grams"],
                "base_carbs": food["carbs"],
                "amount": food["grams"],
                "carbs_per_amount": food["carbs"],
            }
        )
        update_total()

# Delete food card
def delete_food_card(card_id):
    st.session_state.food_cards = [
        card for card in st.session_state.food_cards if card["id"] != card_id
    ]
    update_total()
    st.rerun()  # Force re-render to ensure card is removed immediately

# Update carbs for a specific card
def update_carbs(card_id, new_amount):
    for card in st.session_state.food_cards:
        if card["id"] == card_id:
            # Update only if the value is actually different
            if card["amount"] != new_amount:
                card["amount"] = new_amount
                card["carbs_per_amount"] = (
                    new_amount * card["base_carbs"] / card["base_grams"]
                )
    update_total()

# Main page: Add food section
st.title("💜 Princess calculator 💜")
st.header("Add Food")
col1, col2 = st.columns([3, 1])
with col1:
    selected_food = st.selectbox(
        "Select food to add:", [food["name"] for food in foods]
    )
with col2:
    if st.button("Add Food"):
        add_food_card(selected_food)

# Main page: Display food cards
st.subheader("Your selected foods:")

for card in st.session_state.food_cards:
    st.write("---")
    col1, col2, col3 = st.columns([4, 3, 1])
    with col1:
        st.text(card["name"])
    with col2:
        new_amount = st.number_input(
            "Amount (grams):",
            value=float(card["amount"]),
            step=0.1,
            min_value=0.0,
            key=f"amount_{card['id']}",
        )
        update_carbs(card["id"], new_amount)
    with col3:
        if st.button("Delete", key=f"delete_{card['id']}"):
            delete_food_card(card["id"])

    st.write(
        f"Carbs for this item: **{card['carbs_per_amount']:.2f}g**"
    )

# Display total carbs
st.write("---")
st.subheader(f"Total Carbs: **{st.session_state.total_carbs:.2f}g**")
