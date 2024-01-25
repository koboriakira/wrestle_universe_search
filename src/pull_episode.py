from usecase.pull_episode import PullEpisodesUsecase
from infrastructure.json_repository.json_local_repository import JsonLocalRepository

def handler(event: dict, context):
    print(event)
    print(context)
    next_page_token = event.get("next_page_token")
    count = event.get("count") or 1
    usecase = PullEpisodesUsecase(repository=JsonLocalRepository())
    next_page_token = usecase.handle(next_page_token=next_page_token, stop_episode_id=None, dir="data", count=count)
    result =  {
        "statusCode": 200,
        "body": {
            "message": "success",
            "next_page_token": next_page_token
        },
    }
    return result
