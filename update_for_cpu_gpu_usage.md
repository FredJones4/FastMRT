To enable **GPU and CPU usage logging in Weights & Biases (WandB)** for your current PyTorch Lightning system, you need to **explicitly enable system metrics tracking**.

---

### **✅ Steps to Modify Your Script to Log GPU/CPU Usage in WandB**
### **1. Enable System Metrics Logging in WandB**
Modify the **WandB Logger initialization** in your `FastmrtRunner` class:
```python
import wandb

# Initialize WandB Logger
self.logger = loggers.WandbLogger(
    save_dir=self.args.log_dir, 
    name=self.args.log_name, 
    project=self.args.net.upper(),
    log_model=True  # Ensures model checkpoints are tracked
)

# Enable system monitoring
wandb.init(
    project=self.args.net.upper(), 
    name=self.args.log_name, 
    config=log_cfgs,
    settings=wandb.Settings(code_dir="."),  # Tracks code changes
    monitor_gym=True,  # Enables system metrics logging
)
```

---

### **2. Log GPU & CPU Utilization During Training**
Add these **manual logging metrics** after defining the logger:

#### **Inside `FastmrtRunner.__init__` after initializing `self.logger`**
```python
import torch

# Log available GPU and CPU details
gpu_count = torch.cuda.device_count()
gpu_names = [torch.cuda.get_device_name(i) for i in range(gpu_count)] if gpu_count > 0 else ["No GPU"]
cpu_count = os.cpu_count()

wandb.config.update({
    "num_gpus": gpu_count,
    "gpu_names": gpu_names,
    "num_cpus": cpu_count
})

print(f"Logging System Info: {gpu_count} GPUs, {cpu_count} CPUs")
```

---

### **3. Log GPU/CPU Utilization in Real-Time**
Modify your **training loop** to log GPU and CPU usage **every epoch**.

#### **Inside the `FastmrtRunner.run()` method**
After each training step, log GPU/CPU utilization:
```python
import psutil

def log_system_metrics():
    """Logs GPU and CPU usage every epoch."""
    gpu_utilization = [torch.cuda.memory_reserved(i) / 1e9 for i in range(torch.cuda.device_count())]
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    wandb.log({
        "GPU Usage (GB)": gpu_utilization,
        "CPU Usage (%)": cpu_usage,
        "RAM Usage (%)": ram_usage
    })

if self.args.stage in ['train', 'train-test']:
    for epoch in range(args.model_max_epochs):
        self.trainer.fit(self.model_module, datamodule=self.data_module)
        log_system_metrics()  # Log system usage at the end of each epoch

    if self.args.stage == 'train-test':
        self.trainer.test(self.model_module, datamodule=self.data_module)
elif self.args.stage == 'test':
    if args.net != 'zf':  # zero-filled should not load state dict
        ckpt = torch.load(args.test_ckpt_dir)
        self.model_module.load_state_dict(ckpt["state_dict"], strict=False)
    self.trainer.test(self.model_module, datamodule=self.data_module)
```

---

### **4. Verify Slurm Allocated Resources Correctly**
In **your Slurm job script**, make sure you request enough **GPUs and CPUs**:
```bash
#SBATCH --gres=gpu:4       # Allocates 4 GPUs
#SBATCH --cpus-per-task=16  # Allocates 16 CPU cores
#SBATCH --mem=64G          # Allocates 64GB RAM
```
In your script, print:
```python
print(f"CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}")
```
This ensures **your job is using the correct GPUs** allocated by Slurm.

---

### **✅ Summary of Changes**
| **Modification** | **Purpose** |
|-----------------|------------|
| `wandb.init(monitor_gym=True)` | Enables system metrics tracking |
| `wandb.config.update({...})` | Logs GPU/CPU details at startup |
| `log_system_metrics()` | Logs real-time GPU/CPU utilization |
| `print(f"CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}")` | Verifies Slurm-assigned GPUs |

🚀 **Now WandB will track your system performance!** You’ll see **live GPU, CPU, and RAM usage** in your **WandB dashboard**. Let me know if you need further tweaks!
