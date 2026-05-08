import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

def create_sales_context(row):
    """Construye el texto descriptivo de la venta."""
    return (f"Venta en {row['store_location']} de la categoría {row['product_category']}. "
            f"Producto: {row['product_type']}. Cantidad vendida: {row['transaction_qty']}. "
            f"Fecha: {row['transaction_date']}.")

def prepare_db():
    # 1. Cargar el archivo
    df = pd.read_excel('data/data-db.xlsx')
    
    # Limpieza de datos: Convertir fechas a texto
    df['transaction_date'] = df['transaction_date'].astype(str)
    
    # 2. Generar el contexto para los vectores
    df['search_context'] = df.apply(create_sales_context, axis=1)

    # 3. Configurar el cliente de ChromaDB
    client = chromadb.PersistentClient(path="./sales_vector_db")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(
        name="sales_collection", 
        embedding_function=emb_fn
    )

    print(f"Iniciando indexación de {len(df)} registros...")

    # --- SOLUCIÓN AL ERROR DE BATCH SIZE ---
    batch_size = 1000  # Procesaremos de 1000 en 1000
    
    for i in range(0, len(df), batch_size):
        # Extraemos el pedazo (chunk) de datos correspondiente al lote
        df_batch = df.iloc[i : i + batch_size]
        
        ids = [f"transaccion_{j}" for j in range(i, i + len(df_batch))]
        documents = df_batch['search_context'].tolist()
        metadatas = df_batch[['store_location', 'product_category', 'product_type', 'Sales', 'transaction_qty', 'transaction_date']].to_dict(orient='records')

        # Insertar el lote actual
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Indexados: {i + len(df_batch)} de {len(df)}...")

    print("\n¡Misión cumplida! Base de datos vectorial lista y optimizada.")
    

if __name__ == "__main__":
    prepare_db()
    
    