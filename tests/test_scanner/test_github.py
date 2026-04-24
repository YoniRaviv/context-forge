import respx
from httpx import Response
from contextforge.models import Project
from contextforge.scanner.github import list_repos

@respx.mock
def test_list_repos():
    # This intercepts any GET to this URL and returns fake data
    fake_repos = [
        {"name": "frontend-app", "html_url": "https://github.com/acme/frontend-app", "language": "TypeScript", "archived": False, "fork": False},
        {"name": "payments-api", "html_url": "https://github.com/acme/payments-api", "language": "C#", "archived": False, "fork": False},
        {"name": "service-api", "html_url": "https://github.com/acme/service-api", "language": "Python", "archived": False, "fork": False},
        {"name": "CMS", "html_url": "https://github.com/acme/CMS", "language": "TypeScript", "archived": True, "fork": False},
        {"name": "Relay", "html_url": "https://github.com/acme/Relay", "language": "TypeScript", "archived": False, "fork": True},
    ]

    respx.get("https://api.github.com/orgs/acme/repos").mock(
        return_value=Response(200, json=fake_repos)
    )
    result = list_repos(org="acme", token="fake-token")
    assert result[0].name == "frontend-app"
    assert len(result) == 3
    assert isinstance(result[0], Project)

@respx.mock
def test_multiple_pages():
    fake_page_1 = [
        {"name": f"repo-{i}", "html_url": f"https://github.com/acme/repo-{i}", "language": "Python", "archived": False, "fork": False}
        for i in range(100)
    ]

    fake_page_2 = [
        {"name": f"repo-{i}", "html_url": f"https://github.com/acme/repo-{i}", "language": "Python", "archived": False, "fork": False}
        for i in range(100, 120)
    ]

    respx.get("https://api.github.com/orgs/acme/repos").mock(
        side_effect=[
            Response(200, json=[fake_page_1[0]]),
            Response(200, json=fake_page_1),
            Response(200, json=fake_page_2),
        ]
    )

    result = list_repos(org="acme", token="fake-token")
    assert len(result) == 120