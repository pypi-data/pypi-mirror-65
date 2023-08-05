# Sharpify
### Sharpify turns the attribute routing of the Flask framework, into the Conventional routing of Asp.Net


**Versions:**
0.1.3: Updated README.md


**DISCLAIMER:**  
I don't know whether or not this works in a production environment, since i am only using this for school projects, to make my development easier. I have no experience with blueprints, so i don't know if this package is making scaleablity any better, and there is probably alot of edgecases that is not being handled.

**SETUP**  
After installing the package, you need a folder structure like this:  
- Projectfolder  
- - app folder  
- - - controllers folder **Important**  
- - - templates folder **Important**  
- - venv  
- - etc..

- In the controllers folder, you make one .py file per controller. Ex: ExampleController.py
- Within this pythone file, you make ONE class, with the same name as the file: Ex: class ExampleController():
- Make sure to import the "View" class, the "httpGet" & "httpPost" decorators (only ones supported right now, but can easily be modified by yourselves)
- You can then define an action / method to handle a endpoint

@httpGet  
def Index(id:int=None):  
    name = "Peter";  
    return View(name=name);  

this will create the following endpoints:  
- url/Example/Index/
- url/Example/Index/<int:id>

It takes the name of the class and strips the "Controller" part, leaving "Example", and then it takes the function name "Index", and then it looks for any parameters and whether or not this parameter is optional.
Since python does not have function overloading like C#, you have to handle both the case of the user setting the arguement, and the user leaving it empty. 

**Returning the correct view / template**  
return View(**kwargs), when this object is created, it will look at the class name its created in, aswell as the function name. It will then look in your templates folder to find the correct .html file, and return it to the browser.

- templates  
- - example  
- - - index.html

Any object you pass down to the frontend, can be accessed normally with Jinja2.

**Enabling the routing behaviour**  
In your application init.py, after creating your Flask app object, import and call the "sharpify.use_mvc" function, pass in the app object, and the name of the controller and function you want your webapplication to default to. This will result in "/" pointing to that function.

**Using custom attributes for hrefs and form actions**  
after "use_mvc" is called, you can call "use_htmlAttributes(pathToJsFolder);", this copies a javascript file into your folder, that can be used in any html file.
In any anchor element or form element, you can simply write data-controller="Example" data-action="Index" and it will convert it at runtime, to the correct path.