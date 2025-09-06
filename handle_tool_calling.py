import requests

def handle_tool_call(tool_call):

    webhook_url = "https://velatdicleli.app.n8n.cloud/webhook-test/9b4ebd55-3ac0-4add-9595-38f50344cf99"
    
    payload = {
        "tool_name": tool_call["name"],
        "arguments": tool_call["arguments"]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=25)
        response.raise_for_status() 
        
        
        try:
            return response.json()
        except ValueError:
            return response.text

    except requests.exceptions.RequestException as e:
        print("Webhook gönderilirken hata oluştu:", e)
        return None
