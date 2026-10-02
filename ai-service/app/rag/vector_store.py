import numpy as np
import pickle
import os
import logging
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.embeddings = []
        
        # Determine persistence file
        persist_dir = settings.chroma_persist_directory
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
        self.persist_path = os.path.join(persist_dir, "vector_store.pkl")
        
        self.load()

    def load(self):
        if os.path.exists(self.persist_path):
            try:
                with open(self.persist_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get('documents', [])
                    self.metadatas = data.get('metadatas', [])
                    self.ids = data.get('ids', [])
                    self.embeddings = data.get('embeddings', [])
                logger.info(f"Loaded {len(self.ids)} documents from {self.persist_path}")
            except Exception as e:
                logger.error(f"Failed to load vector store from {self.persist_path}: {e}")
                # Reset state if corrupted
                self.documents = []
                self.metadatas = []
                self.ids = []
                self.embeddings = []

    def save(self):
        try:
            with open(self.persist_path, 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                    'ids': self.ids,
                    'embeddings': self.embeddings
                }, f)
            logger.info(f"Saved {len(self.ids)} documents to {self.persist_path}")
        except Exception as e:
            logger.error(f"Failed to save vector store to {self.persist_path}: {e}")

    def add_document(self, doc_id: str, text: str, embedding: List[float], metadata: Optional[Dict] = None):
        self.add_documents_batch([doc_id], [text], [embedding], [metadata or {}])

    def add_documents_batch(self, doc_ids: List[str], texts: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict]] = None):
        if not metadatas:
            metadatas = [{}] * len(doc_ids)
        for d_id, text, emb, meta in zip(doc_ids, texts, embeddings, metadatas):
            if d_id in self.ids:
                idx = self.ids.index(d_id)
                self.documents[idx] = text
                self.embeddings[idx] = emb
                self.metadatas[idx] = meta
            else:
                self.ids.append(d_id)
                self.documents.append(text)
                self.embeddings.append(emb)
                self.metadatas.append(meta)
        self.save()

    def search(self, query_embedding: List[float], n_results: int = 5, where: Optional[Dict] = None) -> Dict:
        if not self.embeddings:
            return {'ids': [[]], 'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
        
        valid_indices = []
        for i, meta in enumerate(self.metadatas):
            if where:
                match = True
                for k, v in where.items():
                    if meta.get(k) != v:
                        match = False
                        break
                if match:
                    valid_indices.append(i)
            else:
                valid_indices.append(i)
                
        if not valid_indices:
            return {'ids': [[]], 'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

        target_embeddings = [self.embeddings[i] for i in valid_indices]
        sims = cosine_similarity([query_embedding], target_embeddings)[0]
        
        # Sort by similarity descending
        sorted_indices = np.argsort(sims)[::-1][:n_results]
        
        # Return in chromadb format
        res_ids = [self.ids[valid_indices[i]] for i in sorted_indices]
        res_docs = [self.documents[valid_indices[i]] for i in sorted_indices]
        res_metas = [self.metadatas[valid_indices[i]] for i in sorted_indices]
        # Return similarity score directly (higher is better) rather than distance
        # to match our similarity_threshold config logic
        res_scores = [float(sims[i]) for i in sorted_indices]
        
        return {
            'ids': [res_ids],
            'documents': [res_docs],
            'metadatas': [res_metas],
            'distances': [res_scores] # This actually contains cosine similarity (0 to 1)
        }

    def delete_document(self, doc_id: str):
        if doc_id in self.ids:
            idx = self.ids.index(doc_id)
            self.ids.pop(idx)
            self.documents.pop(idx)
            self.embeddings.pop(idx)
            self.metadatas.pop(idx)
            self.save()

    def delete_by_parent(self, parent_doc_id: str):
        indices_to_remove = [i for i, meta in enumerate(self.metadatas) if meta.get('parent_doc_id') == parent_doc_id]
        if indices_to_remove:
            for idx in sorted(indices_to_remove, reverse=True):
                self.ids.pop(idx)
                self.documents.pop(idx)
                self.embeddings.pop(idx)
                self.metadatas.pop(idx)
            self.save()

    def get_document(self, doc_id: str) -> Dict:
        if doc_id in self.ids:
            idx = self.ids.index(doc_id)
            return {'ids': [[doc_id]], 'documents': [[self.documents[idx]]], 'metadatas': [[self.metadatas[idx]]]}
        return {'ids': [[]], 'documents': [[]], 'metadatas': [[]]}

_vector_store = None
def get_vector_store():
    global _vector_store
    if _vector_store is None: _vector_store = VectorStore()
    return _vector_store
