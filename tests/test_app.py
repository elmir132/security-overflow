import app as scanner


def test_benign_page_has_no_immediate_findings():
    result = scanner.analyze_page_content("<html><body><p>Welcome</p></body></html>")

    assert result == {
        "severity": "Low",
        "message": "No immediate vulnerabilities found.",
    }


def test_sql_injection_pattern_is_reported():
    result = scanner.analyze_page_content("UNION ALL SELECT username FROM users")

    assert result == {"severity": "High", "message": "Possible SQL Injection"}


def test_script_tag_is_reported_as_possible_xss():
    result = scanner.analyze_page_content("<script>alert('demo')</script>")

    assert result == {
        "severity": "High",
        "message": "Possible Cross-Site Scripting (XSS)",
    }
