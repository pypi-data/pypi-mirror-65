# core.NS - functional Python with Namespaces.

  There are hundreds, if not thousands Application Frameworks for a Python programming language. Some of them withstand a test of time, some are fairly new. Some of those frameworks are Object-Oriented, some of them …. well, most of them are based on representation of your application through objects. Application logic are represented as a cascade of methods calls and recently, with newly-found fancy for the microservices, cascade of the distributed RPC calls. In the new, distributed world, we are experiencing a strong call for the new Application Frameworks, which will bring together both local and a distributed logic in a simple, straightforward way. The way, that will at least looks familiar for may developers and the way that will not bring artificial barriers between data and code, but rather bringing data and code together, providing clear naming distinction.

  There is nothing new in this approach, which unified data and a code in application space. Because same approach was implemented in Unix decades ago. This approach is having a name: “Everything is a file”. If you are not familiar with a Unix OS, “everything is a file” means that there is only one way to deal with everything that’s it is in Unix by treating that’s everything, including application code is a file, that’s you can read, write and use according with your permissions. Every entity in Unix, well … almost every entity (but every entity in OS Plan9) do have a file name. There are API interface, defining how you can access those files and there are standards defining where you can find different elements of the OS. From a binary programs to data, configuration and a log files.

Full documentation is available at https://corens.readthedocs.io/en/latest/

## In-application filesystem

  Of course, an application is having much more simple structure than a full-sized OS. Almost everything in application space are in memory, so when we are saying, that we are implementing the same approach in core.NS as it is in Unix OS, we do not have to actually implement an in-application filesystem, which are real, “on the disk” filesystem. In the core of our Application Framework is a “virtual FS”. A way to organize our application, when each and every entity having a unique file path-like name. Can be addressed by this unique name and permitted operations can be performed with this entity, addressable by it’s name.  So, our approach is very similar to Unix OS approach, but there are differences.

  In core.NS - everything is a data, addressable by it’s path in in-memory namespace. This in-memory namespace, provides a references to a locally placed data, functions and both local and network resources. There are very important point there: current core.NS namespace implementation are in-memory structure. The rationale for that is a speed. In the future, I will provide on-disk  namespace extension.
  To make core.NS namespace familiar to a crowd, I’ve took a liberty to organize default namespace in the same way as Unix OS file system organisation. There are /bin, /sbin, /home, /etc, /usr/local/bin and the other placeholders, that you are familiar with.

## Functions

  Functions are the first-class citizens in core.NS. This means, that they support all the operations, available to other elements of the Namespace.  You can create data elements containing references to a functions as you are creating any other data elements. You can reference functional data elements, as you are referencing anything else on core.NS. So, functional fact number 1, functions are the data elements in Namespace and each function can be referenced just like any other data element, by there path. For example: /bin/id .

  But it is a bit more about a functions then meet an eye. There is no objects in core.NS and while the functions in framework are not pure, each of them having a reference to a full Namespace as a first parameter.  Functional fact number 2 - you can not take just any Python function and turn it into core.NS function, because to each function in the framework, we will pass that reference. But when ? During execution ? Would it be too mundane to pass the same thing multiple times ?

  The answer to the problem is that in Namespace, we are storing a reference to a partially evaluated function and every time that we are referencing that function, we are receiving a reference not to the function itself, but rather to a partially evaluated function, exactly as we store it.

## First steps

  As a first steps, you will be expected, that there is a guidance on how to install
and do the first try-run of the tool.

### Installation
  ```
  pip install -U corens
  ```

### ... in the beginning
  ```
  Python 3.7.4 (default, Jul  9 2019, 18:13:23)
  [Clang 10.0.1 (clang-1001.0.46.4)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>> from corens import *
  >>> ns, f, F = NS()
  >>> f("/bin/stamp")()
  1578869315.8705332
  >>>
  ```

  In this example, you are creating a namespace, alongside with partially-evaluated functions for resolving and executing functions in namespace and partially-evaluated function for exporting namespace functions into a builtin functions. Then you are resolving and executing partially-evaluated function referred as _/bin/stamp_ inside namespace. This function will return you a current timestamp.
