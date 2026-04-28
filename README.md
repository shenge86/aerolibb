# aerolibb
Originally formulated in 2016, this aerospace package has been recently resurrected. Its purpose is to be a tool for mission planning. 

This is also a sandbox for Shen to test out different Python libraries.

Notes:
- Spacecrafts are defined as classes and each subsystem (propulsion, power, comms, ADCS, etc.) are classes which can generate objects within the main spacecraft class.
- Aside from system classes, files with functions for simple orbital mechanics, controls, etc. will also be provided for use independently or with a spacecraft.

## Setup

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Directory

data
- 3rd party to be ingested

references
- PDF documents of interest

test
- Tests for different scripts. Not guaranteed to work yet.
