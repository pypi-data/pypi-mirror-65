# ProgressBar

Let us consider a few examples explaining how to use the `ProgressBar` class from the module `progress`:

```python
from deeppy.progress import ProgressBar
from time import sleep

bar = ProgressBar(max=20, width=50, elapsed=True)

for i in range(10):
    sleep(1)
    bar.next()
    
bar.finish()
print()

for i in range(15):
    sleep(1)
    bar.next()
```
```
Out:
Processing: [#########################                         ] 50% [elapsed: 10s; ETA: 10s]
Processing: [#####################################             ] 75% [elapsed: 15s; ETA: 5s]
```

The class supports the context management protocol and can be used with the `with` statement. Alternative bar formats are also available:

```python
with ProgressBar("Charging", max=20, width=50) as bar:
    for i in range(10):
        sleep(1)
        bar.next()
print()

with ProgressBar("FillingSquares", max=20, width=50) as bar:
    for i in range(15):
        sleep(1)
        bar.next()
```
```
Out:
Processing: [█████████████████████████∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙] 50% [ETA: 10s]              
Processing: [▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▢▢▢▢▢▢▢▢▢▢▢▢▢] 75% [ETA: 5s]
```

Note that the `next` method can be replaced by the `show` method with `index` argument supplied:

```python
with ProgressBar("FillingCircles", max=20, width=50, eta=False) as bar:
    for i in range(10):
        sleep(1)
        bar.show(i + 1)
```
```
Out:
Processing: [◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯◯] 50%
```


# ProgressSpinner

The following examples explain how to use the `ProgressSpinner` class from the module `progress`:

```python
from deeppy.progress import ProgressSpinner
from time import sleep, time

spinner = ProgressSpinner()

since = time()
while True:
    # Do some work
    sleep(0.2)
    spinner.next()
    if time() - since > 5:
        break
```

Alternative spinner formats are also available:

```python
with ProgressSpinner("Pie") as spinner:
    since = time()
    while True:
        sleep(0.2)
        spinner.next()
        if time() - since > 5:
            break
print()

with ProgressSpinner("Moon") as spinner:
    since = time()
    while True:
        sleep(0.2)
        spinner.next()
        if time() - since > 5:
            break
print()

with ProgressSpinner("Pixel") as spinner:
    since = time()
    while True:
        sleep(0.2)
        spinner.next()
        if time() - since > 5:
            break
```
```
Out:
Processing: ◷
Processing: ◐
Processing: ⣷
```


# Installation

Download from PyPI:
```
pip install deep-py
```