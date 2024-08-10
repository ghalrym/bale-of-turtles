from distutils.core import setup

setup(
    name="bale-of-turtles",
    version="1.0",
    packages=[
        "bale_of_turtles",
        "bale_of_turtles.llm_turtle",
        "bale_of_turtles.chat_turtle",
        "agent_turtle",
    ],
    package_dir={"": "src"},
    url="https://github.com/ghalrym/bale-of-turtles",
    license="",
    author="Andrew",
    author_email="",
    description="",
)
