import torch

print("Torch version:", torch.__version__)

if torch.cuda.is_available():
    # CUDA availability
    print("CUDA available!")
    try:
        print("CUDA device count:", torch.cuda.device_count())
        for i in range(torch.cuda.device_count()):
            print(f"Device {i}:", torch.cuda.get_device_name(i))
        # Optional: device memory and current device
        print("Current CUDA device index:", torch.cuda.current_device())
        # show total memory for device 0 if available (PyTorch 1.8+)
        prop = torch.cuda.get_device_properties(0)
        print("Total memory (bytes):", prop.total_memory)

        print("All good!")

    except Exception as e:
        print("Warning: could not query full device info:", e)
else:
    # On macOS with MPS backend:
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("MPS backend is available (Apple Silicon).")

        print("All good!")
    else:
        print("No CUDA or MPS backend detected.")