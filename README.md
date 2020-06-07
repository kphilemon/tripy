# Tripy
Tripy is a trip planner that optimises the travelling route between Jakarta, Bangkok, Taipei, Hong Kong, 
Tokyo, Beijing and Seoul, where each cities has to be visited once with the least [geodesic distance](https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid) 
travelled. This is a variant of the [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) where all nodes of 
a graph have to be visited once without returning to the starting node. A modified [Held-Karp algorithm](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm)
is used.  

Tripy is also capable of optimising the travelling route based on the sentiment analysis of local economic and financial 
situation of each cities. A [nearest neighbour algorithm](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm) 
that evaluates both geodesic distance and sentiment score is utilised. The sentiment analysis is done based on the 
major economic/ financial news website for each city that are published within the last 3 months.

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
1. Clone the repository.

    ```
    git clone https://github.com/kphilemon/tripy.git
    ```
2. Go to your project root folder to setup your virtual environment. `pip install virtualenv` if you haven't already.
    ```
    cd tripy
    virtualenv venv
    ```
3. Activate your virtual environment and install all the dependencies.
    ```
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
4. Run the application.
    ```
    python -m tripy
    ```

## Workflow
To contribute, please follow the workflow below. **Only** push directly to the `master` branch if you know exactly what you're doing. Evaluate the impact of change before doing so.

1. Make sure your local master is up-to-date.

    ```
    git checkout master
    git pull origin master
    ```
2. Create a new local branch from your master branch to work on your changes.
    ```
    git checkout -b <my-feature-branch>
    ```
3. Make changes on your new branch. Add. Commit. Repeat.
    ```
    git add .
    git commit -m "A meaningful commit message"
    ```
4. When you are ready to push your branch, make sure it's up-to-date with the remote master first.
    ```
    git checkout master
    git pull origin master
    git checkout <my-feature-branch>
    git rebase master
    ```
5. Resolve conflicts if there's any using the IDE's tool. Only if you are using PyCharm.
    https://www.jetbrains.com/help/idea/resolving-conflicts.html

6. Make sure there's no more conflict and you're now ready to push your changes to the remote repository.
    ```
    git push origin <my-feature-branch>
    ```
7. Open a merge request on github to merge your branch to master.
    https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request

#### If you want to install a package, please follow the following steps:
1. Make sure you have activated your virtual environment. Else, you *will* mess up our dependencies.

    ```
    venv\Scripts\activate
    ```
2. After running the script, you will see a `(venv)` in your terminal line. This indicates that you have successfully activated the virtual environment.
   You can now install the package you want.
    ```
    pip install <any-awesome-package>
    ```
3. Finally, run the following command to make sure the `requirements.txt` is up-to-date.
    ```
    pip freeze > requirements.txt
    ```

## Coding Styles
Kindly adhere to the PEP 8 style guide: https://www.python.org/dev/peps/pep-0008/

A few key points to keep coding style consistent as possible:
- Python packages (folder with \_\_init__.py) should also have short, all-lowercase names, and no underscores.
- Modules (py files) should have short, all-lowercase names, underscores to separate words.
- Class names should use CamelCase.
- Function names should be lowercase, with words separated by underscores as necessary to improve readability.
- Variable names follow the same convention as function names.
- Use one leading underscore only for non-public methods and instance variables of a class.
- Absolute imports are recommended, as they are usually more readable and tend to be better behaved.
- Use type hints if possible https://www.python.org/dev/peps/pep-0484/