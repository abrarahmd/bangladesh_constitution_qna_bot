from flask import Flask, request, jsonify
from flask_cors import CORS
from chunker import chunk_text
from embedder import get_embedder
from vector_store import get_chroma_db, create_collection, index_chunks
from rag_pipeline import retrieve, build_prompt, generate_answer
from config import MARKDOWN_PATH
import os
import atexit

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global variables to store initialized components
embedder = None
collection = None
db = None
is_indexed = False

def initialize_system():
    """Initialize the RAG system components once at startup"""
    global embedder, collection, db, is_indexed
    
    print("🚀 Starting RAG system initialization...")
    
    try:
        # Initialize embedder (this is the expensive operation)
        print("📊 Loading embedder...")
        embedder = get_embedder()
        print("✅ Embedder loaded successfully!")
        
        # Initialize vector database
        print("🗄️ Connecting to vector database...")
        db = get_chroma_db()
        collection = create_collection(db)
        print("✅ Vector database connected!")
        
        # Check if we need to index documents
        try:
            count = collection.count()
            if count == 0:
                print("📚 No existing data found. Indexing documents...")
                
                # Load and chunk text
                with open(MARKDOWN_PATH, "r", encoding="utf-8") as f:
                    text = f.read()
                
                chunks = chunk_text(text)
                print(f"📄 Created {len(chunks)} chunks from document")
                
                # Index chunks (this will use the already loaded embedder)
                index_chunks(chunks, embedder, collection)
                is_indexed = True
                print("✅ Document indexing completed!")
            else:
                is_indexed = True
                print(f"✅ Found {count} existing chunks in database. Skipping indexing.")
                
        except Exception as e:
            print(f"⚠️ Error checking/creating index: {e}")
            return False
            
        print("🎉 RAG system initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return False

def cleanup():
    """Cleanup function called when server shuts down"""
    global db
    if db:
        print("🧹 Cleaning up database connections...")
        # Add any cleanup code here if needed

# Register cleanup function
atexit.register(cleanup)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "indexed": is_indexed
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - uses pre-initialized components"""
    try:
        # Get message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "error": "No message provided"
            }), 400
        
        query = data['message'].strip()
        if not query:
            return jsonify({
                "error": "Empty message"
            }), 400
        
        # Check if system is initialized (should always be true after startup)
        if not is_indexed or embedder is None or collection is None:
            return jsonify({
                "error": "System not properly initialized. Please restart the server."
            }), 500
        
        # Process the query through RAG pipeline (fast - just retrieval and generation)
        context = retrieve(collection, embedder, query)
        prompt = build_prompt(context, query)
        answer = generate_answer(prompt)
        
        return jsonify({
            "response": answer,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/reindex', methods=['POST'])
def reindex():
    """Reindex the chunks - only use when document content changes"""
    global embedder, collection, is_indexed
    
    try:
        if embedder is None or collection is None:
            return jsonify({
                "error": "System not initialized properly"
            }), 500
        
        print("🔄 Starting reindexing process...")
        
        # Load and chunk text
        with open(MARKDOWN_PATH, "r", encoding="utf-8") as f:
            text = f.read()
        
        chunks = chunk_text(text)
        print(f"📄 Created {len(chunks)} chunks from updated document")
        
        # Clear existing collection and reindex
        # Note: This recreates the collection, clearing old data
        global db
        collection = create_collection(db)
        index_chunks(chunks, embedder, collection)
        is_indexed = True
        
        print("✅ Reindexing completed successfully!")
        
        return jsonify({
            "message": f"Reindexing completed successfully. Processed {len(chunks)} chunks.",
            "status": "success"
        })
            
    except Exception as e:
        print(f"❌ Reindexing failed: {e}")
        return jsonify({
            "error": f"Reindexing failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        "indexed": is_indexed,
        "embedder_ready": embedder is not None,
        "collection_ready": collection is not None,
        "document_path": MARKDOWN_PATH,
        "document_exists": os.path.exists(MARKDOWN_PATH)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "status": "error"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": "error"
    }), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 RAG Chat API Server")
    print("=" * 60)
    
    if initialize_system():
        print("\n" + "=" * 60)
        print("🎉 Server ready! Starting Flask application...")
        print("📡 API will be available at: http://localhost:5000")
        print("🔗 Health check: http://localhost:5000/api/health")
        print("=" * 60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n" + "=" * 60)
        print("❌ Failed to initialize RAG system. Server not started.")
        print("📋 Please check your configuration and try again.")
        print("=" * 60)