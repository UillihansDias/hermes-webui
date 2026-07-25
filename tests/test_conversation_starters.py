"""Conversation starter copy and empty-state layout regression coverage."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = (ROOT / "static" / "index.html").read_text("utf-8")
STYLE = (ROOT / "static" / "style.css").read_text("utf-8")
I18N = (ROOT / "static" / "i18n.js").read_text("utf-8")


def test_empty_state_uses_the_command_hint_from_the_reference():
    assert 'data-i18n="empty_subtitle_lead">Type a message below ·</span>' in INDEX
    assert '<kbd aria-label="slash">/</kbd>' in INDEX
    assert 'data-i18n="empty_subtitle_commands">for commands</span>' in INDEX
    assert "empty_subtitle_lead: 'Type a message below ·'" in I18N
    assert "empty_subtitle_commands: 'for commands'" in I18N


def test_reference_conversation_starters_fill_the_composer_with_exact_copy():
    starters = (
        ("suggest_capabilities", "What can you do?"),
        ("suggest_recent_sessions", "Summarize my recent sessions"),
        ("suggest_channel", "Help me configure a channel"),
        ("suggest_health", "Check system health"),
    )
    for key, message in starters:
        assert f'data-msg="{message}"' in INDEX
        assert f'data-i18n="{key}">{message}</span>' in INDEX
        assert f"{key}: '{message}'" in I18N


def test_starters_use_a_responsive_two_column_grid():
    assert ".suggestion-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))" in STYLE
    assert ".suggestion-grid{width:100%;max-width:720px;}" in STYLE
    assert "@media(max-width:640px){.suggestion-grid{grid-template-columns:1fr;" in STYLE
