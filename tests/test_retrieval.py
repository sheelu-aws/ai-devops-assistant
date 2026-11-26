
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


def test_retrieve_multiple_symptoms():
    query = (
        "Production application has CPU utilization at 95%, "
        "memory usage above 95%, pods restarting with OOMKilled, "
        "and users receiving HTTP 503 errors."
    )

    results = retrieve_knowledge(query, top_k=4)

    combined_results = "\n".join(results)

    assert "High CPU Usage" in combined_results
    assert "Memory Issues" in combined_results
    assert "HTTP 502 Bad Gateway" in combined_results
