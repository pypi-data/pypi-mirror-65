import yaml

from tinder_cli.client import TinderClient


class TinderCLI(object):
    client = TinderClient()

    COMMANDS = ('like', 'superlike', 'pass', 'info', 'teasers', 'profile')
    PROFILE_KEYS = ('bio', 'birth_date', 'gender', 'distance_mi', 'jobs', 'name', 'photos', 'instagram', 'schools')

    @classmethod
    def cmd_info(cls, session, **kwargs):
        tinder_id = kwargs['tinder_id'] if kwargs.get('tinder_id', False) else input('tinder ID: ')

        resp = cls.client.get_user(session, tinder_id)
        resp.raise_for_status()

        data = {k: v for k, v in resp.json().get('results', {}).items() if k in cls.PROFILE_KEYS}

        data.update({
            'birth_year': int(data.pop('birth_date')[:4]),
            'photos': [x['url'] for x in data['photos']],
            'gender': 'F' if data['gender'] == 1 else 'M' if data['gender'] == 0 else 'O'
        })

        if 'jobs' in data and len(data['jobs']) == 0:
            data.pop('jobs')

        if 'schools' in data and len(data['schools']) == 0:
            data.pop('schools')

        if 'instagram' in data:
            data['instagram'] = [x['image'] for x in data['instagram'].get('photos', [])]

        return yaml.dump(data)

    @classmethod
    def cmd_profile(cls, session, **kwargs):
        resp = cls.client.get_profile(session)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    @classmethod
    def cmd_teasers(cls, session, **kwargs):
        resp = cls.client.get_teasers(session)
        resp.raise_for_status()

        profiles = []

        for item in resp.json().get('data', {}).get('results', []):
            for photo in item.get('user', {}).get('photos', []):
                profiles.append({'image_id': photo['id'], 'url': photo['url']})

        return yaml.dump(profiles)

    @classmethod
    def cmd_like(cls, session, **kwargs):
        tinder_id = kwargs['tinder_id'] if kwargs.get('tinder_id', False) else input('tinder ID: ')

        resp = cls.client.like_user(session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    @classmethod
    def cmd_superlike(cls, session, **kwargs):
        tinder_id = kwargs['tinder_id'] if kwargs.get('tinder_id', False) else input('tinder ID: ')

        resp = cls.client.superlike_user(session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    @classmethod
    def cmd_pass(cls, session, **kwargs):
        tinder_id = kwargs['tinder_id'] if kwargs.get('tinder_id', False) else input('tinder ID: ')

        resp = cls.client.pass_user(session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())
