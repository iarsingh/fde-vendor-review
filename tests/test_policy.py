from vendor.eval import run
from vendor.ingest import EVALS_PATH, load_packets
from vendor.policy import review_packet


def test_eval_file_passes():
    assert run(EVALS_PATH) == 0


def test_bank_change_is_never_auto_approved():
    review = review_packet(load_packets()["V-2"])
    assert review.decision == "manual_review"
    assert "approved" not in review.render().lower()


def test_incomplete_packet_is_blocked_before_the_bank_review():
    review = review_packet(load_packets()["V-6"])
    assert review.decision == "blocked_incomplete"


def test_sanctions_flag_has_no_override():
    review = review_packet(load_packets()["V-5"])
    assert review.decision == "blocked_sanctions"
