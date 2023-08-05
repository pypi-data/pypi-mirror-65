# WidgetMark

The goal of this project is to create a Benchmarking Framework,
which allows you to test the performance of a specific GUI Widget.
The Framework is written as part of my bachelor's thesis.

![alt text](documentation/screenshot.png "Screenshot")

## For users

### How do I install it?

Installation is very simple, since all dependencies are documented in 
[setup.py](setup.py). The following command will provide you with the
minimal dependencies to start writing your own benchmark use cases.
```
python -m pip install -e .
```

### How can I try it out?

There are a few example implementations, that you can run. They can be located
the [examples folder](examples). These contain different use cases, which
are ready to run. 

```
cd path/to/widgetmark
pip install -e .
widgetmark examples
```

To create profiles of the Use Cases you are running and view them using the profile viewer [snakeviz](https://jiffyclub.github.io/snakeviz/) in your browser, run:

```
widgetmark --profile --visualize examples
```

To visualize already created Profiles, you can use [snakeviz](https://jiffyclub.github.io/snakeviz/) directly:

```
snakeviz folder/with/profile_files
```

It is also possible to run only specific Use Cases, e.g. for running the Label Example Use Case which tests the setText operation, run:
```
widgetmark examples/bench_label.py::SetTextUseCase
```

To see more options for the command line interface, run:

```
widgetmark --help
```


### How can I create my own Use Cases?

Widgetmark can be used with different GUI Backends, but currently only Qt is
supported. Benchmarks are python files named "bench_*.py" which contain a set
of use cases. Each use Case is a class derived from the abstract class
[`widgetmark.UseCase`](widgetmark/base/benchmark.py). Each Use Case defines
which widget it wants to use, the operation it want's to be investigated, and
a set of other properties which define f.e. what Frame Rate should be achieved.

To define your own Benchmarks, you simply have to:
1. Create a file **"bench_<foo>.py"**.
2. Add a class derived from [`widgetmark.UseCase`](widgetmark/base/benchmark.py) 
   and implement all functions.
   (Tip: Properties can be simply implemented as class attributes, this will
         save you a few lines of code, for inspiration have a look at the
         [examples folder](examples))
3. Run widgetmark.

### What are the results?

Widgetmark does measure / gather the following things for each use case:

- **Frame Rate / Redraw costs:** How often per second can the widget handle specific operations?
- **Profile:** Detailed listing of the costs of called functions, which allows to discover bottle necks in code.
