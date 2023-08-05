#!/usr/bin/python3

import json

GLOBAL_DEFAULTS = {
	'cat': 'dev-python',
	'refresh_interval': None,
	'python_compat': 'python3_{6,7,8}'
}

async def generate(hub, **pkginfo):
	assert 'python_compat' in pkginfo
	if 'pypi_name' in pkginfo:
		pypi_name = pkginfo['pypi_name']
	else:
		pypi_name = pkginfo['name']

	json_data = await hub.pkgtools.fetch.get_page(f'https://pypi.org/pypi/{pypi_name}/json', refresh_interval=pkginfo['refresh_interval'])
	json_dict = json.loads(json_data)

	if 'versions' not in pkginfo:
		versions = [json_dict['info']['version']] # generate latest version
	else:
		versions = pkginfo['versions']

	for version in versions:
		artifact_url = None
		for artifact in json_dict['releases'][version]:
			if artifact['packagetype'] == 'sdist':
				artifact_url = artifact['url']
				break
		assert artifact_url is not None
		ebuild = hub.pkgtools.ebuild.BreezyBuild(
			**pkginfo,
			version=version,
			artifacts=[
				hub.pkgtools.ebuild.Artifact(url=artifact_url)
			]
		)
		ebuild.push()

# vim: ts=4 sw=4 noet
