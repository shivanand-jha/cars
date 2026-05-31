#!/usr/bin/env python3
import os
import tempfile

import app


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    original_db = app.DB_PATH
    fd, path = tempfile.mkstemp(prefix="cardekho-test-", suffix=".db")
    os.close(fd)
    try:
        app.DB_PATH = path
        app.init_db()

        family = app.recommend(
            {
                "budget_lakh": 12,
                "family_size": 4,
                "usage": "mixed",
                "safety_priority": 5,
                "mileage_priority": 3,
                "feature_priority": 3,
                "body_preference": "any",
            }
        )
        assert_true(family[0]["id"] == "punch-accomplished", "safety-first family ranking changed")
        assert_true(family[0]["match_score"] > family[3]["match_score"], "family scores should be ranked")

        commuter = app.recommend(
            {
                "budget_lakh": 9,
                "family_size": 2,
                "usage": "city",
                "safety_priority": 3,
                "mileage_priority": 5,
                "feature_priority": 2,
                "body_preference": "Hatchback",
            }
        )
        assert_true(commuter[0]["id"] == "baleno-zeta", "budget commuter ranking changed")

        mpv = app.recommend(
            {
                "budget_lakh": 15,
                "family_size": 6,
                "usage": "highway",
                "safety_priority": 4,
                "mileage_priority": 2,
                "feature_priority": 4,
                "body_preference": "MPV",
            }
        )
        assert_true(mpv[0]["seats"] == 7, "large family ranking should prefer seven seats")

        saved = app.save_shortlist(
            {
                "buyer_name": "Smoke Test Buyer",
                "preferences": {"budget_lakh": 12},
                "car_ids": [family[0]["id"], family[1]["id"]],
                "notes": "Persistence check.",
            }
        )
        assert_true(saved["id"] == 1, "shortlist should be saved")
        shortlists = app.list_shortlists()
        assert_true(len(shortlists) == 1, "saved shortlist should be readable")
        assert_true(len(shortlists[0]["cars"]) == 2, "saved cars should hydrate from dataset")

        print("smoke tests passed")
    finally:
        app.DB_PATH = original_db
        if os.path.exists(path):
            os.unlink(path)


if __name__ == "__main__":
    main()
