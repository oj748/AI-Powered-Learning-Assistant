import sys
import json
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

viewer = QWebEngineView()

BASE_DIR = Path(__file__).resolve().parent

viewer_html = (
    BASE_DIR /
    "viewer.html"
)

markdown = r"""
# Markdown Test

This is **bold**.

This is *italic*.

## List

- Apple
- Banana
- Orange

## Table

| Name | Marks |
|------|------:|
| Alice | 95 |
| Bob | 87 |

## Code

```python
print("Hello World")
```

Inline equation:

$\mu = 10$

Display equation:

$x + \frac{y}{2}$

"""

def html_loaded(success):

    print("HTML Loaded:", success)

    if not success:
        return

    viewer.page().runJavaScript(
        f"renderMarkdown({json.dumps(markdown)});"
    )


viewer.loadFinished.connect(html_loaded)

viewer.load(
QUrl.fromLocalFile(
str(viewer_html)
)
)

viewer.resize(900, 700)
viewer.show()

sys.exit(app.exec())