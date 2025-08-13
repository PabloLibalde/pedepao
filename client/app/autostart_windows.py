r"""
Registra o app para iniciar com o Windows (HKCU\...\Run).
Ignora silenciosamente fora do Windows.
"""
import sys, os
if sys.platform.startswith("win"):
    try:
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "PedePao", 0, winreg.REG_SZ, exe_path)
    except Exception:
        pass
