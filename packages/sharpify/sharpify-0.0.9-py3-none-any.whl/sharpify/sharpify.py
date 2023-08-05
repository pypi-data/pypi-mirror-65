import sys;
import inspect;
import ast;
import pkgutil;
from pathlib import Path;
from importlib import import_module;

from flask import Flask, render_template;

#region UTILITY METHODS

# Copy sharpify.js to static folder
def use_htmlAttributes(staticFolderName:str = "static/js"):

    """
    Copies the sharpify.js file, to your static folder.
    Allows the usage of "data-controller" & "data-action" attributes in ANCHOR & FORM elements, to route hrefs and actions.
    - Relative path to your static folder, and whatever sub folder you are storing your .js files in.
    - Path will be combined with the path to the module, where this function is being called from.
    - Example usage: <script src="{{ url_for('static',filename='js/sharpify.js') }}"></script>
    """

    # Filter the input
    if staticFolderName[0] == "/":
        staticFolderName = staticFolderName.replace("/", "", 1);

    fileContent = "";

    with open(Path(__file__).parent.joinpath("sharpify.js"), "r") as file:
        fileContent = file.read();
    
    fi = inspect.stack()[1];
    mod = inspect.getmodule(fi[0]);
    path = Path(mod.__file__).parent.joinpath(staticFolderName).joinpath("sharpify.js");
    print(path);

    with open(path, "w") as file:
        file.write(fileContent);

# Replace first letter of a string with the same letter, in Uppercase
## Used to make sure that lower case Class names, and lower case Function names, get Uppercased for the generated routes
def string_flUppercase(value: str):
    firstLetter = value[0];
    return value.replace(firstLetter, firstLetter.upper(), 1);

def string_flLowercase(value: str):
    firstLetter = value[0];
    return value.replace(firstLetter, firstLetter.lower(), 1);

#endregion


#region ROUTING METHODS

    # Get all functions from a class, and their respective decorators
def get_decorators(cls):
  target = cls
  decorators = {}

  def visit_FunctionDef(node):
    decorators[node.name] = []
    for n in node.decorator_list:
      name = ''
      if isinstance(n, ast.Call):
          name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
      else:
          name = n.attr if isinstance(n, ast.Attribute) else n.id

      decorators[node.name].append(name)

  node_iter = ast.NodeVisitor()
  node_iter.visit_FunctionDef = visit_FunctionDef
  node_iter.visit(ast.parse(inspect.getsource(target)))
  return decorators;

def getFunctionArguements(func):
  full_args = inspect.getfullargspec(func);
  # 0 = args <list>
  # 6 = annotations <dict>
  print(full_args);
  
  routeArguements = "/";

  if bool(full_args[6]) == True: # Not empty
    for key in full_args[6]:
      #print("KEY: " + key);
      #print("VALUE: " + full_args[6][key].__name__);
      routeArguements += "<" + full_args[6][key].__name__ + ":" + key + ">" + "/";
  
  return routeArguements;

def getFunctionMethods(funcName:str, classDecorators:dict):
    methodList = [];
    for deco in classDecorators[funcName]:
        if deco == "httpGet":
            methodList.append("GET");
        if deco == "httpPost":
            methodList.append("POST");

    return methodList;

def use_mvc(flask_app: Flask, default_controller: str, default_action: str):

    """ 
    Definition:
      PYTHON FILES:
      - Create a folder named "Controllers" in your application root
        - Make sure this folder is located, within the module in which you call this function from.
      - Within this folder, name your controller files - "exampleController.py" OR "ExampleController.py"
      - Within those files, have one class per file, named - "class exampleController():" OR "class ExampleController():" 
      - Within those classes, define functions without the "self" arguement - "def Index():"
      - Within those functions, do your logic, and then return a - "View()" object
        - This object will search your default flask "templates" folder, for a ".html" file that matches the names of the controller class it is being called from (minus the "Controller"), and then function name it is being called from
        - templates -> example (folder) -> index.html
        - The View() object, is a wrapper around "render_templates" so you can pass in arguements, you want to send forward to your front-end - View(data = _data) etc.
      - You can decorate controller functions with - "@httpGet" & "@httpPost", to allow one or multiple methods for your route
      - You can add single arguements to your controller functions. 
        - If you default this arguement, it will become an optional arguement, and thus create two routes. One route without the arguement, and one with. 
      
      HTML FILES:
      - For anchor elements & form elements, use attributes - "data-controller" & "data-action" 
        - This: <a data-controller="Example" data-action="Index" />
        - Becomes: <a href="/Example/Index/" />
    """

    # Find the module name, in which this function is called
    # Use this name to find the "controllers" folder
    stk = inspect.stack()[1];
    mod = inspect.getmodule(stk[0]);

    for (_, name, _) in pkgutil.iter_modules([Path(mod.__file__).parent]):

        if(name == "controllers"):
            
            for(_, fileName, _) in pkgutil.iter_modules([Path(mod.__file__).parent.joinpath(name)]):
                #print("Imported fileName: " + fileName);
                try:
                    projectRootName = Path(mod.__file__).parent.name; # ex. app
                    packageName = projectRootName + "." + name; # ex. app.controller
                    imported_module = import_module("." + fileName, package = packageName);
                except ImportError as err:
                    print("Error: ", err);

                for i in dir(imported_module):
                    attribute = getattr(imported_module, i);
                    if(inspect.isclass(attribute) and "Controller" in attribute.__name__):
                        print("ATTRIBUTE: " + attribute.__name__); # Controller
                        classDecos = get_decorators(attribute);    # Dictionary: KEY = FunctionName, VALUE = List(decorators)

                        func_list = inspect.getmembers(attribute, inspect.isfunction)
                        for func in func_list:
                            print("---" + func[0] + "----");

                            controllerName = string_flUppercase(attribute.__name__);
                            funcName = string_flUppercase(func[0]);
                            methods = getFunctionMethods(funcName, classDecos);
                            routeArguements = getFunctionArguements(func[1]);
                            print(methods);



                            # Route State Checks
                            isDefaultRoute = attribute.__name__ == default_controller and func[0] == default_action;
                            isDefaultAction = func[0] == default_action;
                            hasArguements = len(inspect.getfullargspec(func[1]).args) > 0;
                            isOptionalArgs = inspect.getfullargspec(func[1]).defaults != None;
                            print("IsDefaultRoute: " + str(isDefaultRoute));
                            print("IsDefaultAction: " + str(isDefaultAction));
                            print("HasArguements: " + str(hasArguements));
                            print("IsOptionalArgs: " + str(isOptionalArgs));


                            if isDefaultRoute:
                                flask_app.add_url_rule("/", "default_route_" + funcName, func[1], methods=methods);
                                print("GENERATE DEFAULT ROUTE: " + "/");
                                print("MAPS TO: " + attribute.__name__.replace("Controller", "") + "/" + funcName + "/");
                            

                            if isDefaultAction:
                                if hasArguements:
                                    rule = "/" + controllerName.replace("Controller", "") + routeArguements;
                                    endpoint = attribute.__name__ + "_" + func[0] + "_" + "default_args";
                                    flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                    print("GENERATED DEFAULT ACTION ROUTE /w ARG: " + rule);
                                    
                                    if isOptionalArgs:
                                        rule = "/" + controllerName.replace("Controller", "") + "/";
                                        endpoint = attribute.__name__ + "_" + func[0] + "_" + "default_optional";
                                        flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                        print("GENERATED DEFAULT ACTION ROUTE /w OPTIONAL ARG: " + rule);
                                else:
                                    rule = "/" + controllerName.replace("Controller", "") + "/";
                                    endpoint = attribute.__name__ + "_" + func[0] + "_" + "default";
                                    flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                    print("GENERATED DEFAULT ACTION ROUTE: " + rule);

                            else:
                                if hasArguements:
                                    rule = "/" + controllerName.replace("Controller", "") + "/" + funcName + routeArguements;
                                    endpoint = attribute.__name__ + "_" + func[0] + "_" + "args";
                                    flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                    print("GENERATED ROUTE /w ARG: " + rule);

                                    if isOptionalArgs:
                                        rule = "/" + controllerName.replace("Controller", "") + "/" + funcName;
                                        endpoint = attribute.__name__ + "_" + func[0] + "_" + "optional";
                                        flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                        print("GENERATED ROUTE /w OPTIONAL ARG: " + rule);
                                else:
                                    rule = "/" + controllerName.replace("Controller", "") + "/" + funcName;
                                    endpoint = attribute.__name__ + "_" + func[0] + "_" + "optional";
                                    flask_app.add_url_rule(rule, endpoint, func[1], methods=methods);
                                    print("GENERATED ROUTE: " + rule);

#endregion


#region HTTP METHOD DECORATORS

def httpGet(f):
    def decorator(*args, **kwargs):
        print("httpGet");
        return f(*args, **kwargs);
    
    decorator.__signature__ = inspect.signature(f); # This line will preserve the original signature of "f", instead of replacing it with (*args, **kwargs)

    return decorator;

def httpPost(f):
    def decorator(*args, **kwargs):
        print("httpPost");
        return f(*args, **kwargs);

    decorator.__signature__ = inspect.signature(f); # This line will preserve the original signature of "f", instead of replacing it with (*args, **kwargs)

    return decorator;

#endregion


#region CLASSES

class View(str):
    
    def __new__(cls, **context):
        frame = inspect.currentframe()
        frameInfoList = str(frame.f_back).split(",");
        

        # index(1) = file
        # index(3) = function

        # Name of calling controller
        file = frameInfoList[1].split("\\\\");                      # Split the frame info, that contains the fileName.py of where the View were instantiated
        file = file[file.__len__() - 1];                            # Save the last item in the split, as this contains our fileName
        file = string_flLowercase(file);                            # Make sure that the first letter of the fileName is Upper / Lower, so it matches the class name / html directory folder name - within the file
        fileName = file.split(".")[0];                              # Split it again, to remove the ".py" extension
        controllerName = fileName.replace("Controller", "");
        print("FILE: " + fileName);
        print("CONTROLLER: " + controllerName);

        # Name of calling function / action
        func = frameInfoList[3].replace("'", "", 2).replace("code", "", 1).replace(">", "", 1).strip();
        func = string_flLowercase(func);
        print("FUNCTION: " + func);

        # Fetch the correct html
        html = render_template(controllerName + "/" + func + ".html", **context);                               # Folder name & .html name is not case sensitive when giving the path, so no need to alter those
        return super(View, cls).__new__(cls, html);

#endregion