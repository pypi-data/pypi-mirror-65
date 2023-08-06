from setuptools import setup, find_packages

setup(
    name="iotile_support_firm_env_1",
    packages=find_packages(include=["iotile_support_firm_env_1.*", "iotile_support_firm_env_1"]),
    version="1.2.2",
    install_requires=['iotile-core ~= 5.0'],
    entry_points={'iotile.proxy': ['env_proxy = iotile_support_firm_env_1.env_proxy'], 'iotile.emulated_tile': ['envbsl_1 = iotile_support_firm_env_1.envbsl_1'], 'iotile.virtual_device': ['dev_envbsl_1 = iotile_support_firm_env_1.dev_envbsl_1']},
    include_package_data=True,
    author="Arch",
    author_email="info@arch-iot.com"
)