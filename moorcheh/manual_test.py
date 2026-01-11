from moorcheh.get_alerts import generate_alert_message

def run_manual_test():
    user_id = None  # Simulate unknown person
    address = "near a community location"

    print("=== MANUAL NOT_RESPONSIVE TEST ===")
    print("User ID:", user_id)
    print("Address:", address)
    print("\nGenerated Response:\n")

    response = generate_alert_message(user_id=user_id, address=address)

    # Moorcheh answer API usually returns a dict
    if isinstance(response, dict):
        print(response.get("answer", response))
    else:
        print(response)

if __name__ == "__main__":
    run_manual_test()
