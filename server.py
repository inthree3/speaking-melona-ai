import ngrok

listener = ngrok.forward("http://127.0.0.1:8000/", authtoken_from_env=True)

print(f"Ingress established at: {listener.url()}");