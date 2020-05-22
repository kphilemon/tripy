# Tripy
Tripy is a sentiment based trip planner. It optimises the travel route between Jakarta, Bangkok, Taipei, Hong Kong, Tokyo, Beijing and Seoul
based on the sentiment analysis of local economic and financial situation as well as the shortest travelling path between the cities.

This project utilises Dijkstra's algorithm as SPF algorithm and perform sentiment analysis on major economic/ financial news website for each city
that are published within the last 3 months.

## Getting started
1. Clone the repository.

    ```
    git clone https://github.com/kphilemon/tripy.git
    ```
2. Go to your project root folder to setup your virtual environment. `pip install virtualenv` if you haven't already.
    ```
    cd tripy
    virtualenv venv
    ```
3. Activate your virtual environment.
    ```
    venv\Scripts\activate
    ```
4. Install all the dependencies.
    ```
    pip install -r requirements.txt
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


####If you want to install a package, please follow the following steps:
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