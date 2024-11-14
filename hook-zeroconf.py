from PyInstaller.utils.hooks import collect_submodules

# Collect all submodules of zeroconf
hiddenimports = collect_submodules('zeroconf')
