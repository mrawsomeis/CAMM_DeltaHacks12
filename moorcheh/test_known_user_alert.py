from get_alerts import generate_alert_message

def run_known_user_test():
    fake_user_id = "test_user_epilepsy_dementia_001"
    address = "near a community location"

    print("=== KNOWN USER NOT_RESPONSIVE TEST ===")
    print("User ID:", fake_user_id)
    print("Address:", address)
    print("\nGenerated Response:\n")

    response = generate_alert_message(
        user_id=fake_user_id,
        address=address
    )

    if isinstance(response, dict):
        print(response.get("answer", response))
    else:
        print(response)

if __name__ == "__main__":
    run_known_user_test()
