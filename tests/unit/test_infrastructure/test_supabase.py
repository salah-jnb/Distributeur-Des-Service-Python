from src.infrastructure.database import get_supabase_client

def test_supabase_client_initialization():
    client = get_supabase_client()
    # Vérifie que l'objet client a bien été créé
    assert client is not None
    assert hasattr(client, "table")