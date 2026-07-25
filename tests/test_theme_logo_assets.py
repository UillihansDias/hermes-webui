"""Theme-aware Hermes logo regression coverage."""

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = (ROOT / "static" / "index.html").read_text("utf-8")
STYLE = (ROOT / "static" / "style.css").read_text("utf-8")
SERVICE_WORKER = (ROOT / "static" / "sw.js").read_text("utf-8")
BOOT = (ROOT / "static" / "boot.js").read_text("utf-8")


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", data[16:24])


def test_theme_logo_assets_are_valid_pngs():
    assert _png_size(ROOT / "static" / "logo-light.png") == (470, 477)
    assert _png_size(ROOT / "static" / "logo-dark.png") == (470, 477)


def test_both_logo_surfaces_include_light_and_dark_variants():
    assert INDEX.count('src="static/logo-light.png"') == 2
    assert INDEX.count('src="static/logo-dark.png"') == 2
    assert INDEX.count('class="theme-logo theme-logo--light"') == 2
    assert INDEX.count('class="theme-logo theme-logo--dark"') == 2


def test_dark_theme_selects_the_dark_surface_logo():
    assert ".theme-logo--dark{display:none;}" in STYLE
    assert ":root.dark .theme-logo--light{display:none;}" in STYLE
    assert ":root.dark .theme-logo--dark{display:block;}" in STYLE


def test_theme_logos_are_available_in_the_pwa_shell():
    assert "'./static/logo-light.png'" in SERVICE_WORKER
    assert "'./static/logo-dark.png'" in SERVICE_WORKER


def test_quick_theme_picker_drives_the_same_theme_path():
    assert 'aria-controls="railThemeOptions"' in INDEX
    assert "function toggleThemeDropdown(event)" in BOOT
    assert "function selectTheme(name,event)" in BOOT
    assert "_pickTheme(name);" in BOOT


def test_theme_button_has_a_css_fallback_before_javascript_syncs():
    button = INDEX.split('id="btnThemeToggle"', 1)[1].split("</button>", 1)[0]
    assert 'class="sun-icon"' in button
    assert 'class="moon-icon"' in button
    assert 'class="system-icon"' in button
    assert 'style="display:none"' not in button
    assert ".rail-theme-toggle #btnThemeToggle .sun-icon" in STYLE
    assert ":root.dark .rail-theme-toggle #btnThemeToggle .moon-icon" in STYLE


def test_empty_dashboard_info_does_not_separate_heading_from_subtitle():
    center_info = INDEX.split('id="dashboardCenterInfo"', 1)[1].split(">", 1)[0]
    assert "style=" not in center_info
    assert "#dashboardCenterInfo:empty{display:none;}" in STYLE
    assert "#dashboardCenterInfo:not(:empty)" in STYLE
