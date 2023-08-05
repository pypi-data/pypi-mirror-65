![](pics/slurm.jpg)

# Slurm

**Under Development**


```python
from slurm import storage

yaml = storage.read("file.yaml")
json = storage.read("file.json")
json = storage.read("file", "json")


data = [1,2,3,4]
storage.write("bob.json", data)
storage.write("guess", data, "yml")
```
