from setuptools import setup


setup(name='hd_gliomouse',
      version='1.0',
      packages=["hd_gliomouse"],
      description='Tool for brain tumor segmentation in mice. This is the result of a joint project between the Department of '
                  'Neuroradiology at the Heidelberg University Hospital and the Division of Medical Image Computing at '
                  'the German Cancer Research Center (DKFZ). See readme.md for more information',
      url='https://github.com/NeuroAI-HD/HD-GLIOMOUSE',
      python_requires='>=3.5',
      author='Fabian Isensee',
      author_email='f.isensee@dkfz.de',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
          'torch',
          'nnunet>1.0', 'batchgenerators'
      ],
      entry_points={
          'console_scripts': [
                'hd_gliomouse_predict = hd_gliomouse.hd_gliomouse_predict:main',
                'hd_gliomouse_predict_folder = hd_gliomouse.hd_gliomouse_predict_folder:main',
        ],
      },
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Operating System :: Unix'
      ]
      )

