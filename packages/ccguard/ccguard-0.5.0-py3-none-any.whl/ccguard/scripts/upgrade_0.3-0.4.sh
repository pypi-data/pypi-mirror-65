[[ -d env-0.3-backup ]] || cp -dpR env env-0.3-backup
source env/bin/activate
pip install --upgrade ccguard
