from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lxpcloud-device-agent",
    version="1.0.0",
    author="LexpAI",
    author_email="support@lexpai.com",
    description="LXPCloud IoT Device Agent for Industrial Monitoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lexpai/lxpcloud-device-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "asyncio-mqtt>=0.11.0",
        "pyserial>=3.5",
        "requests>=2.28.0",
        "pydantic>=1.10.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "raspberry_pi": [
            "RPi.GPIO>=0.7.0",
            "smbus2>=0.4.0",
            "Adafruit-DHT>=1.4.0",
        ],
        "arduino": [
            "pyserial>=3.5",
        ],
        "esp32": [
            "pyserial>=3.5",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lxpcloud-agent=lxpcloud_device_agent.cli:main",
        ],
    },
) 