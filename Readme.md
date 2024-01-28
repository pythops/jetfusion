# Diffusion models on Jetson boards

Easy deploy of diffusion models on Nvidia jetson boards.

## 🧰 Requirement

- Nvidia Jetson board with at least 8GB of Memory.
- At least 25GB free space on the disk.

## 🛠️ Setup

1. Download and install the minamilist image for your board [here🔗](https://github.com/pythops/jetson-image)

2. Install the necessary dependencies

```
sudo apt update && \
sudo apt install -y \
    cuda-toolkit-11-4 \
    libcudnn8-dev \
    libnuma-dev \
    libopenblas-dev \
    autoconf \
    build-essential \
    g++-8 \
    gcc-8 \
    clang-8 \
    lld-8 \
    gettext-base \
    gfortran-8 \
    libbz2-dev \
    libc++-dev \
    libcgal-dev \
    libffi-dev \
    libfreetype6-dev \
    libhdf5-dev \
    libjpeg-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libssl-dev \
    libxslt-dev \
    openssl \
    python-openssl \
    scons \
    python3-pip \
    python-is-python3 \
    libopenblas-dev \
    git-lfs && \
pip install --user poetry
```

3. Add `$USER` (by default `jetson`) user to the video group

```
sudo usermod -aG video $USER
```

> You need to re-login for the changes to take effect.

4. Clone `sd-turbo` diffusion model

```
mkdir -p ~/diffusion/sd-turbo && \
git lfs install --skip-repo && \
git clone https://huggingface.co/stabilityai/sd-turbo ~/diffusion/sd-turbo

```

4. Clone the jetfusion repository

```
git clone https://github.com/pythops/jetfusion && cd jetfusion
```

4. Install the python dependencies

```
poetry install --no-root
```

5. Run the api server

```
DIFFUSION_MODEL_DIR="$HOME/diffusion/sd-turbo" poetry run uvicorn --host 0.0.0.0 api:api
```

## 🪃 Usage

To display images in your terminal, you'll need to install [img2sixel](https://github.com/saitoha/libsixel)

Your terminal should support the sixel graphics format, check here for more infos https://www.arewesixelyet.com/

### Using curl

```
curl -s https://localhost:8000/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Colorful fish in the coral reef"}' | img2sixel
```

### Using httpie

```
http https://localhost:8000/generate \
prompt="Colorful fish in the coral reef" | img2sixel
```

## ⚖️ License

AGPLv3
