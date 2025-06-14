def format_rupiah(amount):
    """Format angka menjadi format rupiah"""
    return f"Rp {amount:,.0f}".replace(',', '.')

def hitung_total_belanja(items):
    """Menghitung total belanja dari list items
    
    Args:
        items (list): List of dict dengan keys 'harga' dan 'quantity'
    
    Returns:
        int: Total harga
    """
    total = 0
    for item in items:
        total += item.get('harga', 0) * item.get('quantity', 0)
    return total

def format_ukuran(ukuran_list):
    """Format list ukuran menjadi string yang rapi"""
    return ', '.join([str(u) for u in sorted(ukuran_list)])

def validate_ukuran(ukuran, available_sizes):
    """Validasi apakah ukuran tersedia"""
    return ukuran in available_sizes