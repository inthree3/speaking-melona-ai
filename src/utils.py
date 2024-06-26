import json

def validate_response(json_response):
    try:
        data = json.loads(json_response)

        # Validate top-level keys
        required_keys = ["상황", "엔딩", "캐릭터", "플롯", "궁합"]
        for key in required_keys:
            if key not in data:
                return False, f"Missing key: {key}"

        # Validate "캐릭터"
        if not isinstance(data["캐릭터"], list):
            return False, "캐릭터 should be a list"

        for character in data["캐릭터"]:
            if not isinstance(character, dict):
                return False, "Each 캐릭터 should be a dictionary"
            required_character_keys = ["이름", "페르소나", "레전드_설정"]
            for key in required_character_keys:
                if key not in character:
                    return False, f"Missing key in 캐릭터: {key}"

        # Validate "플롯"
        if not isinstance(data["플롯"], list):
            return False, "플롯 should be a list"

        for plot_item in data["플롯"]:
            if not isinstance(plot_item, dict):
                return False, "Each 플롯 item should be a dictionary"
            required_plot_keys = ["캐릭터", "대사"]
            for key in required_plot_keys:
                if key not in plot_item:
                    return False, f"Missing key in 플롯: {key}"

        # Validate "궁합"
        if not isinstance(data["궁합"], dict):
            return False, "궁합 should be a dictionary"

        required_gungap_keys = ["점수", "설명"]
        for key in required_gungap_keys:
            if key not in data["궁합"]:
                return False, f"Missing key in 궁합: {key}"

        return True, "JSON is valid"
    
    except json.JSONDecodeError:
        return False, "Invalid JSON"
    

def format_for_twitter(data):
    plot = data["플롯"]
    compatibility = data["궁합"]

    tweets = []
    current_tweet = ""

    tweet_parts = []

    for scene in plot:
        tweet_part = f'{scene["캐릭터"]}: {scene["대사"]} '
        tweet_parts.append(tweet_part)

    compatibility_text = f'궁합 점수: {compatibility["점수"]} 설명: {compatibility["설명"]}'

    tweet_parts.append(compatibility_text)

    for tweet_part in tweet_parts:
        if len(current_tweet) + len(tweet_part) > 140:
            tweets.append(current_tweet.strip())
            current_tweet = tweet_part
        else:
            current_tweet += tweet_part

    if current_tweet:
        tweets.append(current_tweet.strip())

    return tweets
