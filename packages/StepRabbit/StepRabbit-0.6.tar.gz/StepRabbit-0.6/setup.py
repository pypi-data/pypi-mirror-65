from setuptools import setup  # type: ignore

setup(
    name="StepRabbit",
    version="0.6",
    description="Code snippets communicator",
    install_requires=["pika", "uuid",],
    author="Théo Daroun",
    author_email="mail@tdaron.tk",
    license="MIT",
    packages=["StepRabbit"],
    zip_safe=False,
)
