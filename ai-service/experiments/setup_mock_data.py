import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag.rag_pipeline import get_rag_pipeline

def ingest_mock_dataset():
    rag = get_rag_pipeline()
    
    docs = [
        {"id": "int1", "text": "In my Amazon SDE interview, they asked me to implement LRU cache and explain Dijkstra algorithm. The interviewer was friendly.", "metadata": {"interviewId": "int1", "company": "Amazon", "role": "SDE", "year": 2024, "source": "mock_dataset"}},
        {"id": "int2", "text": "Software engineering interviews usually cover Data Structures, Algorithms, and System Design. You should prepare well.", "metadata": {"interviewId": "int2", "company": "General", "role": "Software Engineer", "year": 2023, "source": "mock_dataset"}},
        {"id": "int3", "text": "System design interviews focus on scalability, database sharding, caching, and load balancing.", "metadata": {"interviewId": "int3", "company": "General", "role": "Backend Developer", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_4", "text": "For the Google Frontend role, I was asked to build a responsive React component from scratch and explain virtual DOM diffing.", "metadata": {"interviewId": "mock_4", "company": "Google", "role": "Frontend", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_5", "text": "My Microsoft SWE interview had 4 rounds. Round 1 was array manipulation. Round 2 was a system design for a chat application. Round 3 was behavioral.", "metadata": {"interviewId": "mock_5", "company": "Microsoft", "role": "SWE", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_6", "text": "In the Meta Data Engineer interview, I had to write complex SQL queries involving window functions and explain data pipeline orchestration with Airflow.", "metadata": {"interviewId": "mock_6", "company": "Meta", "role": "Data Engineer", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_7", "text": "The Apple iOS Engineer interview focused heavily on Swift memory management, ARC, and building multi-threaded apps using Grand Central Dispatch.", "metadata": {"interviewId": "mock_7", "company": "Apple", "role": "iOS Engineer", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_8", "text": "Stripe backend interview was very practical. I had to integrate a dummy payment API and handle failure scenarios and retries gracefully.", "metadata": {"interviewId": "mock_8", "company": "Stripe", "role": "Backend", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_9", "text": "For the Netflix Senior SDE role, the system design round was intense. We discussed video streaming protocols, CDN caching strategies, and global state replication.", "metadata": {"interviewId": "mock_9", "company": "Netflix", "role": "Senior SDE", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_10", "text": "Amazon Data Science interview: We discussed Random Forests vs Gradient Boosting, and I was asked to write a Python script for K-Means clustering from scratch.", "metadata": {"interviewId": "mock_10", "company": "Amazon", "role": "Data Scientist", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_11", "text": "In the Google SWE behavioral round, they asked about a time I disagreed with a teammate and how I resolved it. Also, why Google?", "metadata": {"interviewId": "mock_11", "company": "Google", "role": "SWE", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_12", "text": "A key question in the Meta ML Engineer interview was deriving the backpropagation equations for a simple neural network and optimizing it for GPU.", "metadata": {"interviewId": "mock_12", "company": "Meta", "role": "ML Engineer", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_13", "text": "The Microsoft PM interview involved a case study on designing a new feature for Teams. I had to define KPIs, user personas, and a go-to-market strategy.", "metadata": {"interviewId": "mock_13", "company": "Microsoft", "role": "Product Manager", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_14", "text": "During my Apple Hardware Engineering interview, I was tested on signal integrity, PCB layout basics, and thermal dissipation modeling.", "metadata": {"interviewId": "mock_14", "company": "Apple", "role": "Hardware Engineer", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_15", "text": "My Snowflake SWE interview focused deeply on distributed database consensus protocols like Paxos and Raft, and handling network partitions.", "metadata": {"interviewId": "mock_15", "company": "Snowflake", "role": "SWE", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_16", "text": "For Amazon's SDET role, I was asked to design an automated testing framework for a microservices architecture using Selenium and PyTest.", "metadata": {"interviewId": "mock_16", "company": "Amazon", "role": "SDET", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_17", "text": "The Google Cloud Architect interview covered Kubernetes networking, hybrid cloud deployments, and setting up IAM roles securely.", "metadata": {"interviewId": "mock_17", "company": "Google", "role": "Cloud Architect", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_18", "text": "In the Uber backend interview, the focus was on geospatial indexing. I had to design a system to match riders with drivers efficiently using QuadTrees or Geohashes.", "metadata": {"interviewId": "mock_18", "company": "Uber", "role": "Backend", "year": 2024, "source": "mock_dataset"}},
        {"id": "mock_19", "text": "My Spotify frontend interview was all about Web Audio API and state management using Redux. We discussed optimising audio playback latency in the browser.", "metadata": {"interviewId": "mock_19", "company": "Spotify", "role": "Frontend", "year": 2023, "source": "mock_dataset"}},
        {"id": "mock_20", "text": "Airbnb SWE interview: I was asked to build a date picker component in React and write a system design document for their booking system to prevent double bookings.", "metadata": {"interviewId": "mock_20", "company": "Airbnb", "role": "SWE", "year": 2024, "source": "mock_dataset"}}
    ]
    
    # First clear vector store to ensure clean state
    rag.vector_store.documents = []
    rag.vector_store.metadatas = []
    rag.vector_store.ids = []
    rag.vector_store.embeddings = []
    rag.vector_store.save()
    
    for doc in docs:
        rag.ingest_document_with_chunks(doc["id"], doc["text"], doc["metadata"])
    print(f"Indexed {len(docs)} mock documents successfully.")

if __name__ == "__main__":
    ingest_mock_dataset()
