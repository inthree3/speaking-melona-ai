# %%
import anthropic
from dotenv import load_dotenv
import os

load_dotenv(override=True)
# %%
client=anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)
# %%

characters = {
    '1329841072314983': {
        'name': '크림빵',
        'persona': '전 세계에서 가장 유명한 크림빵. 누구나 한 번쯤은 먹어봤을 정도로 유명하다. 그러나 그의 내면은 아무도 모르는 비밀로 가득하다. 그의 페르소나는 무엇일까?'
    }
}

if __name__=="__main__":
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=1,
        system="너는 드라마 대본을 작성하는 AI assistant야. 사람들의 관심을 끌 수 있는 대본을 작성하는 데에 관심이 있어.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "창의적인 드라마 대본을 작성해줘. 한 장면으로 구성되도록 해줘. 20대 이상의 독자들도 흥미롭게 읽을 수 있도록 잔인하고, 흥미로운 악역을 이야기에 포함해줘. 캐릭터의 말투는 각자의 페르소나가 드러나게끔 설정해줘.\n주인공: 크림빵, 바나나 우유\n다음의 내용만 포함되도록 해줘.\n\n[페르소나]\n크림빵의 페르소나:\n바나나 우유의 페르소나:\n[씬 정보]\n[대본]\n크림빵:\n바나나 우유:"
                    }    
                ]
            }
        ]
    )
    # %%
    def generate_message(message):
        return message.content[0].text
    # %%

def barcode_to_character(barcode):
    return characters.get(barcode, None)