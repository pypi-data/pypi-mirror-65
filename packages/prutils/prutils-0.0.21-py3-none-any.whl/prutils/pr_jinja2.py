import os

from jinja2 import Environment, FileSystemLoader


def gen_file_use_template(tpl_file_path, out_file_path, **kwargs):
    env = Environment(loader=FileSystemLoader(os.path.dirname(tpl_file_path)), keep_trailing_newline=True)
    template = env.get_template(os.path.basename(tpl_file_path))
    output = template.render(**kwargs)
    with open(out_file_path, "w") as f:
        f.write(output)
    return output
