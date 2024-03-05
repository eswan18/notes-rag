# Notes RAG

The easiest way to run this is to get an API key from OpenAI and then invoke the driver file.

```bash
OPENAI_API_KEY=abcdef ipython -i driver.py
```

After this runs, you will have an interactive Python session including a `do_query` function and a `retriever` object that you can call yourself:

```python
do_query(
    'What's my favorite color, based on my notes?',
    retriever=retriever, 
    model_type='openai',
)
```
