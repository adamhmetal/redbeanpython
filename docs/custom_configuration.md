# Configuration

As the idea of RedBeanPython is to be as **zero-config** ORM, by default, no configuration is needed.

But you can do it if you want to change the default directory/namespace and adjust it to your needs and project structure.

# Directory and namespace configuration

By default, RedBeanPython will create models in the `redbean` directory in the app's main directory and use the corresponding namespace. 

But it can be changed by calling `redbean.setup()` with `directory` and `namespace` parameters.

```python
redbean.setup(
    "postgresql+psycopg://...", 
    directory='my_module/my_redbean', 
    namespace='my_module.my_redbean'
)
```

or by setting `REDBEAN_DIRECTORY` and `REDBEAN_NAMESPACE` environment variables.

```bash
REDBEAN_DIRECTORY=my_module/my_redbean
REDBEAN_NAMESPACE=my_module.my_redbean
```

In the above example, models will be created in `my_module/my_redbean` directory 
and will be available as `my_module.my_redbean` namespace.

#
# ___