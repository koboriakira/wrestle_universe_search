from usecase.pull_episode import PullEpisodesUsecase
from infrastructure.json_repository.json_local_repository import JsonLocalRepository

def handler(event, context):
    print(event)
    print(context)
    usecase = PullEpisodesUsecase(repository=JsonLocalRepository())
    usecase.handle(next_page_token=None, stop_episode_id=None, dir="data")
