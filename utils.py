import os
from tkinter import ttk, FLAT

# Colors
BG_DARK = "#0F172A"       # slate-900
BG_CARD = "#1E293B"       # slate-800
FG_LIGHT = "#F8FAFC"      # slate-50
FG_MUTED = "#94A3B8"      # slate-400

COLOR_PRIMARY = "#6366F1"        # Indigo-500
COLOR_PRIMARY_HOVER = "#4F46E5"  # Indigo-600
COLOR_SUCCESS = "#10B981"        # Emerald-500
COLOR_SUCCESS_HOVER = "#059669"  # Emerald-600
COLOR_DANGER = "#EF4444"         # Rose-500
COLOR_DANGER_HOVER = "#DC2626"   # Rose-600
COLOR_WARNING = "#F59E0B"        # Amber-500
COLOR_WARNING_HOVER = "#D97706"  # Amber-600
COLOR_INFO = "#3B82F6"           # Blue-500
COLOR_INFO_HOVER = "#2563EB"     # Blue-600

COLOR_ENTRY_BG = "#334155"       # slate-700
COLOR_ENTRY_FG = "#FFFFFF"
COLOR_ENTRY_BORDER = "#475569"   # slate-600
COLOR_ENTRY_BORDER_FOCUS = "#6366F1" # Indigo-500

# Fonts
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 16, "bold")
FONT_BODY_BOLD = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_FOOTER = ("Segoe UI", 10)

# Rebranding Info
COMPANY_NAME = "Zynox Tech"
WEBSITE = "https://zynoxtech.site"
EMAIL = "hello@zynoxtech.site"
LOCATION = "Abbottabad, Pakistan"
DEV_TEXT = f"IMS - Inventory Management System | Developed by {COMPANY_NAME}\nWebsite: {WEBSITE} | Email: {EMAIL} | Location: {LOCATION}"
DEV_FOOTER = f"Developed by {COMPANY_NAME} | Website: {WEBSITE} | Email: {EMAIL}"

def resolve_path(relative_path):
    """
    Resolves file paths robustly to work across different run contexts and directories.
    Handles 'Inventory-Management-System/' prefix if present.
    """
    if not relative_path:
        return ""
    
    # 1. Normalize separators
    normalized_path = relative_path.replace("\\", "/")
    
    # 2. Get base directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check directly relative to base_dir
    p_direct = os.path.join(base_dir, normalized_path)
    if os.path.exists(p_direct):
        return p_direct
        
    # Check by stripping the 'Inventory-Management-System/' prefix if it's there
    prefix = "Inventory-Management-System/"
    if normalized_path.startswith(prefix):
        stripped = normalized_path[len(prefix):]
        p_stripped = os.path.join(base_dir, stripped)
        if os.path.exists(p_stripped):
            return p_stripped
            
        # Try stripped path relative to current working directory
        if os.path.exists(stripped):
            return os.path.abspath(stripped)
            
    # Try as-is relative to current working directory
    if os.path.exists(normalized_path):
        return os.path.abspath(normalized_path)
        
    # Fallback to direct path
    return p_direct

def style_button(btn, bg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, fg_color="white"):
    """Styles a standard Tkinter Button to have a clean, modern flat look with hover animations."""
    btn.config(
        bg=bg_color,
        fg=fg_color,
        activebackground=hover_color,
        activeforeground=fg_color,
        bd=0,
        relief=FLAT,
        font=FONT_BODY_BOLD,
        cursor="hand2"
    )
    # Hover effects
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

def style_entry(entry):
    """Styles standard Tkinter Entry widgets to look sleek, flat and dark themed with subtle border highlight."""
    entry.config(
        bg=COLOR_ENTRY_BG,
        fg=COLOR_ENTRY_FG,
        insertbackground="white",
        bd=0,
        highlightthickness=1,
        highlightbackground=COLOR_ENTRY_BORDER,
        highlightcolor=COLOR_ENTRY_BORDER_FOCUS,
        font=FONT_BODY
    )

def style_text(txt):
    """Styles standard Tkinter Text widgets to look sleek, flat and dark themed."""
    txt.config(
        bg=COLOR_ENTRY_BG,
        fg=COLOR_ENTRY_FG,
        insertbackground="white",
        bd=0,
        highlightthickness=1,
        highlightbackground=COLOR_ENTRY_BORDER,
        highlightcolor=COLOR_ENTRY_BORDER_FOCUS,
        font=FONT_BODY
    )

def style_label(lbl, font=FONT_BODY, bg=BG_CARD, fg=FG_LIGHT):
    """Styles standard Tkinter Label widgets."""
    lbl.config(bg=bg, fg=fg, font=font)

def style_lf(lf, font=FONT_BODY_BOLD, bg=BG_DARK, fg=COLOR_PRIMARY):
    """Styles standard Tkinter LabelFrame widgets."""
    lf.config(
        bg=bg,
        fg=fg,
        font=font,
        bd=2,
        relief="groove"
    )

def apply_treeview_theme():
    """Sets up a unified modern dark style for ttk widgets (Treeview, Scrollbar, Combobox)."""
    style = ttk.Style()
    # Check if theme is already customized to avoid duplicate warnings
    try:
        style.theme_use('clam')
    except Exception:
        pass
    
    # Treeview styles
    style.configure(
        "Treeview",
        background=BG_CARD,
        foreground=FG_LIGHT,
        fieldbackground=BG_CARD,
        rowheight=28,
        gridcolor="#2D3748",
        font=FONT_BODY
    )
    style.map(
        "Treeview",
        background=[('selected', COLOR_PRIMARY)],
        foreground=[('selected', 'white')]
    )
    
    # Treeview Headings styles
    style.configure(
        "Treeview.Heading",
        background=COLOR_ENTRY_BG,
        foreground=FG_LIGHT,
        relief="flat",
        font=FONT_BODY_BOLD
    )
    style.map(
        "Treeview.Heading",
        background=[('active', COLOR_ENTRY_BORDER)]
    )
    
    # Combobox style
    style.configure(
        "TCombobox",
        fieldbackground=COLOR_ENTRY_BG,
        background=COLOR_ENTRY_BORDER,
        foreground=COLOR_ENTRY_FG,
        arrowcolor="white",
        font=FONT_BODY
    )
    style.map(
        "TCombobox",
        fieldbackground=[('readonly', COLOR_ENTRY_BG)],
        selectbackground=[('readonly', COLOR_ENTRY_BG)],
        selectforeground=[('readonly', COLOR_ENTRY_FG)]
    )

    # Scrollbar style
    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=COLOR_ENTRY_BORDER,
        troughcolor=BG_DARK,
        bordercolor=BG_DARK,
        arrowcolor="white"
    )
    style.configure(
        "Horizontal.TScrollbar",
        gripcount=0,
        background=COLOR_ENTRY_BORDER,
        troughcolor=BG_DARK,
        bordercolor=BG_DARK,
        arrowcolor="white"
    )
