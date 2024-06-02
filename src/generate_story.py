# %%
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)
# %%
client=OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

json_format = '''
    {
        "플롯": [
            {
                "캐릭터": "캐릭터 이름",
                "대사": "대사"
            }
            # 대사는 4-5개로 구성
        ],
        "궁합": 캐릭터간의 궁합 점수 (0-100, integer),
    }
'''


# %%
def _generate_prompt(characters, persona, ending=""):
    characters_with_persona={}
    newbie_characters=[]
    for character in characters:
        if character not in persona.keys():
            newbie_characters.append(character)
            continue
        characters_with_persona[character]=persona[character]
    
    linked_characters="와 ".join(characters)

    print(linked_characters)

    # if ending=="":
    #     ending=_generate_ending()

    base_prompt=f"""
    등장인물들의 페르소나를 이용해 드라마 플롯을 만들어줘. 레전드 설정은 막장 드라마 요소를 포함한, 20대 독자들이 매우 흥미가질만한 상상하기 어렵고 창의적인 설정이야. 각 인물의 말투는 성격을 잘 보여주어야 해. 엔딩이 나오기까지 어느정도의 서사가 있어야하며, 레전드 설정이 일부 드러나야해. 선생님이라면 담당 과목, 회사라면 사업 내용과 같이 모든 요소는 구체적으로 기술되어야 해. 등장인물 간의 궁합을 0부터 100 사이의 값으로 알려줘. 그리고 궁합 설명을 대화 내용을 기반으로 한 마디의 문장으로 말해줘. 아래의 json 형식 이외에 미사여구를 붙이지마.
    엔딩은 드라마 장면의 마지막 대사야. 다음 회차가 궁금해지고, 20대 독자들이 강렬하고 자극적이게 느낄 수 있는 대사여야 해. 감정 표현이나, 상황은 소괄호 안에 넣어서 설명해줘\n\n예시: (눈을 제대로 마주치지 못하며) 미...ㅁ.. 미안해\n예시와 같이 대사야.
    제공된 등장인물 이외의 인물을 등장시켜선 안돼. 등장시킨다면 '회사원'이나 '학생'과 같이 무명으로 설정해야해. 또한, 등장인물의 이름을 다르게 설정하거나, 페르소나를 변경해서는 안돼. 등장인물의 이름과 페르소나는 제공된 것을 그대로 사용해야해.
    각 예시는 예시일 뿐 무조건 따라하지는 마. 창의적인 답변일수록 좋아.

    등장인물들:
    {{
    {characters_with_persona}
    }},
    {{
    "상황": 대화가 진행되는 시간, 장소, 분위기에 대한 설명,
    "엔딩": 20대 독자들이 강렬하고 자극적으로 느낄 만한 엔딩,
    "등장인물 이름"{{
    "페르소나": 캐릭터별 제공된 페르소나,
    "레전드 설정": 캐릭터별 자극적인 설정 (ex - ㅇㅇㅇ은 천재적인 범죄자이며, ㅇㅇㅇ의 동생을 포함한 여러 사건의 배후. 겉으로는 연약해 보이지만, 사실 머리 좋은 전략가로서 많은 사람들이 그의 존재를 두려워한다 or ㅇㅇ은 삼각 관계에 끼어들어, ㅇㅇ과 ㅇㅇ을 서로 빼앗기 위해 모든 것을 할 수 있다. ㅇㅇ은 겉으로는 양아치인 척을 하지만, 그건 자신을 이렇게 만든 세상에 대한 반항일 뿐, 사실은 누구보다 순수한 마음을 가지고 있다.)
    }},
    "플롯": {
        [
            {
                "캐릭터": "캐릭터 이름",
                "대사": "대사"
            }
            # 4-5개의 대사로 구성
        ]
    },
    궁합: {{
        "점수": {linked_characters} 간의 궁합 점수 (0-100, integer) ,
        "설명": {linked_characters} 간의 궁합 한마디 설명 (ex - ㅇㅇㅇ과 ㅇㅇㅇ은 서로를 이해하지 못하는 관계 🤷, ㅇㅇ은 ㅇㅇ와 둘이 없어 죽고 못사는 사이 😍, ㅇㅇ은 ㅇㅇ와 원수 ⚔)
    }},
    }}
    """
    return base_prompt
# %%
def _generate_ending():
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "드라마 엔딩 장면의 마지막 대사를 출력해줘. 다음 회차가 궁금해지고, 20대 독자들이 강렬하고 자극적이게 느낄 수 있는 대사여야 해. 감정 표현이나, 상황은 소괄호 안에 넣어서 설명해줘\n\n예시: (눈을 제대로 마주치지 못하며) 미...ㅁ.. 미안해\n예시와 같이 대사를 출력해. 미사여구는 붙이지 마."}],
    )

    return response.choices[0].message.content
# %%
def generate_drama_plot(item):
    characters=item["characters"]
    persona=item["persona"]
    ending=item["ending"]
    user_prompt=_generate_prompt(characters, persona)

    message = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4096,
    temperature=1,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system",
         "content": "너는 드라마 대본을 작성하는 AI assistant야. 사람들의 관심을 끌 수 있는 대본을 작성하는 데에 관심이 있어. 창의적인 드라마 대본을 작성해줘. 한 장면으로 구성되도록 해줘. 20대 이상의 독자들도 흥미롭게 읽을 수 있도록 잔인하고, 흥미로운 악역을 이야기에 포함해줘. 캐릭터의 말투는 각자의 페르소나가 드러나게끔 설정해줘."},
        {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": user_prompt
                    }    
                ]
            }
        ]
    )

    print(message.choices[0].message.content)

    return json.loads(message.choices[0].message.content)
# %%
characters=["크림빵", "바나나 우유"]
persona={
    "크림빵": "수줍음이 많고 낯을 가리는 편이지만, 마음 깊은 곳엔 강한 의지가 있다. 말투는 부드럽고 점잖으나 때론 결연해지기도 한다.",
    "바나나 우유": "밝고 활발한 성격으로 누구와도 잘 어울린다. 유쾌하고 장난스러운 말투를 즐겨 쓰지만, 진지할 땐 똑 부러지게 말한다."
}

ending=""
if __name__=="__main__":
    drama_plot_response=generate_drama_plot(characters, persona)
    print(drama_plot_response)
# %%
