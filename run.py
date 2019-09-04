import json
import weaklight

with open("tests/example_config.json") as f:
        config = json.load(f)

control = weaklight.Controller(config)
control.begin()