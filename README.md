# Custom filters for Jinja (Home Assistant) Templates

## Installation

### Install via [HACS](https://hacs.xyz/)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=TimothyJCowen&repository=https%3A%2F%2Fgithub.com%2FTimothyJCowen%2Fha_custom_filters)

Either:

-   Use the above link
-   Follow the HACS instructions for adding a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/).

## Example (`double`)

In this example, we will create a filter which doubles any number it is used upon.

Create a file to store your new filter in.
You can have multiple filters in a single file, but all files **MUST** exist in the `/config/custom_filters/` directory of your Home Assistant instance. Sub-directories are currently unsupported.

**filters.py:**

```py
def double(num):
  return num*2
```

Once you have created your filter, reload the integration configuration.

You should now be able to use your custom filter just like any other filter in your Home Assistant templates:

```jinja
{{ 1 | double }} {# Result: 2 #}
{{ 2 | double }} {# Result: 4 #}
{{ 3 | double }} {# Result: 6 #}
```
