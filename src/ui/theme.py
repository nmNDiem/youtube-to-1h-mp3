"""
Modern color theme for the app
"""

# Modern dark theme with vibrant accents
COLORS = {
    # Background colors - Deep blue/gray tones for a premium feel
    'bg_primary': '#0f172a',      # Slate 900
    'bg_secondary': '#1e293b',    # Slate 800 (Cards)
    'bg_tertiary': '#334155',     # Slate 700 (Inputs/Hovers)
    'bg_overlay': 'rgba(0, 0, 0, 0.5)', 
    
    # Accent colors (Vibrant Violet/Indigo)
    'accent_primary': '#6366f1',  # Indigo 500
    'accent_secondary': '#818cf8',# Indigo 400
    'accent_hover': '#4f46e5',    # Indigo 600
    'accent_disabled': '#475569', # Slate 600
    
    # Text colors
    'text_primary': '#f8fafc',    # Slate 50
    'text_secondary': '#cbd5e1',  # Slate 300
    'text_muted': '#94a3b8',      # Slate 400
    'text_inverse': '#0f172a',    # Slate 900
    
    # Status colors
    'success': '#10b981',         # Emerald 500
    'error': '#ef4444',           # Red 500
    'warning': '#f59e0b',         # Amber 500
    'info': '#3b82f6',            # Blue 500
    
    # Border and divider
    'border': '#334155',          # Slate 700
    'divider': '#1e293b',         # Slate 800
}

# Type scale - Slightly reduced for compactness
FONTS = {
    'heading': ('Segoe UI', 22, 'bold'),
    'subheading': ('Segoe UI', 18, 'bold'),
    'body': ('Segoe UI', 15),
    'body_bold': ('Segoe UI', 15, 'bold'),
    'body_large': ('Segoe UI', 18),
    'caption': ('Segoe UI', 13),
    'small': ('Segoe UI', 12),
    'monospace': ('Consolas', 15),
}

# Spacing system - Aggressively reduced for compact UI
SPACING = {
    'xs': 2,
    'sm': 4,      # Was 6
    'md': 8,      # Was 10
    'lg': 16,     # Was 16
    'xl': 20,     # Was 24
    'xxl': 32,
}

# Border radius
RADIUS = {
    'sm': 4,
    'md': 6,
    'lg': 8,
    'xl': 12,
    'full': 100,
}
