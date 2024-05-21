# gem_api
This repository allows you to sets up a local instance of the GEM (Genome Editing Meta-database) API on your localhost. By cloning this repository and configuring it, you can efficiently search and interact with the GEM directly from your local environment. 

## How to use
1. `git clone https://github.com/szktkyk/gem_api.git`
2. `docker build -t gem_api .`
3. `docker run --rm -it -v $(pwd):/app -p 8000:8000 gem_api uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
4. Access `http://127.0.0.1:8000/docs`

