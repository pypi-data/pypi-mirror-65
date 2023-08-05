## **xvgpy**
### A scriptable vector graphics library for Python

---
### **Install** 
```
python3 -m pip install xvg
```
(See: [PyPI package](https://pypi.org/project/xvg/))

---
### **Example** 
```python
from xvg.application import Engine
from xvg.renderers import SVGRenderer

Engine(SVGRenderer()).processFile('image.xvg')
```
(See: [XVGPY Index](https://lrgstu.github.io/xvgpy/))

(See: [XVGPY Tests](./tests))

---