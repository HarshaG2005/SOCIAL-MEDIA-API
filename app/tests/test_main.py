def test_health_check(client_real):
    res= client_real.get("/health")
    assert res.status_code == 200
    assert res.json()=={"status":"healthy"}
