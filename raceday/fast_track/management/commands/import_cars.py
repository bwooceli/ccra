from lib2to3.pytree import Base
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Connect to the track gate and run the race"

    def handle(self, *args, **kwargs):
        print("Paste data from google sheet and then CTRL-Z")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        
        print(contents[0])
