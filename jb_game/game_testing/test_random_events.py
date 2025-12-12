import pytest
from unittest.mock import patch
from jb_game.game_logic.jb_dev_random_events import RandomEvents
from jb_game.game_logic.jb_dev_stats import JBStats


@pytest.fixture
def events():
    return RandomEvents()


@pytest.fixture
def stats():
    return JBStats(available_money=10000, coding_experience=0, pcr_hatred=0)


# ==========================================
# 1. OVERTIME EVENT
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_overtime_take_money(mock_randint, mock_decision, _, events, stats):
    # Note the '_' above. It replaces 'mock_input'
    mock_decision.return_value = '1'
    mock_randint.return_value = 5000
    events.overtime_offer(stats)
    assert stats.available_money == 15000


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_overtime_study_python(mock_randint, mock_decision, _, events, stats):
    mock_decision.return_value = '2'
    mock_randint.return_value = 20
    events.overtime_offer(stats)
    assert stats.coding_experience == 20


# ==========================================
# 2. BIRTHDAY EVENT
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_birthday_pay(mock_decision, _, events, stats):
    mock_decision.return_value = '1'
    events.birthday_gift(stats)
    assert stats.available_money == 9000
    assert stats.pcr_hatred == 5


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_birthday_refuse(mock_decision, _, events, stats):
    mock_decision.return_value = '2'
    events.birthday_gift(stats)
    assert stats.pcr_hatred == 15


# ==========================================
# 3. CIVILIAN SMALL TALK
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_small_talk_vent_success(mock_randint, mock_decision, _, events, stats):
    """Scenario: Vent out (1) and succeed (Roll <= 80)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 50
    stats.pcr_hatred = 50

    events.civilian_small_talk(stats)
    assert stats.pcr_hatred == 25


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_small_talk_vent_fail(mock_randint, mock_decision, _, events, stats):
    """Scenario: Vent out (1) and fail (Roll > 80)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 90

    events.civilian_small_talk(stats)
    assert stats.pcr_hatred == 25
    assert stats.available_money == 7500


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_small_talk_keep_inside(mock_decision, _, events, stats):
    mock_decision.return_value = '2'
    events.civilian_small_talk(stats)
    assert stats.pcr_hatred == 10


# ==========================================
# 4. CORPSE IN CARE HOME
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_corpse_refuse_success(mock_randint, mock_decision, _, events, stats):
    mock_decision.return_value = '1'
    mock_randint.return_value = 20
    events.corpse_in_care_home(stats)
    # Based on code logic: Prints "0 PCR HATRED" but does not subtract existing.
    # If stats started at 0, adding +10 for entering room means result is 10.
    assert stats.pcr_hatred == 10


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_corpse_drag_disaster(mock_randint, mock_decision, _, events, stats):
    mock_decision.return_value = '2'
    mock_randint.return_value = 3
    events.corpse_in_care_home(stats)
    # Enter room (+10) + Disaster (+30) = 40
    assert stats.pcr_hatred == 40


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_corpse_refuse_fail_then_ok(mock_randint, mock_decision, _, events, stats):
    mock_decision.return_value = '1'
    # side_effect: First roll=80 (Refuse Fail), Second roll=90 (Drag Safe)
    mock_randint.side_effect = [80, 90]

    events.corpse_in_care_home(stats)
    # Enter (+10) + Fail Refuse (+5) + Drag Safe (+20) = 35
    assert stats.pcr_hatred == 35


# ==========================================
# 5. ADMIN MISTAKE
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_admin_mistake_leave(mock_decision, _, events, stats):
    mock_decision.return_value = '1'
    stats.pcr_hatred = 20
    events.admin_mistake_after_shift(stats)
    assert stats.available_money == 7500
    assert stats.pcr_hatred == 10


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_admin_mistake_stay(mock_decision, _, events, stats):
    mock_decision.return_value = '2'
    events.admin_mistake_after_shift(stats)
    assert stats.pcr_hatred == 20


# ==========================================
# 6. ISRAELI DEVELOPER
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_dev_low_skill(mock_decision, _, events, stats):
    stats.coding_experience = 10
    mock_decision.return_value = '2'
    events.israeli_developer(stats)
    assert stats.coding_experience == 20


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_dev_high_skill_success(mock_decision, _, events, stats):
    stats.coding_experience = 60
    mock_decision.return_value = '1'
    events.israeli_developer(stats)
    assert stats.coding_experience == 90


# ==========================================
# 7. NIGHTMARE WOLF
# ==========================================

@patch('builtins.input')
def test_event_nightmare_wolf(_, events, stats):
    # Only patched 'input', so only one '_' needed
    events.nightmare_wolf(stats)
    assert stats.pcr_hatred == 10


# ==========================================
# 8. CITIZEN OF CZECHOSLOVAKIA
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_citizen_ignore(mock_decision, _, events, stats):
    """Scenario: Ignore the sovereign citizen (Choice 1)."""
    mock_decision.return_value = '1'
    events.citizen_of_czechoslovakia(stats)
    assert stats.pcr_hatred == 15  # +15 Humiliation


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_citizen_arrest(mock_decision, _, events, stats):
    """Scenario: Arrest him (Choice 2)."""
    mock_decision.return_value = '2'
    events.citizen_of_czechoslovakia(stats)
    assert stats.pcr_hatred == 5  # +5 (Silenced him)
    assert stats.available_money == 9000  # 10k - 1000 Fine


# ==========================================
# 9. PRINTER INCIDENT
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_printer_fix_success(mock_randint, mock_decision, _, events, stats):
    """Scenario: Fix printer (Choice 1) -> Success (Roll <= Skill*2)."""
    stats.coding_experience = 30  # 30 * 2 = 60% chance
    mock_decision.return_value = '1'
    mock_randint.return_value = 50  # Success (< 60)

    events.printer_incident(stats)
    assert stats.coding_experience == 40  # 30 + 10


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_printer_fix_fail(mock_randint, mock_decision, _, events, stats):
    """Scenario: Fix printer (Choice 1) -> Failure."""
    stats.coding_experience = 10  # 20% chance
    mock_decision.return_value = '1'
    mock_randint.return_value = 80  # Fail

    events.printer_incident(stats)
    assert stats.available_money == 8000  # 10k - 2k
    assert stats.pcr_hatred == 15


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_printer_ignore(mock_decision, _, events, stats):
    """Scenario: Ignore it (Choice 2)."""
    mock_decision.return_value = '2'
    events.printer_incident(stats)
    assert stats.pcr_hatred == 5


# ==========================================
# 10. ETHICS SEMINAR
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_ethics_sleep_fail(mock_randint, mock_decision, _, events, stats):
    """Scenario: Sleep (Choice 1) -> Caught (Roll <= 50)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 40

    events.ethics_seminar(stats)
    assert stats.available_money == 9500  # 10k - 500
    assert stats.pcr_hatred == 10


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_ethics_sleep_success(mock_randint, mock_decision, _, events, stats):
    """Scenario: Sleep (Choice 1) -> Success (Roll > 50)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 60

    events.ethics_seminar(stats)
    assert stats.pcr_hatred == -15


# ==========================================
# 11. FORGOTTEN USB
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_usb_risk_fail(mock_randint, mock_decision, _, events, stats):
    """Scenario: Plug in (Choice 1) -> Virus (Roll <= 50)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 10
    stats.coding_experience = 50

    events.forgotten_usb(stats)
    assert stats.coding_experience == 25  # 50 - 25


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
@patch('jb_game.game_logic.jb_dev_random_events.randint')
def test_event_usb_risk_success(mock_randint, mock_decision, _, events, stats):
    """Scenario: Plug in (Choice 1) -> Crypto (Roll > 50)."""
    mock_decision.return_value = '1'
    mock_randint.return_value = 90

    events.forgotten_usb(stats)
    assert stats.available_money == 35000  # 10k + 25k


# ==========================================
# 12. TURKISH FRAUD
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_turkish_success(mock_decision, _, events, stats):
    """Scenario: Track scammer (Choice 1) with High Skill (>= 75)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 80

    events.turkish_fraud(stats)
    assert stats.daily_btc_income == 5000
    assert stats.pcr_hatred == -20


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_turkish_fail(mock_decision, _, events, stats):
    """Scenario: Track scammer (Choice 1) with Low Skill (< 75)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 50

    events.turkish_fraud(stats)
    assert stats.daily_btc_income == 0
    assert stats.pcr_hatred == 10


# ==========================================
# 13. DISPATCH BLUE SCREEN
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_dispatch_fix_success(mock_decision, _, events, stats):
    """Scenario: Fix BSOD (Choice 1) with High Skill (>= 30)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 35

    events.dispatch_blue_screen(stats)
    assert stats.pcr_hatred == -10
    assert stats.coding_experience == 40  # 35 + 5


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_dispatch_fix_fail(mock_decision, _, events, stats):
    """Scenario: Fix BSOD (Choice 1) with Low Skill (< 30)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 10

    events.dispatch_blue_screen(stats)
    assert stats.pcr_hatred == 10


# ==========================================
# 14. TECH BRO SPEEDING
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_tech_bro_ticket(mock_decision, _, events, stats):
    """Scenario: Ticket him (Choice 1)."""
    mock_decision.return_value = '1'
    events.tech_bro_speeding(stats)
    assert stats.pcr_hatred == 15


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_tech_bro_network(mock_decision, _, events, stats):
    """Scenario: Network with him (Choice 2)."""
    mock_decision.return_value = '2'
    events.tech_bro_speeding(stats)
    assert stats.coding_experience == 15  # +15


# ==========================================
# 15. PAPERWORK OVERLOAD
# ==========================================

@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_paperwork_automate_success(mock_decision, _, events, stats):
    """Scenario: Automate (Choice 1) with High Skill (>= 40)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 45

    events.paperwork_overload(stats)
    assert stats.ai_paperwork_buff is True
    assert stats.coding_experience == 50  # 45 + 5


@patch('builtins.input')
@patch('jb_game.game_logic.jb_dev_random_events.Decision.ask')
def test_event_paperwork_automate_fail(mock_decision, _, events, stats):
    """Scenario: Automate (Choice 1) with Low Skill (< 40)."""
    mock_decision.return_value = '1'
    stats.coding_experience = 20

    events.paperwork_overload(stats)
    assert stats.ai_paperwork_buff is False
    assert stats.pcr_hatred == 20