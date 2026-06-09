import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve_chunks

# 1. Load environment variables (your Groq API key)
load_dotenv()

# 2. Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def handle_query(user_question):
    """Retrieves context and asks the LLM to generate a grounded answer."""
    
    # Retrieve the top 5 relevant chunks from your ChromaDB vault
    results = retrieve_chunks(user_question, top_k=5)
    
    context_blocks = []
    sources_list = []
    
    # Check if we got any results back at all
    if not results['documents'][0]:
        return "No relevant information found in the database.", "None"
        
    # Format the retrieved chunks into a single text block for the LLM to read
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        source = results['metadatas'][0][i]['source']
        
        # Inject metadata tags so the LLM knows where the text came from
        context_blocks.append(f"[Source: {source}]\n{doc}\n")
        sources_list.append(source)
            
    compiled_context = "\n".join(context_blocks)
    
    # Create a clean bulleted list of unique sources for the UI
    unique_sources = set(sources_list)
    formatted_sources = "\n".join([f"• {s}" for s in unique_sources])
    
    # 3. Define the strict System Prompt for Grounding
    system_prompt = (
        "You are an assistant for Queens College Computer Science students. "
        "You must answer the user's question using ONLY the provided context documents below. "
        "If the answer is not contained within the context, you must explicitly say: "
        "'I don't have enough information on that.' "
        "Do not use outside knowledge. Always cite your sources in your answer."
    )
    
    # 4. Call the Groq LLM
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context Documents:\n{compiled_context}\n\nUser Question: {user_question}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2 # Low temperature forces the AI to be factual instead of creative
        )
        llm_answer = chat_completion.choices[0].message.content
    except Exception as e:
        llm_answer = f"Error communicating with Groq: {e}"
        
    return llm_answer, formatted_sources

# 5. Build the Gradio Web Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 The Unofficial Guide: Queens College CS")
    gr.Markdown("Ask a question about Queens College CS professors based on real Rate My Professor reviews!")
    
    with gr.Row():
        inp = gr.Textbox(label="Your Question", placeholder="e.g., Which professor gives the most work?")
        
    btn = gr.Button("Ask the Guide", variant="primary")
    
    with gr.Row():
        answer_box = gr.Textbox(label="Answer", lines=8)
        sources_box = gr.Textbox(label="Retrieved Sources", lines=4)
        
    # Wire up the button and the Enter key to run the handle_query function
    btn.click(fn=handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(fn=handle_query, inputs=inp, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    print("Launching The Unofficial Guide...")
    demo.launch()