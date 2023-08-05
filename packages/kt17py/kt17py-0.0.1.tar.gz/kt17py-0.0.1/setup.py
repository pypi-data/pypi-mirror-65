import setuptools


class NoNumpy(Exception):
    pass


try:
    from numpy.distutils.core import Extension
    from numpy.distutils.core import setup
except ImportError:
    raise NoNumpy('Numpy needs to be installed for extensions to be compiled.')


if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(name="kt17py",
          version="0.0.1",
          author="Inaki Ortiz de Landaluce",
          author_email="inaki.ortizdelandaluce@gmail.com",
          description="A Python wrapper to the FORTRAN code for the KT17 dynamic magnetic field model for "
                      "Mercury's magnetosphere",
          long_description=long_description,
          long_description_content_type="text/markdown",
          url="https://github.com/inaki-ortizdelandaluce/kt17py",
          packages=setuptools.find_packages(),
          ext_modules=[Extension(name='kt17py._kt17',
                                 sources=['kt17py/_kt17.pyf', 'kt17py/_kt17.f90'])],
          license="MIT",
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
          ],
          install_requires=['numpy>=1.16'],
          python_requires='>=2.7',
          )
