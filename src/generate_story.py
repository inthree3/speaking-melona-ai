# %%
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
# %%
client=OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

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

    # if ending=="":
    #     ending=_generate_ending()

    base_prompt=f"""
    등장인물들:
    {{
    {characters_with_persona}
    }}
    엔딩:

    등장인물들의 페르소나를 설정한 후 드라마 플롯을 만들어줘. 레전드 설정은 막장 드라마 요소를 포함한, 20대 독자들이 매우 흥미가질만한 상상하기 어렵고 창의적인 설정이야. 각 인물의 말투는 성격을 잘 보여주어야 해. 엔딩이 나오기까지 어느정도의 서사가 있어야하며, 레전드 설정이 일부 드러나야해. 선생님이라면 담당 과목, 회사라면 사업 내용과 같이 모든 요소는 구체적으로 기술되어야 해. 등장인물 간의 궁합을 0부터 100 사이의 값으로 알려줘. 그리고 궁합 설명을 '둘이 없어 죽고 못 사는 사이 ♥️'와 같이 대화 내용을 기반으로 한 마디의 문장으로 말해줘. 아래의 json 형식 이외에 미사여구를 붙이지마.
    엔딩은 드라마 장면의 마지막 대사야. 다음 회차가 궁금해지고, 20대 독자들이 강렬하고 자극적이게 느낄 수 있는 대사여야 해. 감정 표현이나, 상황은 소괄호 안에 넣어서 설명해줘\n\n예시: (눈을 제대로 마주치지 못하며) 미...ㅁ.. 미안해\n예시와 같이 대사야.
    {{
    "상황": ,
    "엔딩": ,
    "등장인물 이름"{{
    "페르소나": ,
    "레전드 설정":
    }},
    "드라마 플롯": {{
    "등장인물 이름": 대사,
    [...]
    }},
    f"{linked_characters} 간 궁합 점수": ,
    f"{linked_characters} 간 궁합 설명":
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
def generate_drama_plot(characters, persona, ending=""):
    user_prompt=_generate_prompt(characters, persona, ending="")

    message = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4096,
    temperature=1,
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

    return message.choices[0].message.content
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
