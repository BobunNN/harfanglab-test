import pytest
from fastapi.testclient import TestClient

VALID_GAME = {
    "name": "The Witcher 3",
    "release_date": "2015-05-19",
    "studio": "CD Projekt RED",
    "ratings": 19,
    "platform": "PC",
}


def create_game(client: TestClient, payload: dict = None) -> dict:
    response = client.post("/video-games/", json=payload or VALID_GAME)
    assert response.status_code == 201
    return response.json()


class TestCreateVideoGame:
    def test_create_returns_game(self, client: TestClient):
        response = client.post("/video-games/", json=VALID_GAME)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == VALID_GAME["name"]
        assert data["platform"] == VALID_GAME["platform"]
        assert "uuid" in data

    def test_create_rejects_empty_name(self, client: TestClient):
        response = client.post("/video-games/", json={**VALID_GAME, "name": ""})
        assert response.status_code == 422

    def test_create_rejects_invalid_platform(self, client: TestClient):
        response = client.post("/video-games/", json={**VALID_GAME, "platform": "Xbox360"})
        assert response.status_code == 422

    def test_create_rejects_rating_out_of_range(self, client: TestClient):
        response = client.post("/video-games/", json={**VALID_GAME, "ratings": 21})
        assert response.status_code == 422


class TestGetVideoGame:
    def test_get_existing_game(self, client: TestClient):
        game = create_game(client)
        response = client.get(f"/video-games/{game['uuid']}")
        assert response.status_code == 200
        assert response.json()["uuid"] == game["uuid"]

    def test_get_nonexistent_game_returns_404(self, client: TestClient):
        response = client.get("/video-games/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestPatchVideoGame:
    def test_patch_updates_field(self, client: TestClient):
        game = create_game(client)
        response = client.patch(f"/video-games/{game['uuid']}", json={"ratings": 10})
        assert response.status_code == 200
        assert response.json()["ratings"] == 10

    def test_patch_does_not_overwrite_unset_fields(self, client: TestClient):
        game = create_game(client)
        client.patch(f"/video-games/{game['uuid']}", json={"ratings": 10})
        response = client.get(f"/video-games/{game['uuid']}")
        assert response.json()["name"] == VALID_GAME["name"]

    def test_patch_nonexistent_game_returns_404(self, client: TestClient):
        response = client.patch("/video-games/00000000-0000-0000-0000-000000000000", json={"ratings": 5})
        assert response.status_code == 404


class TestDeleteVideoGame:
    def test_delete_removes_game(self, client: TestClient):
        game = create_game(client)
        response = client.delete(f"/video-games/{game['uuid']}")
        assert response.status_code == 204
        assert client.get(f"/video-games/{game['uuid']}").status_code == 404

    def test_delete_nonexistent_game_returns_404(self, client: TestClient):
        response = client.delete("/video-games/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestFuzzyDuplicateCheck:
    def test_rejects_similar_name(self, client: TestClient):
        create_game(client)
        response = client.post("/video-games/", json={**VALID_GAME, "name": "The Witcher 3 "})
        assert response.status_code == 409

    def test_rejects_typo_name(self, client: TestClient):
        create_game(client, {**VALID_GAME, "name": "Don't Starve"})
        response = client.post("/video-games/", json={**VALID_GAME, "name": "Son't Starve"})
        assert response.status_code == 409

    def test_allows_different_name(self, client: TestClient):
        create_game(client)
        response = client.post("/video-games/", json={**VALID_GAME, "name": "Mario Kart 8"})
        assert response.status_code == 201


class TestSearchVideoGames:
    def test_search_returns_all_by_default(self, client: TestClient):
        create_game(client)
        create_game(client, {**VALID_GAME, "name": "Mario Kart 8"})
        response = client.get("/video-games/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_filter_by_name(self, client: TestClient):
        create_game(client)
        create_game(client, {**VALID_GAME, "name": "Mario Kart 8"})
        response = client.get("/video-games/?name=witcher")
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "The Witcher 3"

    def test_filter_by_platform(self, client: TestClient):
        create_game(client)
        create_game(client, {**VALID_GAME, "name": "Mario Kart 8", "platform": "Switch"})
        response = client.get("/video-games/?platform=Switch")
        assert len(response.json()) == 1

    def test_filter_by_min_ratings(self, client: TestClient):
        create_game(client)
        create_game(client, {**VALID_GAME, "name": "Low Rated Game", "ratings": 5})
        response = client.get("/video-games/?min_ratings=15")
        assert all(g["ratings"] >= 15 for g in response.json())

    def test_pagination_limit(self, client: TestClient):
        for i in range(5):
            create_game(client, {**VALID_GAME, "name": f"Game {i}"})
        response = client.get("/video-games/?limit=3")
        assert len(response.json()) == 3

    def test_pagination_offset(self, client: TestClient):
        for i in range(5):
            create_game(client, {**VALID_GAME, "name": f"Game {i}"})
        all_games = client.get("/video-games/").json()
        paginated = client.get("/video-games/?offset=2").json()
        assert paginated == all_games[2:]
