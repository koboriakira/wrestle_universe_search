from usecase.pull_episode import PullEpisodesUsecase
from infrastructure.json_repository.json_local_repository import JsonLocalRepository

def handler(event: dict, context):
    print(event)
    print(context)
    next_page_token = event.get("next_page_token")
    usecase = PullEpisodesUsecase(repository=JsonLocalRepository())
    next_page_token = usecase.handle(next_page_token=next_page_token, stop_episode_id=None, dir="data")
    result =  {
        "statusCode": 200,
        "body": {
            "message": "hello world",
            "next_page_token": next_page_token
        },
    }
    print(result)
    return result
