from usecase.pull_episode import PullEpisodesUsecase

def handler(event, context):
    print(event)
    print(context)
    usecase = PullEpisodesUsecase()
    usecase.handle(next_page_token=None, stop_episode_id=None, dir="data")
