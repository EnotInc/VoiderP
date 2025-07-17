from PyQt6.QtGui import QFont

THEMES = {
    "light":"""
        background-color: #e0f0ff;
        color: #000000;
    """,
    "dark":"""
        background-color: #2d2d2d;
        color: #e0e0e0;    
    """,
    "console":"""
        background-color: #000000;
        color: #ffffff; 
    """
}



def apply_theme(window, theme_name):
    if theme_name not in THEMES:
        theme_name = "dark"
    
    theme = THEMES[theme_name]

    font = QFont()
    font.setFamily("Consolas")
    font.setPointSize(16)
    font.setStyleHint(QFont.StyleHint.Monospace)
    
    window.setFont(font)
    window.setStyleSheet(theme)
