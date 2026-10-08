from fastapi.testclient import TestClient

def test_空の時は空配列が返る(client: TestClient) -> None:
    response = client.get("/diaries")
    assert response.status_code == 200
    assert response.json() == []

def test_登録すると採番されて返る(client: TestClient) -> None:
    response = client.post(
        "/diaries", json={"written_on": "2026-10-08", "body": "テスト用の日記"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "diary_id": 1,
        "written_on": "2026-10-08",
        "body": "テスト用の日記"
    }

def test_登録したものが一覧に出る(client: TestClient) -> None:
    client.post("/diaries", json={"written_on": "2026-10-08", "body": "1件目"})
    client.post("/diaries", json={"written_on": "2026-10-09", "body": "2件目"})
    
    response = client.get("/diaries")
    assert response.status_code == 200
    assert [row["body"] for row in response.json()] == ["1件目", "2件目"]

def test_存在しないIDは404(client: TestClient) -> None:
    response = client.get("/diaries/999")
    assert response.status_code == 404

def test_IDが数値でなければ422(client: TestClient) -> None:
    response = client.get("/diaries/abc")
    assert response.status_code == 422

def test_差し替えると中身が変わる(client: TestClient) -> None:
    client.post("/diaries", json={"written_on": "2026-10-08", "body": "書き換え前"})
    
    response = client.put(
        "/diaries/1", json={"written_on": "2026-10-10", "body": "書き換え後"}
    )
    assert response.status_code == 200
    assert response.json()["body"] == "書き換え後"
    assert response.json()["written_on"] == "2026-10-10"
    
def test_削除すると消える(client: TestClient) -> None:
    client.post("/diaries", json={"written_on": "2026-10-08", "body": "消される日記"})
    
    assert client.delete("/diaries/1").status_code == 204
    assert client.get("/diaries/1").status_code == 404
    assert client.get("/diaries").json() == []
