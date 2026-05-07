import gzip

import faiss
import ijson
import numpy as np
from constants.faiss import DIMENSION, INDEX_FILE


def preprocess_dataset(file_path):
    # Inicializa o índice HNSW
    # M=32 é um bom equilíbrio entre velocidade de busca e precisão
    index = faiss.IndexHNSWFlat(DIMENSION, 32, faiss.METRIC_INNER_PRODUCT)
    
    print("[*] Iniciando extração de vetores do GZ...")
    
    chunk = []
    chunk_size = 10000 
    
    with gzip.open(file_path, 'rb') as f:
        # 'item.vector' navega em: [{ 'vector': [aqui], 'label': '...' }, ...]
        parser = ijson.items(f, 'item.vector')
        
        for i, vector in enumerate(parser):
            chunk.append(vector)
            
            if len(chunk) >= chunk_size:
                _add_batch(index, chunk)
                chunk = []
                print(f"--- {i + 1} vetores indexados...")

        # Adiciona o restante
        if chunk:
            _add_batch(index, chunk)

    # Persistência do índice para performance absurda nas próximas rodadas
    faiss.write_index(index, INDEX_FILE)
    print(f"[SUCCESS] Índice HNSW criado com {index.ntotal} vetores.")
    return index

def _add_batch(index, vector_list):
    # Converte lista de listas diretamente para matriz float32
    arr = np.array(vector_list).astype('float32')
    # Normaliza para que a busca por Similaridade de Cosseno seja válida
    faiss.normalize_L2(arr)
    index.add(arr)