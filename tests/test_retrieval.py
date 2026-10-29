from app.retrieval import load_knowledge, retrieve_knowledge


def test_load_knowledge():
    documents = load_knowledge()

    assert len(documents) == 4


def test_retrieve_502_knowledge():
    results = retrieve_knowledge("HTTP 502 Bad Gateway")

    assert len(results) > 0
    assert "HTTP 502 Bad Gateway" in results[0]


def test_retrieve_cpu_knowledge():
    results = retrieve_knowledge("high CPU usage")

    assert len(results) > 0
    assert "High CPU Usage" in results[0]


def test_retrieve_memory_knowledge():
    results = retrieve_knowledge("memory OOMKilled")

    assert len(results) > 0
    assert "Memory Issues" in results[0]


def test_retrieve_image_pull_knowledge():
    results = retrieve_knowledge("Kubernetes ImagePullBackOff")

    assert len(results) > 0
    assert "Kubernetes ImagePullBackOff" in results[0]
