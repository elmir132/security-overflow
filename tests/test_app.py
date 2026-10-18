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


def test_scan_rejects_a_url_without_http_or_https():
    client = scanner.app.test_client()
    for bad in ("file:///etc/passwd", "-oG /tmp/x", "javascript:alert(1)", "example.com"):
        response = client.post("/scan", json={"url": bad})
        assert response.status_code == 400
        assert "http" in response.get_json()["error"]


def test_env_file_is_read_without_overriding_the_real_environment(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("# comment\nGEMINI_TEST_KEY_A=from_file\nGEMINI_TEST_KEY_B='quoted'\n")
    monkeypatch.setenv("GEMINI_TEST_KEY_A", "already_set")
    monkeypatch.delenv("GEMINI_TEST_KEY_B", raising=False)
    scanner._load_env_file(str(env_file))
    import os

    assert os.environ["GEMINI_TEST_KEY_A"] == "already_set"
    assert os.environ["GEMINI_TEST_KEY_B"] == "quoted"
    monkeypatch.delenv("GEMINI_TEST_KEY_B", raising=False)
