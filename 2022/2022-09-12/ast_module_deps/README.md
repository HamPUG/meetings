# AST Module dependencies

Determines dependencies between modules using the `import` statements and generates a 
[graphviz](https://graphviz.org/) file from it (directed graph).

* clone example code base

  ```bash
  git clone https://github.com/fracpete/python-weka-wrapper3.git
  ```

* generate dependency graph

  ```bash
  python3 module_deps.py \
    -s ./python-weka-wrapper3/python/ \
    -o ./pww3.dot \
    -i "weka.*" \
    -e "weka.flow.*" \
    -v
  ```

* generate PNG from graph

  ```bash
  dot -T png -o pww3.png pww3.dot
  ```

* view PNG

  ```bash
  xdg-open pww3.png
  ```

