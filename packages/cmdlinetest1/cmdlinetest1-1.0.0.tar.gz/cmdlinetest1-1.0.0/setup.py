from setuptools import setup, find_packages 

setup( 

        name ='cmdlinetest1', 

        version ='1.0.0', 

        author ='Bhakti Jadhav', 

        author_email ='bhaktij910@gmail.com',  

        description ='Demo Package for CLI', 

        packages = find_packages(), 

        entry_points ={ 

            'console_scripts': [ 

                'clirest = cmdlinetest1.clirest:main'

            ] 

        }, 

        classifiers =( 

            "Programming Language :: Python :: 3", 

            "Operating System :: OS Independent", 

        ), 


        zip_safe = False
) 