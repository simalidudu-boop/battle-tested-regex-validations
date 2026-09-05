import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tool import validate, validate_label, get_entries, get_entry_by_label, get_labels, search_entries


def test_entries_loaded():
    entries = get_entries()
    assert len(entries) >= 25


def test_all_entries_have_required_fields():
    entries = get_entries()
    for e in entries:
        assert "input" in e
        assert "label" in e
        assert "note" in e


def test_email_valid():
    assert validate_label("email", "user@example.com") is True
    assert validate_label("email", "first.last+tag@sub.domain.co.uk") is True


def test_email_invalid():
    assert validate_label("email", "not-an-email") is False
    assert validate_label("email", "@missing-local.com") is False
    assert validate_label("email", "user@") is False


def test_url_valid():
    assert validate_label("url", "https://www.example.com/path?q=1") is True
    assert validate_label("url", "http://example.org") is True


def test_url_invalid():
    assert validate_label("url", "not a url") is False


def test_phone_e164_valid():
    assert validate_label("phone-e164", "+14155552671") is True
    assert validate_label("phone-e164", "4915112345678") is True


def test_phone_e164_invalid():
    assert validate_label("phone-e164", "0123456789") is False
    assert validate_label("phone-e164", "abc") is False


def test_phone_us_valid():
    assert validate_label("phone-us", "(415) 555-2671") is True
    assert validate_label("phone-us", "415-555-2671") is True
    assert validate_label("phone-us", "415.555.2671") is True


def test_phone_us_invalid():
    assert validate_label("phone-us", "12345") is False


def test_ipv4_valid():
    assert validate_label("ipv4", "192.168.1.1") is True
    assert validate_label("ipv4", "0.0.0.0") is True
    assert validate_label("ipv4", "255.255.255.255") is True


def test_ipv4_invalid():
    assert validate_label("ipv4", "256.1.1.1") is False
    assert validate_label("ipv4", "1.2.3") is False


def test_uuid_valid():
    assert validate_label("uuid", "12345678-1234-1234-1234-123456789012") is True


def test_uuid_invalid():
    assert validate_label("uuid", "12345678123412341234123456789012") is False
    assert validate_label("uuid", "12345678-1234-1234-1234-12345678901") is False


def test_slug_valid():
    assert validate_label("slug", "my-blog-post") is True
    assert validate_label("slug", "a1b2c3") is True


def test_slug_invalid():
    assert validate_label("slug", "-leading-hyphen") is False
    assert validate_label("slug", "trailing-hyphen-") is False
    assert validate_label("slug", "UPPER-CASE") is False


def test_password_valid():
    assert validate_label("password", "Abc123!@") is True
    assert validate_label("password", "StrongPass1!") is True


def test_password_invalid():
    assert validate_label("password", "alllowercase1!") is False
    assert validate_label("password", "NoDigitsNoSpecial") is False
    assert validate_label("password", "Short1!") is False


def test_hex_color_valid():
    assert validate_label("hex-color", "#ff5733") is True
    assert validate_label("hex-color", "#abc") is True


def test_hex_color_invalid():
    assert validate_label("hex-color", "ff5733") is False
    assert validate_label("hex-color", "#gggggg") is False


def test_base64_valid():
    assert validate_label("base64", "SGVsbG8gV29ybGQ=") is True
    assert validate_label("base64", "dGVzdA==") is True


def test_base64_invalid():
    assert validate_label("base64", "not base64!") is False


def test_semver_valid():
    assert validate_label("semver", "1.2.3") is True
    assert validate_label("semver", "1.0.0-alpha.1") is True
    assert validate_label("semver", "2.1.0+build.123") is True


def test_semver_invalid():
    assert validate_label("semver", "1.2") is False
    assert validate_label("semver", "v1.2.3") is False


def test_iso8601_valid():
    assert validate_label("iso8601-datetime", "2024-01-15T10:30:00Z") is True
    assert validate_label("iso8601-datetime", "2024-01-15T10:30:00.123+05:30") is True


def test_iso8601_invalid():
    assert validate_label("iso8601-datetime", "2024-13-01T10:30:00Z") is False


def test_ssn_valid():
    assert validate_label("ssn", "123-45-6789") is True


def test_ssn_invalid():
    assert validate_label("ssn", "000-45-6789") is False
    assert validate_label("ssn", "666-45-6789") is False
    assert validate_label("ssn", "123-00-6789") is False
    assert validate_label("ssn", "123-45-0000") is False


def test_mac_address_valid():
    assert validate_label("mac-address", "00:1A:2B:3C:4D:5E") is True
    assert validate_label("mac-address", "ff:ff:ff:ff:ff:ff") is True


def test_mac_address_invalid():
    assert validate_label("mac-address", "00:1A:2B:3C:4D") is False


def test_postal_us_valid():
    assert validate_label("postal-us", "90210") is True
    assert validate_label("postal-us", "90210-1234") is True


def test_postal_us_invalid():
    assert validate_label("postal-us", "9021") is False


def test_api_key_valid():
    assert validate_label("api-key", "a1b2c3d4e5f6a7b8c9d0") is True


def test_api_key_invalid():
    assert validate_label("api-key", "short") is False
    assert validate_label("api-key", "a1b2c3d4e5f6a7b8c9d0!") is False


def test_credit_card_valid():
    assert validate_label("credit-card", "4111111111111111") is True
    assert validate_label("credit-card", "5500005555555559") is True


def test_credit_card_invalid():
    assert validate_label("credit-card", "1234567890123456") is False


def test_get_entry_by_label():
    entry = get_entry_by_label("email")
    assert entry is not None
    assert "input" in entry


def test_get_entry_by_label_not_found():
    entry = get_entry_by_label("nonexistent-label")
    assert entry is None


def test_get_labels():
    labels = get_labels()
    assert len(labels) >= 25
    assert "email" in labels
    assert "ipv4" in labels


def test_search_entries():
    results = search_entries("email")
    assert len(results) >= 1


def test_validate_direct():
    assert validate(r"^\d+$", "12345") is True
    assert validate(r"^\d+$", "abc") is False


def test_validate_bad_pattern():
    assert validate(r"[invalid", "test") is False
