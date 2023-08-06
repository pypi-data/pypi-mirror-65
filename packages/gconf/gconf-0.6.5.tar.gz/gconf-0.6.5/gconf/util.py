from collections.abc import Mapping


def update(d: dict, u: dict):
	for k, v in u.items():
		if isinstance(v, Mapping):
			d[k] = update(d.get(k, {}), v)
		else:
			d[k] = v
	return d
