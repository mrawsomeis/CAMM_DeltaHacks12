from ingest import ingest_medical_info

def run_test_user_ingest():
    fake_user_id = "test_user_epilepsy_dementia_001"

    medical_info = (
        "I have epilepsy and early-onset dementia. "
        "I suffer from allergy to peanuts and macadamia nuts. "
        "I have anxiety, so I get super anxious when I hear loud voices "
        "and when people touch me and may freak out."
    )

    print("Ingesting test user medical info...")
    res = ingest_medical_info(
        user_id=fake_user_id,
        medical_text=medical_info
    )

    print("Ingestion response:")
    print(res)

if __name__ == "__main__":
    run_test_user_ingest()
