import streamlit as st

# Predefined list of foods
foods = [
    {"name": "Apple", "grams": 100, "carbs": 15},
    {"name": "Banana", "grams": 100, "carbs": 23},
    {"name": "Rice", "grams": 100, "carbs": 28},
    {"name": "Potato", "grams": 100, "carbs": 17},
    {"name": "Bread", "grams": 50, "carbs": 25},
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
def update_carbs(card_id, amount):
    for card in st.session_state.food_cards:
        if card["id"] == card_id:
            card["amount"] = amount
            card["carbs_per_amount"] = (
                amount * card["base_carbs"] / card["base_grams"]
            )
    update_total()

# Main page: Add food section
st.title("Carb Calculator")
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
            value=card["amount"],
            step=1,
            min_value=0,
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
