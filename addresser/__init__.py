import pkg_resources


APP = 'addresser'


def _version():
    try:
        return pkg_resources.get_distribution(APP).version
    except pkg_resources.DistributionNotFound:
        return '0.0.0'
