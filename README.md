# PyTorch on GPU for Your Project

by: Mariia Berdnyk
PhD student – DS4H | AI, Robotics & Virtual Reality<br>
I3S, CNRS & Inria laboratories<br>
Website : [mariiaberdnyk.vercel.app](https://mariiaberdnyk.vercel.app)<br>

## Advantages of Utilization of GPU for Learning/Tuning

**Speed:**
PyTorch on GPU can be **up to 10–50× faster** than on a processor (CPU), depending on your model size, batch size, and operation type. The acceleration comes from massive parallelism provided by NVIDIA CUDA cores.

---

## General Remarks

If you have **Linux**, GPU driver installation is a **tricky process**. Every distributor has its own guide, and most of them **don't work properly** (including some official step-by-step ones).

I have tested the installation on the most popular distributions yesterday, but I **cannot guarantee** that this guide won't break your OS completely (so badly that you will not even be able to start your computer). I also cannot guarantee that after you update your OS (`sudo apt-get update`), it won't randomly break the GPU driver.

That's a **common problem** for Linux and GPUs — even for experts.

**Advice:**
Keep your Linux installer on a USB key nearby, just in case. You can reinstall the same distribution on top of your data without losing it and try another guide :)

And don't get frustrated — personally, I've repeated the same process of OS reinstallation several times over the past two years of work at IBM.

---

If you have **Mac-provided** or **AMD** video cards — in most cases, **you are out of luck.**

* **Metal for MacOS:** Float128 problems; many libraries are not adapted for it.
* **AMD:** PyTorch/TensorFlow are not well adapted.

**Advice:**
Use **Google Colab** with **TPU** for learning or **rent GPU/TPU resources online** (e.g., AWS, Paperspace, or NVIDIA GPU Cloud).

In general for your personal carrier - If you want to perform **model/agent learning or tuning**, you **MUST** have a machine with an **NVIDIA GPU** and the latest **Ubuntu** versions or **Windows 11** (ideally both — dual boot).

---

There are alternatives to the **Anaconda** environment, but other environments **do not consistently support GPU utilization**.
You can install **Miniconda** instead — the difference is minor for GPU utilization.

**Anaconda advantages:**

* Constant support and bug fixes.
* If you encounter a PyTorch GPU utilization issue, you can report it and expect a quick fix.
* Most research and initial development is done primarily in Conda.

---

## General Steps of Installation
1. [Verify you have a **CUDA-capable GPU**](#1-verify-you-have-a-capable-gpuos)
2. [Install **Anaconda**](#2-anaconda-installation)
3. Create an environment in it with:
   * Python version **up to 3.10 for PyTorch**
   * Python version **3.8 for TensorFlow**
   ```bash
   conda create -n <your_env_name> python=<version>
   ```
   You will see:
   ```
   The following NEW packages will be INSTALLED:
   Proceed ([y]/n)? y
   ```
4. **Activate this environment:**
   ```bash
   conda activate <your_env_name>
   ```
5. [**NVIDIA Driver installation** (except for MacOS)](#3-nvidia-driver-installation)
6. [**CUDA Toolkit installation** (except for MacOS)](#4-cuda-toolkit-installation)
7. [**PyTorch/Anaconda packages download**](#5-pytorch--anaconda-packages-download)
8. [**Verification of successful installation**](#6-verification-of-successful-installation)

---

## 1. Verify You Have a Capable GPU/OS

> ⚠️ **Important:** Proceed only if the verification is successful! 

### CUDA is supported on Windows 10/11

You can verify that you have a CUDA-capable GPU through the **Display Adapters** section in the **Windows Device Manager**.
Here you'll find the vendor name and model of your graphics card(s).

If you have an NVIDIA card that is listed on [https://developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus), that GPU is CUDA-capable.

---

### MacOS

1. Press and hold the **Option** key while choosing **Apple menu > System Information**.
2. Click **Graphics/Displays** in the sidebar.
3. Check the information on the right for **Metal Support** or **Metal Family**:

   * If you see **Metal Support**, you'll also see the supported version of Metal.
   * If you see **Metal Family**, your Mac supports **Metal 2 and earlier**.

---

### Linux

**Verify You Have a CUDA-Capable GPU:**
Run:

```bash
lspci | grep -i nvidia
```

If you have an NVIDIA card listed on [https://developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus), it's CUDA-capable.

**Verify You Have a Supported Version of Linux:**
Run:

```bash
hostnamectl
```

Check if your distributor, OS version, and kernel are listed in **Table 1** here:
[https://docs.nvidia.com/cuda/cuda-installation-guide-linux/](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)

**Verify you have gcc installed:**

```bash
gcc --version
```

If not installed:

```bash
sudo apt install gcc
```

If all these verifications pass — continue with this guide.

---

## 2. Anaconda Installation

**General link:** [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)

---

### Windows

**Download the installer:**
[https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Windows-x86_64.exe](https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Windows-x86_64.exe)

(Optional, but recommended) **Verify installer integrity:**

```powershell
Get-FileHash .\Downloads\<INSTALLER_FILE> -Algorithm SHA256
```

Compare with the official hash at [repo.anaconda.com/archive](https://repo.anaconda.com/archive).

**Run the installer:**

* Click **Next**, then **I Agree** to accept the TOS.
* Choose **Just Me (recommended)** or **All Users**.
* Select destination folder → **Next**.
* (Optional) Add Anaconda3 to PATH.
* Click **Install** and wait for completion.
* Click **Next** twice → **Finish**.

---

### MacOS

**Download the .sh script:**

```bash
# Apple Silicon
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-MacOSX-arm64.sh

# Intel
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-MacOSX-x86_64.sh
```

**Verify integrity:**

```bash
shasum -a 256 ~/<INSTALLER-FILENAME>
```

Compare with the official SHA-256 hash from the Anaconda archive.

**Install:**

```bash
bash ~/Anaconda3-2025.06-0-MacOSX-<arch>.sh
```

Follow prompts:

* Accept TOS with `yes`
* Press Enter for the default path
* Choose initialization option:

  * **Yes (Recommended)** — automatically initializes Conda.
  * **No** — run manually:

    ```bash
    source <PATH_TO_CONDA>/bin/activate
    conda init --all
    ```

**Post-installation:**

```bash
conda config --set auto_activate_base False
```

Then close and reopen your terminal.

---

### Linux

**Download the .sh script:**

```bash
# x86
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh

# ARM64
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-aarch64.sh
```

**Verify integrity:**

```bash
shasum -a 256 ~/<INSTALLER-FILENAME>
```

**Install:**

```bash
bash ~/Anaconda3-2025.06-0-Linux-<arch>.sh
```

Follow the same initialization steps as above.

---

### (For All OS)

**Verify your installation:**

```bash
conda list
```

This displays a list of packages installed in your active environment and their versions.

---

## 3. NVIDIA Driver Installation

### Windows 10/11 (You Are Safe)

1. Install the **NVIDIA App**:
   [https://www.nvidia.com/en-us/software/nvidia-app/](https://www.nvidia.com/en-us/software/nvidia-app/)
2. Open it → **Drivers** section → Download the recommended driver.
3. Restart your computer (recommended).
4. Verify installation:

   ```bash
   nvidia-smi
   ```

---

### MacOS

Nothing to do.
Be happy and watch the struggles of your groupmates 😄

---

### Linux x86_64 / ARM64

#### Fedora 42 / RHEL 10

```bash
sudo dnf -y install cuda-drivers
sudo reboot
```

And pray. After reboot:

```bash
nvidia-smi
```

If your GPU and CUDA version are listed — congratulations, the first hazardous point is done!

---

#### Ubuntu 22.04 / 24.04 / Debian 12

```bash
sudo apt-get install -y cuda-drivers
sudo reboot
```

And pray. After reboot:

```bash
nvidia-smi
```

If your GPU and CUDA version are listed — you are in a safe zone now!

---

#### RHEL 8 / 9

```bash
sudo dnf -y module install nvidia-driver:latest-dkms
sudo reboot
```

And pray. After reboot:

```bash
nvidia-smi
```

If your GPU and CUDA version are listed — congratulations, you're good to go!
Got it — continuing in the **same clear and structured format** as before:

---

## 4. CUDA Toolkit Installation

### **Windows**

Download and open the installer for your system version:

* **Windows 10:**
  [https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_windows.exe](https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_windows.exe)

* **Windows 11:**
  [https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_windows.exe](https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_windows.exe)

Follow on-screen prompts during the installation.
After installation:

1. **Restart your OS.**
2. **Verify installation** in the Command Prompt (not PowerShell):

   ```bash
   nvcc --version
   ```

   If it returns the CUDA version (e.g., “release 13.0, V13.0.1”), the installation is successful.

---

### **MacOS**

Nothing to do. Be happy and watch struggles of your groupmates =D

---

### **Linux**

#### Fedora 42 / RHEL 8 / RHEL 9 / RHEL 10

Replace:

* `<distributor>` with one of: `fedora42`, `rhel10`, `rhel9`, or `rhel8`
* `<arch>` with `x86_64` or `aarch64`

```bash
wget https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda-repo-<distributor>-13-0-local-13.0.1_580.82.07-1.<arch>.rpm
sudo rpm -i cuda-repo-<distributor>-13-0-local-13.0.1_580.82.07-1.<arch>.rpm
sudo dnf clean all
sudo dnf -y install cuda-toolkit-13-0
sudo reboot
```

After reboot, verify installation:

```bash
nvcc --version
```

---

#### Ubuntu 22.04 / 24.04 / Debian 12 / RHEL 8

Replace:

* `<distributor>` with `ubuntu2204`, `ubuntu2404`, `debian12`, or `rhel8`
* `<arch>` with `amd64` (for x86_64) or `arm64`

> **Note:** The first two steps (pinning) are required only for Ubuntu distributors.

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600

wget https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda-repo-<distributor>-13-0-local_13.0.1-580.82.07-1_<arch>.deb
sudo dpkg -i cuda-repo-<distributor>-13-0-local_13.0.1-580.82.07-1_<arch>.deb
sudo cp /var/cuda-repo-<distributor>-13-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-13-0
sudo reboot
```

After reboot, verify installation:

```bash
nvcc --version
```

---

## 5. PyTorch / Anaconda Packages Download

### For All Operating Systems

1. Open **Terminal / Command Prompt**.
2. **Activate** the Anaconda environment you created in Step 2:

   ```bash
   conda activate <your_env_name>
   ```

#### **Windows / Linux**

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

#### **MacOS**

```bash
conda install pytorch torchvision torchaudio -c pytorch-nightly
```

---

## 6. Verification of Successful Installation

For all operating systems:

1. Open your terminal (or Command Prompt on Windows).
2. Activate your Anaconda environment:

   ```bash
   conda activate <your_env_name>
   ```
3. Run Python:

   ```bash
   python
   ```
4. Copy and paste the following code:

   ```python
    import torch
    if torch.cuda.is_available():
        print("CUDA available")
    else if torch.backends.mps.is_available():
        print("MPS available")
   ```

   * If you get the message:

     ```
     CUDA available
     ```
     or
     ```
     MPS available
     ```

     🎉 **Congratulations!** You now have a fully working GPU-enabled environment.

To exit Python:

```python
exit()
```

---

## Possibly (!!) Bonus Task for your project (Windows/Linux only — *MacOS excluded, it's too easy =D*)

> ⚠️ **Important:** Only one person from your team is enough to set up the gpu environment.

1. In your working environment, download the `command_remote_evaluation.py` from GitHub.
2. Execute:

   ```bash
   python ./<file_name>.py <YOUR_STUDENT_EMAIL>
   ```
3. You may test your setup beforehand with the `verification.py` script on the same GitHub page — if it returns `All good`, your submission will pass too.

> ⚠️ **Important:**
>
> * Submissions are allowed **only once.**
> * Any attempt to cheat (e.g., viewing the command from the script, modifying code, or sharing answers) will result in a **penalty instead of a bonus.**
> * We verify timestamps and emails — cheating or facilitating it for others will be detected.