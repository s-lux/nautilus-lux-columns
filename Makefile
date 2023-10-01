user-install:
	rm -rf __pycache__ || true
	python3 -OO -m compileall lux-columns.py
	install -dm755 $(HOME)/.local/share/nautilus-python/extensions/__pycache__/
	install -m755 lux-columns.py $(HOME)/.local/share/nautilus-python/extensions/
	test -f __pycache__/lux-columns.*.pyc && install -m755 __pycache__/lux-columns.*.pyc $(HOME)/.local/share/nautilus-python/extensions/__pycache__/ || true
	rm -rf __pycache__ || true

system-install:
	rm -rf __pycache__ || true
	python3 -OO -m compileall lux-columns.py
	install -dm755 /usr/share/nautilus-python/extensions/__pycache__/
	install -m755 lux-columns.py /usr/share/nautilus-python/extensions/
	test -f __pycache__/lux-columns.*.pyc && install -m755 __pycache__/lux-columns.*.pyc /usr/share/nautilus-python/extensions/__pycache__/ || true
	rm -rf __pycache__ || true

user-remove:
	rm $(HOME)/.local/share/nautilus-python/extensions/lux-columns.py || true
	rm $(HOME)/.local/share/nautilus-python/extensions/__pycache__/lux-columns.*.pyc || true
	rm -rf __pycache__ || true

system-remove:
	rm /usr/share/nautilus-python/extensions/lux-columns.py || true
	rm /usr/share/nautilus-python/extensions/__pycache__/lux-columns.*.pyc || true
	rm -rf __pycache__ || true
