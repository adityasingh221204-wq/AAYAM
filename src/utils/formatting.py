"""
AAYAM - Number, Currency and Metric Formatting
Converts financial numbers to Indian numbering format (Lakhs, Crores, INR).
"""

def format_inr(value: float | int | None, show_decimals: bool = False) -> str:
    """Format numeric amount into Indian Rupee format (e.g. ₹1,25,000)."""
    if value is None:
        return "₹0"
    try:
        val = float(value)
        sign = "-" if val < 0 else ""
        val = abs(val)
        
        parts = f"{val:.2f}".split(".")
        integer_part = parts[0]
        decimal_part = parts[1] if show_decimals else ""
        
        if len(integer_part) <= 3:
            res = integer_part
        else:
            last_three = integer_part[-3:]
            remaining = integer_part[:-3]
            # Group in 2s
            grouped = []
            while len(remaining) > 2:
                grouped.insert(0, remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                grouped.insert(0, remaining)
            res = ",".join(grouped) + "," + last_three
            
        final_str = f"{sign}₹{res}"
        if show_decimals and decimal_part:
            final_str += f".{decimal_part}"
        return final_str
    except Exception:
        return f"₹{value}"


def format_lakh_crore(value_crores: float | int | None) -> str:
    """Format large crores value into readable string."""
    if value_crores is None:
        return "—"
    try:
        val = float(value_crores)
        if val >= 100000:
            return f"₹{val/100000:.2f} Lakh Cr"
        elif val >= 1000:
            return f"₹{val:.1f} Cr"
        else:
            return f"₹{val:.2f} Cr"
    except Exception:
        return str(value_crores)


def format_pct(value: float | int | None, decimals: int = 1) -> str:
    """Format percentage value."""
    if value is None:
        return "0.0%"
    try:
        return f"{float(value):.{decimals}f}%"
    except Exception:
        return f"{value}%"
