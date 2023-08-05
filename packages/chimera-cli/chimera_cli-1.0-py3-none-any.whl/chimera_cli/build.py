from docker import from_env, APIClient
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from json import loads
from queue import Queue
client = from_env()
repo = Repo(search_parent_directories=True)
cli = APIClient()


def Tag(yaml: dict
        ):
    if repo.is_dirty():
        tag = '{}-dirty'.format(
            repo.git.describe(always=True)
        )
    else:
        tag = '{}'.format(
            repo.git.describe(always=True)
        )
    print(
        ' - \033[35m{} \033[31m --> \33[0m{}:{}'.format(
            yaml["build"]["image"],
            yaml["build"]["image"],
            tag
        )
    )
    return f"{yaml['build']['image']}:{tag}"


def TagAll(fullYaml: dict
           ):
    print('\033[35mTagging images...')

    for node in fullYaml['nodes']:
        tag = Tag(node)
        node['image'] = tag

    print('\033[35mFinished tagging images!\033[0m')


class BuildHandler(FileSystemEventHandler):
    def __init__(self,
                 base_path: str,
                 yaml: dict,
                 name: str,
                 namespace: str,
                 file: dict,
                 queue: Queue):
        super().__init__()

        self.base_path = base_path
        self.yaml = yaml
        self.name = name
        self.namespace = namespace
        self.queue = queue
        self.file = file

    def on_modified(self, event):
        self.queue.put(self)
        return super().on_modified(event)

    def on_created(self, event):
        self.queue.put(self)
        return super().on_created(event)

    def on_deleted(self, event):
        self.queue.put(self)
        return super().on_deleted(event)

    def on_any_event(self, event):

        return super().on_any_event(event)


def BuildAll(fullYaml):
    print('\n\n\033[33mBuilding all images...\n\n')

    for node in fullYaml['nodes']:
        Build(
            node['build']['context'],
            node['image']
        )


def Build(base_path: str, image_tag: str):

    print(f'\n\n\033[35mBuilding {image_tag}...\033[0m')

    stream = cli.build(path=base_path,
                       tag=f'{image_tag}'
                       )
    for line in stream:  # printing docker stream
        try:
            
            line = line.decode("utf-8")
            line = line.split("\r\n")
            line = map(lambda x: loads(x.encode("utf-8")), line[:-1])
            for current in line:
                print(current['stream'], end='')
        except KeyError:
            try:
                print(line['aux'], end='')
            except:
                pass

    print(f'\n\n\033[35mPushing {image_tag}...\033[0m')
    path, tag = image_tag.split(':')[:2]
    current_line: int = 0
    id_to_line: dict = {}
    max_line = 0
    for line in cli.push(path,
                         tag=tag,
                         stream=True):	
        line = line.decode("utf-8")
        line = line.split("\r\n")
        line = map(lambda x: loads(x.encode("utf-8")), line[:-1])
        for current in line:
            try:
                current_id = current['id']
            except KeyError:
                print()
                PrintLineOfStream(current)
                print()
            else:
                try:
                    delta = id_to_line[current_id] - current_line
                except KeyError:
                    id_to_line[current_id] = max_line
                    max_line += 1
                    delta = max_line - current_line
                    print(f'\033[{delta-1}B', end='\n')
                    current_line = max_line
                    start = ''
                else:
                    start = f'\033[{delta}B\033[0K\r'
                    current_line += delta
                PrintLineOfStream(current, start)


def PrintLineOfStream(current, start = ''):
    try:
        print(
            f'{start}{current["id"]}: {current["status"]} {current["progress"]}',
            end=''
        )
    except KeyError:
        try:
            print(
                f'{start}{current["id"]}: {current["status"]}',
                end=''
            )
        except KeyError:
            try:
                print(f'{start}{current["status"]}')
            except:
                pass


def Deploy(yaml: dict,
           name: str,
           namespace: str):
    from .api import chimera_rest_api
    formatted = yaml.copy()
    formatted['nodes'] = []
    for node in yaml['nodes']:
        formatted['nodes'] += [node.copy()]
    for node in formatted['nodes']:
        node.pop('build')

    chimera_rest_api.create_pipeline(name,
                                     namespace,
                                     formatted
                                     )
    print(
        "\n\n\033[35mPipeline {} created in namespace {}!".format(
            name, namespace
        )
    )


class DockerWatcher:
    def __init__(self,
                 src_path: str,
                 yaml: dict,
                 name: str,
                 namespace: str,
                 file,
                 queue: Queue):
        self.__src_path = src_path
        self.__event_handler = BuildHandler(
            src_path,
            yaml,
            name,
            namespace,
            file,
            queue
        )
        self.__event_observer = Observer()

    def run(self):
        self.start()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


def Watch(files):
    from .__main__ import parse_pipeline
    from queue import Queue
    from .api import chimera_rest_api
    q = Queue()
    print('\033[31m Starting watch mode...')
    for f in files:
        if f['type'] == 'pipeline':
            pipe = parse_pipeline(f)
            TagAll(pipe)
            BuildAll(pipe)
            for node in pipe['nodes']:
                DockerWatcher(node['build']['context'],
                              node,
                              f['name'],
                              f['namespace'],
                              pipe,
                              q
                              ).run()
            Deploy(pipe, f['name'], f['namespace'])
    while True:
        try:
            print('\n\n\n\n\033[31mWatching for changes...')
            item: BuildHandler = q.get()
            Build(
                item.yaml['build']['context'],
                item.yaml['image']
            )
            Deploy(
                item.file,
                item.name,
                item.namespace
            )
        except KeyboardInterrupt:
            print('Bye!')
            exit(0)
